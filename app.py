from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
DB_FILE = "database.db"

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        wallet TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/claim', methods=["GET", "POST"])
def claim():
    if request.method == "POST":
        name = request.form['name']
        wallet = request.form['wallet']
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO requests (name, wallet, timestamp) VALUES (?, ?, ?)", (name, wallet, timestamp))
        conn.commit()
        conn.close()

        return '''<script>alert("Request received! Admin will verify your wallet."); window.location.href = "/claim";</script>'''

    return render_template("claim.html")

@app.route('/security')
def security():
    return render_template("security.html")

@app.route('/technologie')
def technologie():
    return render_template("technologie.html")

@app.route('/admin')
def admin():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, wallet, timestamp FROM requests ORDER BY timestamp DESC")
    requests_data = c.fetchall()
    conn.close()
    return render_template("admin.html", requests=[{'name': n, 'wallet': w, 'timestamp': t} for n, w, t in requests_data])

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=8080)
