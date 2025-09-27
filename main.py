#import various libraries
import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import time
import sqlite3
import pandas as pd
from scipy.spatial import distance as dist

# --- Step 1: Load and Encode Known Faces ---
path = 'images'
images = []
class_names = []
my_list = os.listdir(path)

for cl in my_list:
    if cl.endswith(('.jpg', '.jpeg', '.png')):
        current_img = cv2.imread(f'{path}/{cl}')
        if current_img is not None:
            images.append(current_img)
            class_names.append(os.path.splitext(cl)[0])
        else:
            print(f"Warning: Could not read image file {cl}. Skipping...")

def find_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list

print("Encoding registered faces...")
if images:
    known_encodings = find_encodings(images)
    print("Encoding complete.")
else:
    print("No images found to encode. Please add a face image to the 'images' folder.")
    known_encodings = []

# --- Step 2: Attendance Marking Function with Database ---
def mark_attendance(name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            PRIMARY KEY (name)
        );
    ''')
    now = datetime.now()
    dt_string = now.strftime('%Y-%m-%d %H:%M:%S')
    try:
        cursor.execute("SELECT * FROM attendance WHERE name = ?;", (name,))
        existing_record = cursor.fetchone()
        if existing_record is None:
            cursor.execute("INSERT INTO attendance (name, timestamp) VALUES (?, ?);", (name, dt_string))
            conn.commit()
            print(f"Attendance recorded for: {name}")
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.close()

# --- New Function: Generate Attendance Report ---
def generate_attendance_report():
    try:
        conn = sqlite3.connect('attendance.db')
        df = pd.read_sql_query("SELECT * FROM attendance;", conn)
        
        if df.empty:
            print("\n--- Attendance Report ---")
            print("No attendance records found.")
            print("-" * 25)
        else:
            print("\n--- Attendance Report ---")
            print(df.to_string(index=False))
            print("-" * 25)

    except sqlite3.Error as e:
        print(f"\nDatabase error: {e}")
    finally:
        if conn:
            conn.close()

# --- NEW: Liveness Detection Variables and Function ---
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3
COUNTER = 0

def eye_aspect_ratio(eye):
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# --- Step 3: Real-Time Face Recognition with Start/Stop (Updated) ---
cap = cv2.VideoCapture(0)
time.sleep(2)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

is_recording = False
match_threshold = 0.6

print("Press 'S' to START attendance recording.")
print("Press 'Q' to QUIT the program.")
print("Press 'R' for Report.")
print("Liveness detection is ON.")

while True:
    success, img = cap.read()
    if not success:
        print("Error: Failed to capture frame from webcam. Exiting...")
        break
    
    h, w, _ = img.shape
    img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)
    
    faces_current_frame = face_recognition.face_locations(img_s)
    encodes_current_frame = face_recognition.face_encodings(img_s, faces_current_frame)
    face_landmarks = face_recognition.face_landmarks(img_s)
    
    # NEW Liveness check logic starts here
    blinked = False
    for facial_landmarks in face_landmarks:
        left_eye = facial_landmarks['left_eye']
        right_eye = facial_landmarks['right_eye']
        
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        
        ear = (left_ear + right_ear) / 2.0
        
        if ear < EYE_AR_THRESH:
            COUNTER += 1
        else:
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                blinked = True
            COUNTER = 0
    # Liveness check logic ends here

    for encode_face, face_loc in zip(encodes_current_frame, faces_current_frame):
        if len(known_encodings) > 0:
            matches = face_recognition.compare_faces(known_encodings, encode_face)
            face_dist = face_recognition.face_distance(known_encodings, encode_face)
            match_index = np.argmin(face_dist)
            
            if matches[match_index] and face_dist[match_index] < match_threshold:
                name = class_names[match_index].upper()
                y1, x2, y2, x1 = face_loc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                
                color = (0, 255, 0)
                if not blinked:
                    color = (0, 165, 255)
                    cv2.putText(img, "BLINK TO CONFIRM", (x1, y1 - 15), cv2.FONT_HERSHEY_COMPLEX, 0.6, color, 1)

                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                
                if is_recording and blinked:
                    mark_attendance(name)
            else:
                name = "UNKNOWN"
                y1, x2, y2, x1 = face_loc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        else:
            name = "UNKNOWN"
            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            
    status = "Recording: ON" if is_recording else "Recording: OFF"
    cv2.putText(img, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(img, "Press 'S' to Start", (w - 250, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(img, "Press 'Q' to Quit", (w - 250, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(img, "Press 'R' for Report", (w - 250, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    cv2.imshow('Face Attendance System', img)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('s'):
        is_recording = True
        print("Attendance recording started!")
        
    if key == ord('q'):
        break
        
    if key == ord('r'):
        generate_attendance_report()

cap.release()
cv2.destroyAllWindows()