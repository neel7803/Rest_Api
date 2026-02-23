import json, secrets
from db import cursor, conn

tokens = {}

def register(handler, data):
    user_id = data.get("user_id")
    password = data.get("password")

    if not user_id or not password:
        handler.set_headers(400)
        handler.wfile.write(json.dumps({"error": "user_id and password are required"}).encode())
        return

    cursor.execute(
        "INSERT INTO users (user_id, password) VALUES (%s, %s)",
        (user_id, password)
    )
    conn.commit()

    handler.set_headers(201)
    handler.wfile.write(b'{"message":"User created"}')

def login(handler, data):
    user_id = data.get("user_id")
    password = data.get("password")

    cursor.execute(
        "SELECT id FROM users WHERE user_id=%s AND password=%s",
        (user_id, password)
    )

    user = cursor.fetchone()

    if user:
        token = secrets.token_hex(8)
        tokens[token] = user[0]
        handler.set_headers()
        handler.wfile.write(json.dumps({"token": token}).encode())
    else:
        handler.set_headers(401)
        handler.wfile.write(b'{"error":"Invalid credentials"}')