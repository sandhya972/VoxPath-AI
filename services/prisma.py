import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GNANI_API_KEY")
BASE_URL = "https://api.vachana.ai"


def transcribe_audio(audio_path):

    if not API_KEY:
        raise ValueError("Gnani API key is missing. Check your .env file.")

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    url = f"{BASE_URL}/stt/v3"

    headers = {
        "X-API-Key-ID": API_KEY
    }

    data = {
        "model": "prisma-v3.0",
        "language_code": "indic-auto"
    }

    with open(audio_path, "rb") as audio:

        files = {
            "audio_file": (
                os.path.basename(audio_path),
                audio
            )
        }

        response = requests.post(
            url,
            headers=headers,
            files=files,
            data=data,
            timeout=60
        )

    if not response.ok:
        print("GNANI ERROR STATUS:", response.status_code)
        print("GNANI ERROR DETAILS:", response.text)

    response.raise_for_status()

    result = response.json()

    if not result.get("success"):
        raise RuntimeError(f"Transcription failed: {result}")

    return result


if __name__ == "__main__":
    print("Gnani Prisma integration is ready!")