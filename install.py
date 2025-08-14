import subprocess
import sys

try:
    import yaml
    import sounddevice as sd
except ImportError:
    print("❌ Missing dependencies for the installer.")
    print("Please install them by running: pip install -r requirements-installer.txt")
    sys.exit(1)

def check_prerequisites():
    """Checks if Docker and Docker Compose are installed."""
    print("--- Checking Prerequisites ---")
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
        print("✅ Docker is installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker is not installed. Please install Docker before proceeding.")
        sys.exit(1)

    try:
        subprocess.run(["docker-compose", "--version"], check=True, capture_output=True)
        print("✅ Docker Compose is installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker Compose is not installed. Please install Docker Compose before proceeding.")
        sys.exit(1)

    print("\n--- External Dependencies ---")
    print("This application requires LM Studio to be running in the background.")
    print("Please ensure you have downloaded, installed, and started the LM Studio server.")
    input("Press Enter to continue once LM Studio is running...")


def get_audio_devices():
    """Returns a list of available audio devices."""
    devices = sd.query_devices()
    input_devices = [(i, d['name']) for i, d in enumerate(devices) if d['max_input_channels'] > 0]
    output_devices = [(i, d['name']) for i, d in enumerate(devices) if d['max_output_channels'] > 0]
    return input_devices, output_devices

def select_audio_device(prompt, devices):
    """Prompts the user to select an audio device."""
    print(prompt)
    for i, name in devices:
        print(f"  {i}: {name}")

    while True:
        try:
            choice = input(f"Select the device number (or press Enter for default): ")
            if not choice:
                return None
            return int(choice)
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_user_config():
    """Gathers configuration from the user."""
    config = {
        'whisper': {},
        'lm': {'chat': {}, 'tts': {}},
        'tts': {},
        'audio': {},
        'vad': {},
        'hotword': {},
        'segmentation': {},
        'speech': {},
        'interaction': {}
    }

    print("\n--- Whisper Configuration ---")
    config['whisper']['model'] = input("Enter Whisper model name [small.en]: ") or "small.en"
    config['whisper']['sample_rate'] = 16000

    print("\n--- LM Studio Configuration ---")
    config['lm']['api_url'] = input("Enter LM Studio API URL [http://127.0.0.1:1234/v1]: ") or "http://127.0.0.1:1234/v1"
    config['lm']['chat']['endpoint'] = "/chat/completions"
    config['lm']['chat']['model'] = input("Enter Chat model name [gemma-3-12b-it]: ") or "gemma-3-12b-it"
    config['lm']['tts']['endpoint'] = "/completions"
    config['lm']['tts']['model'] = input("Enter TTS model name [orpheus-3b-ft.gguf@q2_k]: ") or "orpheus-3b-ft.gguf@q2_k"

    print("\n--- Audio Configuration ---")
    input_devices, output_devices = get_audio_devices()
    config['audio']['input_device'] = select_audio_device("Select Input Device:", input_devices)
    config['audio']['output_device'] = select_audio_device("Select Output Device:", output_devices)
    config['audio']['hotword_sample_rate'] = 16000

    print("\n--- Hotword Configuration ---")
    config['hotword']['enabled'] = input("Enable hotword detection? (y/n) [y]: ").lower() != 'n'
    config['hotword']['phrase'] = input("Enter hotword phrase [Hey Assistant]: ") or "Hey Assistant"

    print("\n--- Interaction Configuration ---")
    config['interaction']['mode'] = input("Interaction mode (push_to_talk, hotword, both) [both]: ") or "both"

    # Add default values for other settings
    config['tts']['sample_rate'] = 24000
    config['vad'] = {'mode': 2, 'frame_duration_ms': 30, 'silence_threshold_ms': 1000, 'min_record_time_ms': 2000}
    config['hotword'].update({'sensitivity': 0.7, 'timeout_sec': 5, 'retries': 3})
    config['segmentation'] = {'max_words': 60}
    config['speech'] = {'normalize_audio': False, 'default_pitch': 0, 'min_speech_confidence': 0.5, 'max_retries': 3}
    config['interaction']['post_audio_delay'] = 0.5

    return config

def main():
    """Main function for the installer."""
    print("--- Welcome to the mOrpheus Installer ---")
    check_prerequisites()
    config = get_user_config()

    with open('settings.yml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

    print("\n✅ Configuration complete! `settings.yml` has been created.")
    print("\nTo start the assistant, run the following command:")
    print("  docker-compose up --build")

if __name__ == "__main__":
    main()
