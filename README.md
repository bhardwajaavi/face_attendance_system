
Face Attendance System


A real-time biometric attendance system built with Python. This project uses **Computer Vision** to recognize faces and includes **Liveness Detection** (blink verification) to prevent spoofing using photos or videos. Attendance is automatically logged to both an **SQLite Database** and an **Excel sheet** for easy reporting.

---

## 🚀 Key Features

* **Real-Time Face Recognition:** Identifies registered users instantly using the `face_recognition` library.
* **👁️ Liveness Detection:** Prevents security breaches by requiring the user to **blink** to confirm they are a real person (not a static photo).
* **Dual-Storage System:**
    * **SQLite:** Robust backend storage for historical data.
    * **Excel Automation:** Auto-syncs daily logs to `.xlsx` for easy sharing with HR/Admin.
* **Smart Duplicate Prevention:** Logic ensures a user is only marked present once per day to prevent data clutter.
* **Interactive GUI:** Visual feedback with status indicators, bounding boxes, and instruction overlays.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Core Libraries:**
    * `face_recognition`: For generating 128-d face encodings.
    * `opencv-python` (cv2): For video capture and image processing.
    * `scipy`: For calculating Euclidean distance (Eye Aspect Ratio).
    * `pandas`: For data manipulation and Excel export.
    * `sqlite3`: For database management.
    * `openpyxl`: Engine for writing to Excel files.

---

## 📂 Project Structure

\`\`\`bash
├── images/               # Stores reference images of registered users
├── main.py               # Main application (Recognition + Liveness + DB/Excel Logic)
├── register.py           # Script to register new users (Capture & Save)
├── view_attendance.py    # Utility to view DB records in terminal
├── attendance.db         # SQLite Database (Auto-generated)
├── Attendance.xlsx       # Excel Report (Auto-generated)
└── README.md             # Project Documentation
\`\`\`

---

## ⚙️ Installation & Setup

1.  **Clone the repository**
    \`\`\`bash
    git clone https://github.com/yourusername/face-attendance-system.git
    cd face-attendance-system
    \`\`\`

2.  **Install Dependencies**
    \`\`\`bash
    pip install opencv-python face-recognition pandas scipy openpyxl numpy
    \`\`\`
    *(Note: CMake and Dlib may need to be installed separately depending on your OS).*

---

## 🖥️ How to Use

### Step 1: Register a New User
Run the registration script to capture a user's face.
\`\`\`bash
python register.py
\`\`\`
* Enter the user's name.
* The camera will open. Press **'Q'** to capture and save the face data.

### Step 2: Start the Attendance System
Run the main system.
\`\`\`bash
python main.py
\`\`\`
* **Press 'S'**: Start the recording mode.
* **Verification**: Look at the camera. The system will prompt you to **"BLINK TO CONFIRM"**.
* **Success**: Once the blink is detected, the name turns Green, and data is saved to `attendance.db` and `Attendance.xlsx`.
* **Press 'R'**: View a quick attendance report in the console.
* **Press 'Q'**: Quit the application.

---

## 📊 Sample Output (Excel)

The system automatically generates an `Attendance.xlsx` file:

| Name | Timestamp |
| :--- | :--- |
| AAVI BHARDWAJ | 2025-11-28 10:30:45 |
| NAMIT  | 2025-11-28 10:32:12 |

---

## 🔮 Future Scope
* **Web Dashboard:** Integrating with Flask/Django to view attendance logs in a browser.
* **Cloud Sync:** Uploading the database to AWS/Firebase for remote access.
* **Email Alerts:** Automatically emailing the Excel sheet to HR at the end of the day.

---

## 👤 Author

**Aavi Bhardwaj**
* **Role:** MCA Student & Python Developer
* **Interest:** Computer Vision, Full-Stack Development
* **LinkedIn:* https://www.linkedin.com/in/aavi-b-abb205120/
