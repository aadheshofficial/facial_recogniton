import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        roll_number TEXT NOT NULL UNIQUE
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        date DATE NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(id)
    )
''')
conn.commit()
cursor.close()
conn.close()

def insert_student(name, roll_number):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO students (name, roll_number) VALUES (?, ?)", (name, roll_number))
        conn.commit()
        print(f"Student '{name}' with roll number '{roll_number}' inserted successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: Student with roll number '{roll_number}' already exists.")

    cursor.close()
    conn.close()


# insert_student('aadhesh', '1')
# insert_student("aravind",'2')
# insert_student("erai",'3')


