import sqlite3
from os import path

base_dir = path.dirname(path.abspath(__file__))
db_path = path.join(base_dir, "blocklists")
connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()

