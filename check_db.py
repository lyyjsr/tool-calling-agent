import sqlite3

conn = sqlite3.connect("app.db")

rows = conn.execute(
    "SELECT session_id, role, content FROM messages ORDER BY id DESC LIMIT 5"
).fetchall()

print(rows)