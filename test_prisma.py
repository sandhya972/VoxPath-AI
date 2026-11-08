from services.prisma import transcribe_audio

try:
    print("Sending audio to Gnani Prisma...")

    result = transcribe_audio("test_audio.wav.m4a")

    print("\n========== TRANSCRIPTION RESULT ==========")
    print("Success:", result.get("success"))
    print("Transcript:", result.get("transcript"))
    print("Detected language:", result.get("detected_language_code"))
    print("Model:", result.get("model"))

except Exception as error:
    print("\nError:", error)