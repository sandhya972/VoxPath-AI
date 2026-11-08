from services.voice_pipeline import process_voice

try:
    result = process_voice("test_audio.wav.m4a")

    print("\n========== FINAL RESULT ==========")
    print("You said:", result["user_text"])
    print("\nVoxPath replied:", result["ai_response"])
    print("\nAudio:", result["audio_file"])

except Exception as error:
    print("\nPipeline Error:", error)