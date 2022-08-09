import sqlite3
from os import path
from flask import Flask, jsonify, request

base_dir = path.dirname(path.abspath(__file__))
db_path = path.join(base_dir, "db/blocklists")
connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)
app.config["DEBUG"] = True

def fetch_ips():
    ips = []
    connection.row_factory = sqlite3.Row
    cursor.execute("SELECT * FROM firehol")
    rows = cursor.fetchall()
    
    for i in rows:
        print(i[0])
        ips.append(i[0])

    return ips

@app.route("/", methods=["GET"])
def home():
    return "<h1>Blocklist API</h1><p>To be described...</p>"

@app.route("/ips", methods=["GET"])
def get_ips():
    offset = int(request.args.get("offset"))
    per_page = int(request.args.get("per_page"))
    ips = fetch_ips()
    return jsonify(ips[offset: offset + per_page])

app.run(debug=True)

