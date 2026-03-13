from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from llm_task_extractor import extract_tasks_llm
from github_api import create_github_issue
from audio_to_text import convert_audio_to_text
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# serve frontend
@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)


# process transcript text
@app.route("/process-text", methods=["POST"])
def process_text():

    try:
        data = request.json
        transcript = data.get("transcript", "")

        if not transcript:
            return jsonify({"error": "No transcript provided"}), 400

        summary, tasks = extract_tasks_llm(transcript)

        return jsonify({
            "summary": summary,
            "tasks": tasks
        })

    except Exception as e:
        print("PROCESS TEXT ERROR:", e)
        return jsonify({"error": "Failed to process transcript"}), 500


# upload audio and convert to transcript
@app.route("/upload-audio", methods=["POST"])
def upload_audio():

    try:

        if "audio" not in request.files:
            return jsonify({"error": "No audio file uploaded"}), 400

        file = request.files["audio"]

        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        transcript = convert_audio_to_text(path)

        if transcript is None or transcript.strip() == "":
            return jsonify({"error": "Audio could not be understood"}), 400

        summary, tasks = extract_tasks_llm(transcript)

        # IMPORTANT: returning transcript also
        return jsonify({
            "transcript": transcript,
            "summary": summary,
            "tasks": tasks
        })

    except Exception as e:
        print("UPLOAD AUDIO ERROR:", e)
        return jsonify({"error": "Audio processing failed"}), 500


# create github issue
@app.route("/create-issue", methods=["POST"])
def create_issue():

    try:

        data = request.json

        repo = data.get("repo")
        token = data.get("token")
        task = data.get("task")

        if not repo or not token or not task:
            return jsonify({"error": "Missing required data"}), 400

        issue = create_github_issue(repo, token, task)

        return jsonify(issue)

    except Exception as e:
        print("CREATE ISSUE ERROR:", e)
        return jsonify({"error": "Failed to create issue"}), 500


if __name__ == "__main__":
    app.run(debug=True)