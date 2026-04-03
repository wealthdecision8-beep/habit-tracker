from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import date, datetime

app = Flask(__name__)
DATA_FILE = "habits.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"habits": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    data = load_data()
    today = str(date.today())
    return render_template("index.html", habits=data["habits"], today=today)

@app.route("/add", methods=["POST"])
def add_habit():
    name = request.form.get("name", "").strip()
    emoji = request.form.get("emoji", "✅").strip()
    if name:
        data = load_data()
        data["habits"].append({
            "id": int(datetime.now().timestamp() * 1000),
            "name": name,
            "emoji": emoji,
            "completions": []
        })
        save_data(data)
    return redirect(url_for("index"))

@app.route("/toggle", methods=["POST"])
def toggle():
    habit_id = int(request.form.get("habit_id"))
    today = str(date.today())
    data = load_data()
    for habit in data["habits"]:
        if habit["id"] == habit_id:
            if today in habit["completions"]:
                habit["completions"].remove(today)
            else:
                habit["completions"].append(today)
            break
    save_data(data)
    return redirect(url_for("index"))

@app.route("/delete", methods=["POST"])
def delete_habit():
    habit_id = int(request.form.get("habit_id"))
    data = load_data()
    data["habits"] = [h for h in data["habits"] if h["id"] != habit_id]
    save_data(data)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
