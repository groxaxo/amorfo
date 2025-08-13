Amorfo - A Voice-Powered, Tool-Using Virtual Assistant
￼
Table of Contents
	•	Overview
	•	Features
	•	How It Works
	•	Getting Started
	•	Prerequisites
	•	Configuration
	•	Running with Docker (Recommended)
	•	Running Locally
	•	Contributing
	•	License
	•	Notice
Overview
Amorfo is a sophisticated, voice-activated virtual assistant designed as a powerful real-world agent. It integrates advanced speech recognition, text generation, and TTS with a tool-using framework and long-term memory for complex tasks like web searching, browsing, and learning.
Features
	•	Advanced Voice Interaction:
	◦	Speech-to-Text: OpenAI’s Whisper for fast, accurate transcription.
	◦	Text-to-Speech: High-quality AI TTS via LM Studio.
	◦	Activation: Hotword (“Hey Cassie”) or push-to-talk.
	•	Pluggable LLM Backends:
	◦	Model-agnostic, supports OpenAI API format.
	◦	Pre-configured for LM Studio and vLLM.
	•	Extensible Tool System:
	◦	Agency: Interact with external world via tools.
	◦	Web Search: SearxNG for private searches.
	◦	Web Browsing: Playwright to navigate sites.
	◦	Memory Management: Save to long-term memory.
	•	Long-Term Memory:
	◦	Conversational Memory: Redis for multi-turn coherence.
	◦	Knowledge Base (RAG): ChromaDB for persistent semantic retrieval.
	•	Reproducibility:
	◦	Dockerized: Dockerfile for easy deployment.
How It Works
Amorfo runs in a continuous loop:
	1	Activation: Hotword or keypress.
	2	Listen & Transcribe: Record and transcribe with Whisper.
	3	Think & Act: a. Recall: From Redis (conversation) and ChromaDB (knowledge). b. Process: LLM with context. c. Tool Use: If needed (e.g., search), feed back output.
	4	Respond: Generate response.
	5	Speak: Synthesize and play.
	6	Memorize: Save to Redis.
Getting Started
Prerequisites
	•	OpenAI-compatible LLM endpoint (vLLM or LM Studio).
	•	Redis for memory.
	•	SearxNG (optional for search).
Configuration
	1	Copy settings.yml (use example as start).
	2	Update with URLs/ports for LLM, Redis, SearxNG.
	3	Set llm_client to "vllm" or "lmstudio".
Running with Docker (Recommended)
	1	Build image: docker build -t amorfo-assistant .
	2	
	3	Run: docker run --rm -it --net=host -v ./outputs:/usr/src/app/outputs amorfo-assistant
	4	
Running Locally
	1	Install: pip install -r requirements.txt
	2	playwright install --with-deps
	3	
	4	Run: python amorfo.py
	5	
Contributing
Fork, create branch, commit changes, pull request. Issues welcome.
License
MIT License. See LICENSE.
Notice
See NOTICE.
