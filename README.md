Amorfo - A Voice-Activated, Tool-Using Virtual Assistant
Overview
Amorfo is an advanced, voice-powered virtual assistant built for real-world tasks, not just chat. It combines cutting-edge speech recognition, text generation, and text-to-speech (TTS) with a robust tool framework and long-term memory. Amorfo can search the web, browse sites, and learn over time.
Features
	•	Voice Interaction:
	◦	Speech-to-Text: Uses OpenAI’s Whisper for fast, accurate transcription.
	◦	Text-to-Speech: High-quality AI TTS (via LM Studio) for natural responses.
	◦	Activation: Supports hotword (“Hey Cassie”) or push-to-talk.
	•	Flexible LLM Backends:
	◦	Model-agnostic, supports OpenAI API-compatible models.
	◦	Works with LM Studio or vLLM for easy switching.
	•	Tool System:
	◦	Agency: Uses tools to interact externally.
	◦	Web Search: Integrates SearxNG for private searches.
	◦	Web Browsing: Uses Playwright to navigate websites.
	◦	Memory: Saves data to long-term memory.
	•	Long-Term Memory:
	◦	Conversation Memory: Uses Redis for coherent multi-turn chats.
	◦	Knowledge Base (RAG): Uses ChromaDB for persistent, semantic memory retrieval.
	•	Reproducibility:
	◦	Dockerized: Includes Dockerfile for easy deployment.
How It Works
Amorfo operates in a loop:
	1	Activation: Detects hotword or keypress.
	2	Listen & Transcribe: Records and transcribes audio with Whisper.
	3	Think & Act:
	◦	Recall: Retrieves context from Redis (conversation) and ChromaDB (knowledge).
	◦	Process: LLM processes query with context.
	◦	Tool Use: Optionally uses tools (e.g., web search) and feeds results back.
	4	Respond: Generates text response.
	5	Speak: Synthesizes and plays response.
	6	Memorize: Saves conversation to Redis.
Getting Started
Prerequisites
	•	OpenAI-compatible LLM endpoint (vLLM or LM Studio).
	•	Redis for memory.
	•	SearxNG (optional, for web search).
Configuration
	1	Create settings.yml from example.
	2	Update with LLM, Redis, and SearxNG URLs/ports.
	3	Set llm_client to "vllm" or "lmstudio" in settings.yml.
Docker (Recommended)
	1	Build image: docker build -t amorfo-assistant .
	2	
	3	Run container: docker run --rm -it --net=host -v ./outputs:/usr/src/app/outputs amorfo-assistant
	4	
Local Run
	1	Install dependencies: pip install -r requirements.txt
	2	playwright install --with-deps
	3	
	4	Run: python amorfo.py
	5	
License
MIT License. See LICENSE.
Notice
See NOTICE.
