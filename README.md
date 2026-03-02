## Status Update

Abandoned: Between Orpheus not being a good fit, and other reasons I'm not working on this any longer. I'm keeping the repo up for others who wish to continue if any. 

Try MiraiAssist instead. It is still a WIP. https://github.com/Nighthawk42/MiraiAssist 

# ------------
# mOrpheus Virtual Assistant Demo

This project implements the mOrpheus Virtual Assistant, which integrates speech recognition, text generation, and text-to-speech (TTS) synthesis. The assistant is being modernized around:

- **Whisper** for speech recognition.
- **Silero VAD** for robust voice-activity detection.
- **vLLM** for low-latency LLM serving.
- **Parakeet TTS 0.3 multilingual** for multilingual speech synthesis.

## Bottlenecks and Improvement Plan

### Current bottlenecks
- **Single-backend coupling:** chat and TTS are currently tied to one backend API shape.
- **VAD accuracy/runtime tradeoff:** the previous WebRTC-based VAD can miss softer speech in real-world environments.
- **Limited UX/project page clarity:** repository documentation does not clearly present architecture, roadmap, and frontend direction.
- **Monolithic runtime flow:** audio capture, inference calls, and playback happen in a tightly sequential loop.

### Required target stack
The project direction is now:
1. **Silero VAD** for speech boundary detection.
2. **Parakeet TTS 0.3 multilingual** for speech synthesis.
3. **vLLM** for LLM deployment and chat completions.

### Frontend and project-page improvements
- Add a lightweight web UI (session transcript, latency cards, model/runtime status, push-to-talk button).
- Expose a small backend API boundary (`/stt`, `/chat`, `/tts`, `/health`) so UI and voice loop can evolve independently.
- Keep this README as the project page with a clear architecture section, migration checklist, and performance goals.

## Features

- **Speech Recognition:**  
  Captures audio from the microphone and transcribes it using the Whisper model.

- **Text Generation:**  
  Uses a vLLM OpenAI-compatible endpoint to generate natural language responses based on transcribed input.

- **Text-to-Speech:**  
  Converts generated text into speech with Parakeet TTS 0.3 multilingual.
  

- **Audio Playback & Activation:**  
  Plays the generated audio and waits for the next activation. Long responses are segmentented then recombined at playback. The assistant supports both push‑to‑talk (keypress) and hotword (“Hey Assistant”) activation, or both simultaneously, as configured.

## Requirements

- Python 3.7+
- [PyTorch](https://pytorch.org/)
- [Whisper](https://github.com/openai/whisper)
- [sounddevice](https://python-sounddevice.readthedocs.io/)
- [scipy](https://www.scipy.org/)
- [numpy](https://numpy.org/)
- [requests](https://docs.python-requests.org/)
- [PyYAML](https://pyyaml.org/)
- [Transformers](https://huggingface.co/transformers/)
- [SNAC](https://github.com/hubertsiuzdak/snac)

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/morpheus-virtual-assistant.git
   cd morpheus-virtual-assistant
   ```

2. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   *Ensure that your `requirements.txt` includes all required packages.*

3. **Configure the application:**

   - Create a `settings.yml` file in the project root.
   - Populate it with your configuration details for Whisper, vLLM API, Parakeet TTS, audio settings, and interaction mode.

   Example `settings.yml`:

   ```yaml
   # -------------------------------
   # Configuration for Whisper STT
   # -------------------------------
   whisper:
     model: "small.en"
     sample_rate: 16000

   # -------------------------------
    # Configuration for vLLM + Parakeet services
   # -------------------------------
   lm:
      api_url: "http://127.0.0.1:8000/v1"
     
     chat:
       endpoint: "/chat/completions"
        model: "meta-llama/Llama-3.1-8B-Instruct"
       system_prompt: "You are a helpful assistant."
       max_tokens: 256
       temperature: 0.7
       top_p: 0.9
       repetition_penalty: 1.1
       max_response_time: 10.0

     tts:
        endpoint: "/audio/speech"
        model: "parakeet-tts-0.3-multilingual"
        default_voice: "alloy"
       max_tokens: 4096
       temperature: 0.6
       top_p: 0.9
       repetition_penalty: 1.0
       speed: 1.0
       max_segment_duration: 20

   # -------------------------------
   # TTS Audio Output Configuration
   # -------------------------------
   tts:
     sample_rate: 24000

   # -------------------------------
   # Audio Device Configuration
   # -------------------------------
   audio:
     input_device: null
     output_device: null
     hotword_sample_rate: 16000

   # -------------------------------
   # Voice Activity Detection (VAD) Configuration
   # -------------------------------
   vad:
      provider: "silero"
      mode: 2
     frame_duration_ms: 30
     silence_threshold_ms: 1000
     min_record_time_ms: 2000

   # -------------------------------
   # Hotword Detection Configuration
   # -------------------------------
   hotword:
     enabled: true
     phrase: "Hey Assistant"
     sensitivity: 0.7
     timeout_sec: 5
     retries: 3

   # -------------------------------
   # Segmentation Configuration for TTS
   # -------------------------------
   segmentation:
     max_words: 60

   # -------------------------------
   # Speech Quality Configuration
   # -------------------------------
   speech:
     normalize_audio: false
     default_pitch: 0
     min_speech_confidence: 0.5
     max_retries: 3

   # -------------------------------
   # Interaction Configuration
   # -------------------------------
   interaction:
     mode: "both"  # Options: "push_to_talk", "hotword", or "both"
     post_audio_delay: 0.5
   ```

4. **Run inference backends**
Before activating the assistant, start:
- a **vLLM** server exposing an OpenAI-compatible chat endpoint.
- a **Parakeet TTS 0.3 multilingual** endpoint for synthesis.

5. **Run the Assistant:**

   ```bash
   python morpheus.py
   ```


## Suggested Deployments

These are suggested starting points; adjust based on your hardware and latency goals.

**LLM (vLLM):**
- `meta-llama/Llama-3.1-8B-Instruct`

**TTS (Parakeet):**
- `parakeet-tts-0.3-multilingual`

## Usage

- **Activation:**  
  The assistant listens for activation either via a hotword ("Hey Assistant") or a push-to-talk keypress (or both, depending on your settings).  
- **Speech Processing:**  
  It records your speech, transcribes it using Whisper, gates speech regions with Silero VAD, and generates text via vLLM.
- **TTS Synthesis:**  
  The response is cleaned to remove unwanted characters (e.g., emojis, newlines, markdown formatting) and synthesized with Parakeet TTS 0.3 multilingual.
- **Audio Playback:**  
  The generated audio is played back, and a brief delay is applied before the assistant waits for the next activation.

## Contributing

Feel free to open issues or submit pull requests with improvements or bug fixes. I'm fairly new at this and feel this could see a lot of improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Notice

See the [NOTICE](NOTICE) file for details.

## Donations
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/P5P21QRW51)
