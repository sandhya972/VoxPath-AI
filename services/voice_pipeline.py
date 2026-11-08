from services.prisma import transcribe_audio
from services.response_engine import generate_response
from services.timbre import generate_speech


def process_voice(audio_path, conversation_history=None):
    """
    Complete VoxPath voice interaction:
    1. Convert user's speech into text.
    2. Generate a career-related response.
    3. Convert the response into speech.
    """

    print("\n========== VOXPATH VOICE PIPELINE ==========")

    # STEP 1: Speech to Text
    print("\n[1] Listening to user...")

    transcription = transcribe_audio(audio_path)
    user_text = transcription.get("transcript", "")

    if not user_text.strip():
        raise ValueError("Could not recognize the user's speech.")

    print("User said:", user_text)

    # STEP 2: Generate Response
    print("\n[2] Generating career response...") 
    ai_response = generate_response(user_text, conversation_history)

    print("VoxPath:", ai_response)

    # STEP 3: Text to Speech
    print("\n[3] Converting response into speech...")

    audio_output = generate_speech(
        ai_response,
        output_path="static/audio/voxpath_response.wav",
        voice="Pranav",
        language="en-IN"
    )

    print("Audio generated:", audio_output)

    print("\n========== VOXPATH COMPLETED ==========")

    return {
        "user_text": user_text,
        "ai_response": ai_response,
        "audio_file": audio_output
    }