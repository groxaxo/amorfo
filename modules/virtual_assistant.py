# modules/virtual_assistant.py

import os
import time
import wave
import numpy as np
import sounddevice as sd
from typing import Optional
from modules.logging import logger
from modules.whisper_recognizer import WhisperRecognizer
from modules.lm_client import LMStudioClient, VLLMClient
from modules.hotword_detector import HotwordDetector
from modules.performance import PerformanceMonitor
from modules.config import load_config
from modules.tools import Tools

class VirtualAssistant:
    def __init__(self, config_path: str = "settings.yml"):
        self.config = load_config(config_path)
        self.recognizer = WhisperRecognizer(
            model_name=self.config["whisper"]["model"],
            sample_rate=self.config["whisper"]["sample_rate"],
            config=self.config
        )

        self.tools = Tools(self.config)
        self.session_id = "default_session"

        llm_client_type = self.config.get("assistant", {}).get("llm_client", "lmstudio")
        logger.info("Using LLM client: %s", llm_client_type)

        if llm_client_type == "vllm":
            if "vllm" not in self.config:
                raise ValueError("vllm configuration not found in settings.yml")
            self.chat_client = VLLMClient(self.config, self.tools)
            self.tts_client = LMStudioClient(self.config)
        elif llm_client_type == "lmstudio":
            self.chat_client = LMStudioClient(self.config, self.tools)
            self.tts_client = self.chat_client
        else:
            raise ValueError(f"Unsupported llm_client type: {llm_client_type}")

        # Always initialize hotword detector if enabled in config
        self.hotword_detector = HotwordDetector(config=self.config) if self.config["hotword"]["enabled"] else None
        self.performance = PerformanceMonitor()
        self._running = False

    def run(self):
        self._running = True
        logger.info("Assistant started. Press ENTER or say '%s' to interact.", self.config["hotword"]["phrase"])
        
        try:
            while self._running:
                try:
                    if not self._wait_for_activation():
                        continue
                    # Record and process user input
                    user_text = self.recognizer.transcribe()
                    if not user_text:
                        logger.warning("No speech detected.")
                        continue

                    # Retrieve context from memory
                    history_limit = self.config.get("memory", {}).get("redis", {}).get("conversation_limit", 10)
                    history = self.tools.redis_memory.get_conversation_history(self.session_id, limit=history_limit)

                    chroma_results = self.config.get("memory", {}).get("chromadb", {}).get("search_results", 3)
                    documents = self.tools.chroma_memory.search(user_text, n_results=chroma_results)

                    context = ""
                    if documents and documents[0]:
                        context += "Here are some documents that might be relevant:\n"
                        for doc in documents[0]:
                            context += f"- {doc}\n"

                    if history:
                        context += "Here is the recent conversation history:\n"
                        for turn in history:
                            context += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"

                    full_input = f"{context}\nUser's new question: {user_text}"

                    # Get and process response
                    response_text = self.chat_client.chat(full_input)
                    self.performance.add_tokens(len(response_text.split()))
                    
                    # Save conversation to memory
                    self.tools.redis_memory.save_conversation(self.session_id, user_text, response_text)

                    # Synthesize speech
                    word_count = len(response_text.split())
                    if word_count > self.config["segmentation"]["max_words"]:
                        logger.info("Response is long (%d words). Segmenting...", word_count)
                        output_file = self.tts_client.synthesize_long_text(response_text)
                    else:
                        output_file = self.tts_client.synthesize_speech(response_text)
                    
                    # Play audio and wait for the activation signal before next loop
                    self.play_audio(output_file)
                    self._wait_for_activation()  # Wait again after audio playback
                except Exception as e:
                    logger.error("Error in main loop: %s", str(e))
                    time.sleep(1)
                    
        except KeyboardInterrupt:
            logger.info("Exiting assistant. Goodbye!")
        finally:
            try:
                self.performance.report(force=True)
            except Exception as e:
                logger.error("Error in performance report: %s", str(e))
            self._running = False

    def stop(self):
        self._running = False

    def _flush_stdin(self):
        """Flush any lingering input from stdin."""
        try:
            import sys
            import termios
            termios.tcflush(sys.stdin, termios.TCIFLUSH)
        except Exception:
            try:
                import msvcrt
                while msvcrt.kbhit():
                    msvcrt.getch()
            except Exception:
                pass

    def _wait_for_activation(self) -> bool:
        """
        Wait for activation either by detecting a keypress (push-to-talk)
        or by detecting the hotword, whichever comes first.
        """
        logger.info("Waiting for activation: press ENTER or say the hotword...")
        hotword_timeout = self.config["hotword"]["timeout_sec"] if self.hotword_detector else 0
        elapsed = 0.0
        check_interval = 0.5
        while elapsed < hotword_timeout:
            if self._check_for_keypress():
                self._flush_stdin()
                return True
            if self.hotword_detector and self.hotword_detector.check_for_hotword(timeout=check_interval):
                return True
            time.sleep(check_interval)
            elapsed += check_interval
        # Fallback to blocking push-to-talk input if neither hotword nor keypress detected within the timeout
        input("Press ENTER to speak...")
        return True

    def _check_for_keypress(self) -> bool:
        """Non-blocking keypress check."""
        try:
            import msvcrt  # Windows
            return msvcrt.kbhit()
        except ImportError:
            import sys
            import select  # Unix
            return sys.stdin in select.select([sys.stdin], [], [], 0)[0]

    def play_audio(self, filename: str):
        """Play audio with normalization and error handling."""
        if not os.path.exists(filename):
            logger.error("Audio file not found: %s", filename)
            return
        try:
            with wave.open(filename, "rb") as wf:
                sample_rate = wf.getframerate()
                audio_data = wf.readframes(wf.getnframes())
            audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32767.0
            if self.config["speech"]["normalize_audio"]:
                max_val = np.max(np.abs(audio_array))
                if max_val > 0:
                    audio_array = audio_array / max_val
            sd.play(audio_array, samplerate=sample_rate)
            sd.wait()
        except Exception as e:
            logger.error("Audio playback error: %s", str(e))
            raise
