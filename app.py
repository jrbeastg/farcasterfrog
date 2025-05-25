from flask import Flask, request, jsonify, render_template
import json
from datetime import datetime

app = Flask(__name__)
ENTRIES_FILE = "data.json"

@app.route("/")
def home():
    return render_template("frame.html")

@app.route("/api/enter", methods=["POST"])
def enter_lottery():
    data = request.form.to_dict()
    fid = data.get("fid")
    if not fid:
        return jsonify({"error": "FID missing"}), 400

    # Load current entries
    try:
        with open(ENTRIES_FILE, "r") as f:
            entries = json.load(f)
    except:
        entries = []

    entries.append({
        "fid": fid,
        "joined_at": datetime.utcnow().isoformat()
    })

    with open(ENTRIES_FILE, "w") as f:
        json.dump(entries, f, indent=2)

    return "🎉 You've entered the lottery!", 200

@app.route("/entries")
def show_entries():
    with open(ENTRIES_FILE, "r") as f:
        entries = json.load(f)
    return jsonify(entries)
