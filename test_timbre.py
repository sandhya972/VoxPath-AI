from services.timbre import generate_speech

try:
    print("Sending text to Gnani Timbre...")

    audio_file = generate_speech(
        "Hello! Welcome to VoxPath AI. "
        "I am your personal voice-powered career mentor. "
        "Let's explore your career opportunities together."
    )

    print("\n========== TTS RESULT ==========")
    print("Success: True")
    print("Audio file:", audio_file)

except Exception as error:
    print("\nTTS Error:", error)