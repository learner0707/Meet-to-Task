from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from task_extractor import extract_tasks
from github_api import create_github_issue
from audio_to_text import convert_audio_to_text
import os

app = Flask(__name__)
CORS(app)

# upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# serve frontend
@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")


# serve css/js
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory("../frontend", path)


# process transcript text
@app.route("/process-text", methods=["POST"])
def process_text():
    try:
        data = request.json
        transcript = data.get("transcript", "")

        summary, tasks = extract_tasks(transcript)

        return jsonify({
            "summary": summary,
            "tasks": tasks
        })

    except Exception as e:
        print("Text processing error:", e)
        return jsonify({
            "summary": [],
            "tasks": []
        })


# process audio upload
@app.route("/upload-audio", methods=["POST"])
def upload_audio():
    try:

        if "audio" not in request.files:
            return jsonify({
                "summary": [],
                "tasks": []
            })

        file = request.files["audio"]

        if file.filename == "":
            return jsonify({
                "summary": [],
                "tasks": []
            })

        # save file
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        # convert audio -> text
        transcript = convert_audio_to_text(path)

        print("Transcript:", transcript)

        if transcript == "":
            return jsonify({
                "summary": ["Audio could not be understood"],
                "tasks": []
            })

        summary, tasks = extract_tasks(transcript)

        return jsonify({
            "summary": summary,
            "tasks": tasks
        })

    except Exception as e:

        print("Audio processing error:", e)

        return jsonify({
            "summary": ["Audio processing failed"],
            "tasks": []
        })


# create github issue
@app.route("/create-issue", methods=["POST"])
def create_issue():
    try:

        data = request.json

        repo = data.get("repo")
        token = data.get("token")
        task = data.get("task")

        issue = create_github_issue(repo, token, task)

        return jsonify(issue)

    except Exception as e:

        print("GitHub issue error:", e)

        return jsonify({
            "issue_title": "Error creating issue",
            "issue_url": "#"
        })


if __name__ == "__main__":
    app.run(debug=True)