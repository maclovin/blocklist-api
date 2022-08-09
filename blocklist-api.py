import sqlite3
from os import path
from flask import Flask, jsonify, request

base_dir = path.dirname(path.abspath(__file__))
db_path = path.join(base_dir, "db/blocklists")
connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()

app = Flask(__name__)
app.config["DEBUG"] = True

def fetch_all_ips():
    ips = []
    connection.row_factory = sqlite3.Row
    cursor.execute("SELECT * FROM firehol;")
    rows = cursor.fetchall()
    
    for i in rows:
        ips.append(i[0])

    return ips

def fetch_ips(ips_list):
    found_ips = []
    query = "SELECT * FROM firehol WHERE ip IN (%s);" %(", ".join([str("'" + ip + "'") for ip in ips_list]))
    connection.row_factory = sqlite3.Row
    cursor.execute(query)
    rows = cursor.fetchall()

    for i in rows:
        found_ips.append(i[0])

    sam_found_ips = list(set(found_ips))
    
    return sam_found_ips

@app.route("/", methods=["GET"])
def home():
    return "<h1>Blocklist API</h1><p>To be described...</p>"

@app.route("/list", methods=["GET"])
def get_list():
    offset = int(request.args.get("offset"))
    per_page = int(request.args.get("perPage"))
    ips = fetch_all_ips()

    return jsonify(ips[offset: offset + per_page])

@app.route("/find", methods=["GET"])
def find_ips():
    ips = request.args.get("ips")
    print(ips)
    
    split_ips = ips.split(",")
    found_ips = fetch_ips(split_ips)
    not_found_ips = list(set(split_ips).symmetric_difference(set(found_ips)))
    response = {"found": found_ips, "notFound": not_found_ips}

    return jsonify(response)

app.run(debug=True)

