import json
from db import cursor, conn
from auth import tokens

def get_user_from_token(handler):
    """Parses the Authorization header and returns the user_id if the token is valid."""
    auth_header = handler.headers.get("Authorization")
    token = None
    if auth_header:
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = auth_header

    if not token or token not in tokens:
        handler.set_headers(401)
        handler.wfile.write(b'{"error":"Unauthorized"}')
        return None

    return tokens[token]

# -------- ADD STUDENT --------
def add_student(handler, data):
    created_by_id = get_user_from_token(handler)
    if not created_by_id:
        return

    name = data.get("name")
    age = data.get("age")
    course = data.get("course")

    if not all([name, age, course]):
        handler.set_headers(400)
        handler.wfile.write(b'{"error":"Missing required fields: name, age, course"}')
        return

    cursor.execute(
        "INSERT INTO students (name, age, course, created_by_id) VALUES (%s, %s, %s, %s)",
        (name, age, course, created_by_id)
    )
    conn.commit()

    handler.set_headers(201)
    handler.wfile.write(b'{"message":"Student added"}')


# -------- LIST STUDENTS --------
def list_students(handler):
    # The user must be authenticated to list students
    user_id = get_user_from_token(handler)
    if not user_id:
        return

    cursor.execute("SELECT id, name, age, course, created_by_id FROM students WHERE created_by_id=%s", (user_id,))
    rows = cursor.fetchall()

    students = []
    for r in rows:
        students.append({
            "id": r[0],
            "name": r[1],
            "age": r[2],
            "course": r[3],
            "created_by_id": r[4]
        })

    handler.set_headers()
    handler.wfile.write(json.dumps(students).encode())


# -------- UPDATE STUDENT --------
def update_student(handler, data):
    user_id = get_user_from_token(handler)
    if not user_id:
        return

    student_id = data.get("id")
    if not student_id:
        handler.set_headers(400)
        handler.wfile.write(b'{"error":"ID is required"}')
        return

    fields = []
    values = []

    for key in ["name", "age", "course"]:
        if key in data:
            fields.append(f"{key}=%s")
            values.append(data[key])

    if not fields:
        handler.set_headers(400)
        handler.wfile.write(b'{"error":"No fields to update"}')
        return

    values.append(student_id)
    values.append(user_id)  
    sql = f"""
UPDATE students
SET {', '.join(fields)}
WHERE id=%s AND created_by_id=%s
"""
    cursor.execute(sql, values)
    conn.commit()

    handler.set_headers()
    handler.wfile.write(b'{"message":"Student updated"}')


# -------- DELETE STUDENT --------
def delete_student(handler, data):
    user_id = get_user_from_token(handler)
    if not user_id:
        return

    student_id = data.get("id")
    if not student_id:
        handler.set_headers(400)
        handler.wfile.write(b'{"error":"ID is required"}')
        return

    cursor.execute(
        "DELETE FROM students WHERE id=%s AND created_by_id=%s",
        (student_id, user_id)
    )
    conn.commit()

    handler.set_headers()
    handler.wfile.write(b'{"message":"Student deleted"}')