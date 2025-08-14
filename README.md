## Status Update

Abandoned: Between Orpheus not being a good fit, and other reasons I'm not working on this any longer. I'm keeping the repo up for others who wish to continue if any. 

Try MiraiAssist instead. It is still a WIP. https://github.com/Nighthawk42/MiraiAssist 

# ------------
# mOrpheus Virtual Assistant Demo

This project implements the mOrpheus Virtual Assistant, which integrates speech recognition, text generation, and text-to-speech (TTS) synthesis. The assistant leverages several state-of-the-art components:

- **Whisper** for speech recognition.
- **LM Studio API** for both text generation (chat) and text-to-speech synthesis.
- **SNAC-based decoder** to convert TTS token streams into PCM audio.

## Features

- **Speech Recognition:**  
  Captures audio from the microphone and transcribes it using the Whisper model.

- **Text Generation:**  
  Uses LM Studio’s chat API to generate natural language responses based on transcribed input.

- **Text-to-Speech:**  
  Converts the generated text into speech via LM Studio’s TTS API. The text is cleaned (removing newlines, markdown symbols, and emojis) before being sent to the TTS engine, and the resulting token stream is decoded using a SNAC-based decoder.
  

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

This project uses Docker and Docker Compose to simplify the installation process. An interactive installer is provided to guide you through the setup.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [LM Studio](https://lmstudio.ai/)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/morpheus-virtual-assistant.git
   cd morpheus-virtual-assistant
   ```

2. **Install installer dependencies:**

   ```bash
   pip install -r requirements-installer.txt
   ```

3. **Run the interactive installer:**

   ```bash
   python install.py
   ```

   The installer will:
   - Check for Docker and Docker Compose.
   - Guide you through configuring the `settings.yml` file.
   - Help you select your audio input and output devices.

3. **Run LM Studio**
   Before starting the assistant, you must have LM Studio running with the required LLM and TTS models loaded and the API server started.

4. **Run the Assistant:**

   ```bash
   docker-compose up --build
   ```

   This command will build the Docker image and start the mOrpheus virtual assistant.


## Suggested Models

These are the models I tested with, your milage may vary with additional models.

**LLM Models:**
- gemma-3-12b-it-GGUF/gemma-3-12b-it-Q3_K_L.gguf

**Orpheus Models:**
- lex-au/Orpheus-3b-FT-Q2_K.gguf - Fastest inference (~50% faster tokens/sec than Q8_0).
- lex-au/Orpheus-3b-FT-Q4_K_M.gguf - Balanced quality/speed.
- lex-au/Orpheus-3b-FT-Q8_0.gguf - Original high-quality model.

## Usage

- **Activation:**  
  The assistant listens for activation either via a hotword ("Hey Assistant") or a push-to-talk keypress (or both, depending on your settings).  
- **Speech Processing:**  
  It records your speech, transcribes it using Whisper, and generates a text response via LM Studio’s chat API.
- **TTS Synthesis:**  
  The response is cleaned to remove unwanted characters (e.g., emojis, newlines, markdown formatting) and then sent to LM Studio’s TTS API. The SNAC-based decoder converts the TTS token stream into PCM audio.
- **Audio Playback:**  
  The generated audio is played back, and a brief delay is applied before the assistant waits for the next activation.

## Contributing

Feel free to open issues or submit pull requests with improvements or bug fixes. I'm fairly new at this and feel this could see a lot of improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Notice

See the [NOTICE](NOTICE) file for details.
