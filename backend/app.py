from flask import Flask, request, jsonify
import os, json
from datetime import datetime
from flask_cors import CORS # type: ignore

app = Flask(__name__)
CORS(app)  # Allow all origins

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "submissions.json")
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def save_submission(data):
    record = {**data, "timestamp": datetime.utcnow().isoformat()}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            submissions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        submissions = []

    submissions.append(record)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(submissions, f, indent=2)

    return record

# ---------- API Endpoint for frontend ----------
@app.route("/api/submit", methods=["POST"])
def api_submit():
    try:
        # Handle JSON or form submissions
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        name = data.get("name")
        email = data.get("email")
        message = data.get("message")

        if not name or not email or not message:
            return jsonify({"ok": False, "error": "All fields are required"}), 400

        save_submission({"name": name, "email": email, "message": message})
        return jsonify({"ok": True, "message": "Data submitted successfully"})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500

# ---------- Health Check ----------
@app.route("/api/health")
def health():
    return jsonify({"ok": True, "service": "backend"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
