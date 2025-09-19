import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import time

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

# --- Step 2: Attendance Marking Function ---
def mark_attendance(name):
    with open('attendance/attendance.csv', 'a+') as f:
        f.seek(0)
        data_list = f.readlines()
        name_list = []
        for line in data_list:
            entry = line.split(',')
            name_list.append(entry[0])
        
        if name not in name_list:
            now = datetime.now()
            dt_string = now.strftime('%H:%M:%S')
            f.write(f'\n{name},{dt_string}')
            print(f"Attendance recorded for: {name}")

# --- Step 3: Real-Time Face Recognition with Start/Stop ---
cap = cv2.VideoCapture(0)
time.sleep(2)
if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

is_recording = False
match_threshold = 0.6

print("Press 'S' to START attendance recording.")
print("Press 'Q' to QUIT the program.")

while True:
    success, img = cap.read()
    if not success:
        print("Error: Failed to capture frame from webcam. Exiting...")
        break

    img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)
    
    faces_current_frame = face_recognition.face_locations(img_s)
    encodes_current_frame = face_recognition.face_encodings(img_s, faces_current_frame)
    
    for encode_face, face_loc in zip(encodes_current_frame, faces_current_frame):
        if len(known_encodings) > 0:
            matches = face_recognition.compare_faces(known_encodings, encode_face)
            face_dist = face_recognition.face_distance(known_encodings, encode_face)
            
            match_index = np.argmin(face_dist)
            
            if matches[match_index] and face_dist[match_index] < match_threshold:
                name = class_names[match_index].upper()
                
                y1, x2, y2, x1 = face_loc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                
                if is_recording:
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

    cv2.imshow('Face Attendance System', img)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('s'):
        is_recording = True
        print("Attendance recording started!")
        
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()