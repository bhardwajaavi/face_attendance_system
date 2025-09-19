import sqlite3

def view_records():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    
    # Select all rows from the attendance table
    cursor.execute("SELECT * FROM attendance;")
    
    # Fetch all the results
    records = cursor.fetchall()
    
    if records:
        print("Attendance Records:")
        print("-" * 30)
        print("Name\t\tTimestamp")
        print("-" * 30)
        for record in records:
            print(f"{record[0]}\t\t{record[1]}")
    else:
        print("No attendance records found.")

    conn.close()

if __name__ == "__main__":
    view_records()