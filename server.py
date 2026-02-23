from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from auth import register, login
from students import add_student, list_students, update_student, delete_student

class MyServer(BaseHTTPRequestHandler):

    def set_headers(self, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(length).decode()

    def do_POST(self):
        try:
            raw = self.read_body()
            if raw:
               data = json.loads(raw)
            else:
              data = {}
        except:
            self.set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode())
            return

        if self.path == "/register":
            register(self, data)

        elif self.path == "/login":
            login(self, data)

        elif self.path == "/students":
            add_student(self, data)

        else:
            self.set_headers(404)
            self.wfile.write(json.dumps({"error": "Route not found"}).encode())

    def do_GET(self):
        if self.path == "/students":
            list_students(self)
        else:
            self.set_headers(404)
            self.wfile.write(json.dumps({"error": "Route not found"}).encode())
    def do_PUT(self):
        try:
            raw = self.read_body()
            data = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            self.set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode())
            return

        if self.path == "/students":
            update_student(self, data)
        else:
            self.set_headers(404)
            self.wfile.write(json.dumps({"error": "Route not found"}).encode())


    def do_DELETE(self):
        try:
            raw = self.read_body()
            data = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            self.set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode())
            return

        if self.path == "/students":
            delete_student(self, data)
        else:
            self.set_headers(404)
            self.wfile.write(json.dumps({"error": "Route not found"}).encode())


server = HTTPServer(("localhost", 9000), MyServer)
print("Server running at http://localhost:9000")
server.serve_forever()
