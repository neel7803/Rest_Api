import json, secrets, string
from storage import users, tokens

def generate_short_token(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def register(handler, data):
    user_id = data.get("user_id")
    password = data.get("password")

    if not user_id or not password:
        handler.set_headers(400)
        handler.wfile.write(json.dumps({"error": "user_id and password required"}).encode())
        return

    if user_id in users:
        handler.set_headers(400)
        handler.wfile.write(json.dumps({"error": "User already exists"}).encode())
    else:
        users[user_id] = password
        handler.set_headers(201)
        handler.wfile.write(json.dumps({"message": "User created"}).encode())

def login(handler, data):
    user_id = data.get("user_id")
    password = data.get("password")

    if users.get(user_id) == password:
        token = generate_short_token()
        tokens[token] = user_id
        handler.set_headers()
        handler.wfile.write(json.dumps({"token": token}).encode())
    else:
        handler.set_headers(401)
        handler.wfile.write(json.dumps({"error": "Invalid credentials"}).encode())
