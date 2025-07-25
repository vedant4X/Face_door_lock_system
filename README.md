
# 🔐 Face Recognition Door Lock System

This project integrates **face recognition** using Python (OpenCV) with **Arduino** to create a smart **face-based door lock**. The system detects and recognizes a face via webcam and triggers the Arduino to unlock or lock the door via serial communication.

---

## 🧰 Components Used

### 📦 Hardware
- Arduino Uno
- Servo motor (for door lock control)
- USB cable (for Arduino connection)
- Wires & Breadboard
- Power source (if required)

### 💻 Software
- Python 3.x
- OpenCV (`opencv-contrib-python`)
- PySerial
- Pyttsx3 (for voice feedback)
- Arduino IDE

---

## 📂 Project Structure

```

face-door-lock/
- doorlock.py         # Main face recognition + Arduino control script
- facedata.py         # Script to capture and store face data
- door.ino            # Arduino sketch to control servo motor
- /image/             # Directory containing face image dataset
- README.md           # Project documentation (this file)

````

---

## 🚀 How It Works

1. **Face Data Collection**:
   - Run `facedata.py`
   - Captures grayscale images of the user's face via webcam.
   - Stores up to 500 face images in the `/image` folder.
   - Press `Enter` to stop early if needed.

2. **Face Recognition & Door Operation**:
   - Run `doorlock.py`
   - Detects faces using Haar Cascades and identifies them using LBPH (Local Binary Pattern Histogram).
   - If face is recognized with over 83% confidence:
     - Sends `a` to Arduino to unlock the door (servo motor rotates).
     - After 5 seconds, sends `b` to lock the door again.
     - Gives voice confirmation using Pyttsx3.

3. **Arduino Sketch**:
   - `door.ino` reads serial input.
   - On receiving `a`, opens the door (servo rotates).
   - On receiving `b`, closes the door (servo returns to lock position).

---

## 🔧 Setup Instructions

### ✅ Python Requirements
Install dependencies using:
```bash
pip install opencv-contrib-python pyserial pyttsx3
````

### ✅ Face Dataset Path

Update the image dataset path in both `doorlock.py` and `facedata.py` if needed:

```python
data_path = r'C:\Users\Vedan\python\image'
```

### ✅ Arduino Setup

* Open `door.ino` in Arduino IDE.
* Upload to Arduino Uno.
* Make sure the correct port (e.g., COM9) is used in `doorlock.py`:

```python
ard = serial.Serial('COM9', 9600, timeout=2)
```

---

## 💬 Voice Feedback

The system provides speech responses such as:

* ✅ “Face recognition complete. It matches the database. Welcome, sir. The door is opening for 5 seconds.”
* ❌ “Face not found. Please try again.”
* ❌ “Face does not match. Please try again.”
* ✅ “Door was opened successfully.”

---

## 🧠 Logic Summary

* System stops if:

  * 10 successful recognitions (`x == 10`)
  * 30 failed recognitions (`c == 30`)
  * 20 frames with no face found (`d == 20`)
* On success (`x >= 5`), door unlocks.

---

## 📸 Sample Output

* Console:
  `Training complete.`
  `Confidence: 92%`

* Webcam Feed:

  * Green rectangle around detected face
  * Text: `"Unlocked"` or `"Locked"`

---

## ⚠️ Troubleshooting

* If OpenCV shows face module error:

  ```bash
  pip install opencv-contrib-python
  ```
* If serial error occurs:

  * Check if Arduino is connected and the port matches.
  * Close other apps using the COM port.

---

## 📌 To-Do / Future Improvements

* Store face embeddings instead of raw grayscale images
* Add GUI for dataset creation
* Enable logging (e.g., timestamp of door open)
* Use RFID or PIN as backup access method

---

## 👨‍💻 Author

**Vedant Jadhav**
This is a hands-on learning project combining computer vision, embedded systems, and Python programming.
Feel free to fork or contribute!

---

## 📄 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute it for personal or educational purposes.

---

Happy Coding! ☕🔐


