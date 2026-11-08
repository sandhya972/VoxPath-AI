import os
import subprocess
from pathlib import Path

import imageio_ffmpeg

from flask import Flask, request, jsonify, render_template,session
from werkzeug.utils import secure_filename

from services.voice_pipeline import process_voice
from services.response_engine import generate_response
from services.timbre import generate_speech
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "voxpath-development-key")
# Configuration
UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024

ALLOWED_EXTENSIONS = {"wav", "mp3", "m4a", "ogg", "webm"}
def convert_to_wav(input_path, output_path):
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    command = [
        ffmpeg_exe,
        "-y",
        "-i", str(input_path),
        "-ar", "24000",
        "-ac", "1",
        str(output_path)
    ]

    subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True
    )

    return output_path

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/health")
def health():
    return jsonify({
        "status": "success",
        "message": "VoxPath AI backend is running!"
    })


@app.route("/api/voice", methods=["POST"])
def voice():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file received."}), 400

    audio = request.files["audio"]

    if not audio.filename:
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(audio.filename):
        return jsonify({"error": "Unsupported audio format."}), 400

    filename = secure_filename(audio.filename)
    audio_path = UPLOAD_FOLDER / filename
    converted_path = UPLOAD_FOLDER / f"{Path(filename).stem}_converted.wav"

    try:
        audio.save(audio_path)

        print("\nConverting uploaded audio to WAV...")
        convert_to_wav(audio_path, converted_path)
        print("Audio conversion successful!")

        # Get previous conversation
        conversation_history = session.get("conversation_history", [])

        # Process voice with conversation context
        result = process_voice(
            str(converted_path),
            conversation_history
        )

        # Save current conversation
        conversation_history.append({
            "user": result["user_text"],
            "assistant": result["ai_response"]
        })

        # Keep only the latest 5 exchanges
        session["conversation_history"] = conversation_history[-5:]
        session.modified = True

        return jsonify({
            "status": "success",
            "transcript": result["user_text"],
            "response": result["ai_response"],
            "audio_url": "/" + result["audio_file"].replace("\\", "/")
        })

    except Exception:
        app.logger.exception("Voice processing failed")
        return jsonify({
            "error": "Voice processing failed. Please try again."
        }), 500

    finally:
        if audio_path.exists():
            audio_path.unlink()

        if converted_path.exists():
            converted_path.unlink()

@app.route("/api/reset", methods=["POST"])
@app.route("/api/chat", methods=["POST"])
def text_chat():

    try:
        data = request.get_json()

        user_text = data.get("message", "").strip()

        if not user_text:
            return jsonify({"error": "Please enter a message."}), 400

        # Retrieve conversation history
        conversation_history = session.get("conversation_history", [])

        # Generate response
        ai_response = generate_response(user_text, conversation_history)

        # Generate voice response
        audio_path = generate_speech(ai_response)

        # Save conversation
        conversation_history.append({
            "user": user_text,
            "assistant": ai_response
        })

        session["conversation_history"] = conversation_history[-5:]
        session.modified = True

        return jsonify({
            "status": "success",
            "transcript": user_text,
            "response": ai_response,
            "audio_url": "/" + audio_path.replace("\\", "/")
        })

    except Exception:
        app.logger.exception("Text chat failed")
        return jsonify({
            "error": "Unable to process your message."
        }), 500
def reset_conversation():
    session.pop("conversation_history", None)

    return jsonify({
        "status": "success",
        "message": "Conversation reset successfully."
    })

if __name__ == "__main__":
    app.run(debug=True)