import json
from storage import students, tokens

def add_student(handler, data): 
    token = handler.headers.get("Authorization")

    if token not in tokens:
        handler.set_headers(401)
        handler.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
        return

    name = data.get("name")
    age = data.get("age")
    course = data.get("course")

    if not name or not age or not course:
        handler.set_headers(400)
        handler.wfile.write(json.dumps({"error": "All fields required"}).encode())
        return

    student_id = len(students) + 1
    students.append({
        "id": student_id,
        "name": name,
        "age": age,
        "course": course
    })

    handler.set_headers(201)
    handler.wfile.write(json.dumps({"message": "Student added"}).encode())

def list_students(handler):
    token = handler.headers.get("Authorization")

    if token not in tokens:
        handler.set_headers(401)
        handler.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
        return

    handler.set_headers()
    handler.wfile.write(json.dumps(students).encode())
# -------- UPDATE STUDENT --------
def update_student(handler, data):
    token = handler.headers.get("Authorization")

    if token not in tokens:
        handler.set_headers(401)
        handler.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
        return

    student_id = data.get("id")

    for student in students:
        if student["id"] == student_id:
            student["name"] = data.get("name", student["name"])
            student["age"] = data.get("age", student["age"])
            student["course"] = data.get("course", student["course"])

            handler.set_headers()
            handler.wfile.write(json.dumps({"message": "Student updated"}).encode())
            return

    handler.set_headers(404)
    handler.wfile.write(json.dumps({"error": "Student not found"}).encode())


# -------- DELETE STUDENT --------
def delete_student(handler, data):
    token = handler.headers.get("Authorization")

    if token not in tokens:
        handler.set_headers(401)
        handler.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
        return

    student_id = data.get("id")

    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            handler.set_headers()
            handler.wfile.write(json.dumps({"message": "Student deleted"}).encode())
            return

    handler.set_headers(404)
    handler.wfile.write(json.dumps({"error": "Student not found"}).encode())