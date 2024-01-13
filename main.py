import cv2
import numpy as np
import sqlite3
from tensorflow.keras.models import load_model
from datetime import date

#created model name
model = load_model('facial_recognition_model.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

def mark_attendance(student_roll_number, attendance_date, attendance_status):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM students WHERE roll_number=?", (student_roll_number,))
    student_id = cursor.fetchone()

    if student_id is not None:
        student_id = student_id[0]

        cursor.execute('''
            SELECT id FROM attendance
            WHERE student_id=? AND date=?
        ''', (student_id, attendance_date))
        existing_record = cursor.fetchone()

        if existing_record is None:
            cursor.execute('''
                INSERT OR REPLACE INTO attendance (student_id, date, status)
                VALUES (?, ?, ?)
            ''', (student_id, attendance_date, attendance_status))

            conn.commit()

            print(f"Attendance marked for {student_roll_number} on {attendance_date}: {attendance_status}")
        else:
            print(f"Attendance already marked for {student_roll_number} on {attendance_date}.")
    else:
        print(f"Student with roll number {student_roll_number} not found.")

    cursor.close()
    conn.close()

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        face_roi = frame[y:y+h, x:x+w]
        face_img = cv2.resize(face_roi, (224, 224))
        face_img = np.expand_dims(face_img, axis=0)
        face_img = face_img / 255.0

        predictions = model.predict(face_img)
        predicted_class = np.argmax(predictions)

        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, f'Class: {predicted_class}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        print("predicted class:", predicted_class)
        if predicted_class != 0:
            today_date = date.today().strftime("%Y-%m-%d")
            mark_attendance(str(predicted_class), today_date, 'Present')
            print("Attendance marked for", predicted_class)

    cv2.imshow('Facial Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
