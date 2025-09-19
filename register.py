import cv2
import os
import time

# Create the 'images' directory if it doesn't exist
if not os.path.exists('images'):
    os.makedirs('images')

# Get the name of the person from the user
name = input("Enter the name of the person: ")

# Initialize the webcam
cap = cv2.VideoCapture(0)

# We can add a short delay to give the camera time to start up
time.sleep(2)

print("Starting video capture. Look at the camera. Press 'q' to take a photo.")

# Create a loop to continuously capture frames
while True:
    # Read a frame from the video stream
    ret, frame = cap.read()
    
    # Check if a valid frame was read
    if not ret:
        print("Failed to capture a valid frame. Check your camera.")
        break
        
    # Display the live video feed
    cv2.imshow('Registration - Press Q to save image', frame)
    
    # Wait for the 'q' key to be pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Save the captured frame (image)
        file_path = f"images/{name}.jpg"
        cv2.imwrite(file_path, frame)
        print(f"Image saved successfully as {file_path}")
        break # Exit the loop after saving
        
# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()