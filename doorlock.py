import cv2
import numpy as np
import os
import serial
import time
import pyttsx3

# ✅ Initialize speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty("voice", engine.getProperty('voices')[0].id)
engine.setProperty("rate", 140)
engine.setProperty("volume", 1.0)

def speak(audio):
    """Text-to-Speech function"""
    engine.say(audio)
    engine.runAndWait()

# ✅ Load Haar Cascade Classifier for face detection
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ✅ Set dataset path
data_path = r'C:\Users\Vedan\python\image'

# ✅ Check if dataset directory exists
if not os.path.exists(data_path):
    print(f"Error: Directory '{data_path}' not found!")
    exit()

# ✅ Prepare dataset for training
onlyfiles = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]
Training_data, Labels = [], []

for i, file in enumerate(onlyfiles):
    image_path = os.path.join(data_path, file)
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if images is None:
        print(f"Warning: Could not load {file}. Skipping...")
        continue
    images = cv2.resize(images, (200, 200))
    Training_data.append(np.asarray(images, dtype=np.uint8))
    Labels.append(i)

Labels = np.asarray(Labels, dtype=np.int32)

if len(Training_data) == 0:
    print("Error: No valid training images found!")
    exit()

# ✅ Train the recognizer
try:
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(np.asarray(Training_data, dtype=np.uint8), Labels)
    print("Training complete.")
except AttributeError:
    print("Error: OpenCV is missing 'face' module! Install it using:")
    print("pip install opencv-contrib-python")
    exit()

# ✅ Face detection function
def face_detector(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return img, None

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200, 200))
        return img, roi

    return img, None

# ✅ Initialize counters
x, c, d, m = 0, 0, 0, 0

# ✅ Start video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    image, face = face_detector(frame)

    try:
        if face is not None:
            result = model.predict(face)
            confidence = int((1 - (result[1]) / 300) * 100)
            cv2.putText(image, f"Confidence: {confidence}%", (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if confidence >= 83:
                cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                x += 1
            else:
                cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                c += 1
        else:
            cv2.putText(image, "Face not found", (250, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            d += 1

        cv2.imshow('Face Recognition', image)

    except Exception as e:
        print("Error:", e)
        pass

    # Break conditions
    if cv2.waitKey(1) == 13 or x == 10 or c == 30 or d == 20:
        break

cap.release()
cv2.destroyAllWindows()

# ✅ Serial communication with Arduino
if x >= 5:
    m = 1
    try:
        ard = serial.Serial('COM9', 9600, timeout=2)
        time.sleep(2)  # Wait for connection to establish

        # Send command to open door
        ard.write(b'a')
        speak("Face recognition complete. It matches the database. Welcome, sir. The door is opening for 5 seconds.")
        time.sleep(5)  # Keep door open for 5 seconds

        # Send command to close door
        ard.write(b'b')
        speak("Door is now closing.")

        ard.close()

    except serial.SerialException:
        print("Error: Could not open serial port. Check if Arduino is connected.")

elif c == 30:
    speak("Face does not match. Please try again.")

elif d == 20:
    speak("Face not found. Please try again.")

if m == 1:
    speak("Door was opened successfully.")
