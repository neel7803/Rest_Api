import psycopg2

conn = psycopg2.connect(
    dbname="student_project_API",
    user="postgres",
    password="neel7803",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()