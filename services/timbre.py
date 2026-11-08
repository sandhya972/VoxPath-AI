import os
from pathlib import Path

from dotenv import load_dotenv
from gnani.tts import GnaniTTSClient, DEFAULT_MODEL, AudioConfig

load_dotenv()

def generate_speech(text, output_path="static/audio/response.wav",
                    voice="Pranav", language="en-IN"):

    if not text.strip():
        raise ValueError("Text cannot be empty.")

    api_key = os.getenv("GNANI_API_KEY")

    if not api_key:
        raise ValueError("Gnani API key missing. Check your .env file.")

    client = GnaniTTSClient(api_key=api_key)

    audio_config = AudioConfig(
        sample_rate=24000,
        encoding="linear_pcm",
        num_channels=1,
        sample_width=2,
        container="wav"
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    client.synthesize(
        text,
        voice=voice,
        model=DEFAULT_MODEL,
        language=language,
        audio_config=audio_config,
        output_file=output_path
    )

    return str(output_path)


if __name__ == "__main__":
    print("Timbre TTS integration is ready!")