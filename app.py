from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Atlas connection (अपना URI डालो)
client = MongoClient("mongodb+srv://admin:test12345@cluster0.7easxzl.mongodb.net/flask_db?retryWrites=true&w=majority&appName=cluster0")
db = client["flask_db"]       # database name
collection = db["users"]      # collection name

# ---------- API Route ----------
@app.route("/api")
def api_data():
    with open("data.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

# ---------- Form Page ----------
@app.route("/")
def index():
    return render_template("form.html")

# ---------- Form Submission ----------
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form.get("name")
        email = request.form.get("email")

        # Insert into MongoDB
        collection.insert_one({"name": name, "email": email})

        return redirect(url_for("success"))
    except Exception as e:
        return render_template("form.html", error=str(e))

# ---------- Success Page ----------
@app.route("/success")
def success():
    return "Data submitted successfully"

if __name__ == "__main__":
    app.run(debug=True)
