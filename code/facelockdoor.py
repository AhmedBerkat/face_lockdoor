import cv2
import numpy as np
from os import listdir
from os.path import isfile, join
import serial
import time
import pyttsx3

q = 1
x = 0
c = 0
m = 0
d = 0
# Load trained model during the first iteration
while q <= 2:
    data_path = 'C:\\Users\\pc\\Desktop\\image'
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    Training_data, Labels = [], []

    for i, file in enumerate(onlyfiles):
        image_path = join(data_path, onlyfiles[i])
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Check if the image is not empty
        if images is not None:
            Training_data.append(np.asarray(images, dtype=np.uint8))
            Labels.append(i)

    Labels = np.asarray(Labels, dtype=np.int32)

    # Create LBPH face recognizer
    model = cv2.face.LBPHFaceRecognizer_create()

    # Train the model
    try:
        model.train(np.asarray(Training_data), np.asarray(Labels))
        print("Training complete")
    except Exception as e:
        print('Error during training:', e)

    q += 1

# Initialize face classifier
face_classifier = cv2.CascadeClassifier('C:/Users/pc/Downloads/FACELOCKING-DOOR-USING-PYTHON-AND-ARDUINO-PROGRAMING-master/FACELOCKING-DOOR-USING-PYTHON-AND-ARDUINO-PROGRAMING-master/requirements/haarcascade_frontalface_default.xml')

# Text-to-speech engine setup
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 140)
engine.setProperty("volume", 1000)

def face_detector(img, size=0.5):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Adjust parameters for better face detection
    faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Print debug information
    print('Number of faces detected:', len(faces))

    if len(faces) == 0:
        return img, None

    # Use the first detected face
    (x, y, w, h) = faces[0]
    roi = img[y:y+h, x:x+w]

    # Check if the face region is not empty
    if roi.size == 0:
        return img, None

    roi = cv2.resize(roi, (200, 200))

    return img, roi


# Capture video from the camera
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    # Break the loop if the frame is empty
    if not ret or frame is None:
        print('Error: Empty frame')
        break

    image, face = face_detector(frame)

    try:
        # Check if the face is not empty
        if face is not None:
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            result = model.predict(face)
            if result[1] < 500:
                confidence = int((1 - (result[1]) / 300) * 100)
                display_string = str(confidence)
                cv2.putText(image, display_string, (100, 120), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 255, 0))

            if confidence >= 83:
                cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 255, 255))
                cv2.imshow('Face', image)
                x += 1
            else:
                cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 255, 255))
                cv2.imshow('Face', image)
                c += 1
        else:
            print('Error: No face detected')
    except Exception as e:
        print('Error:', e)
        cv2.putText(image, "Face not found", (250, 450), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 255, 255))
        cv2.imshow('Face', image)
        d += 1
        pass

    # Break the loop if Enter key is pressed or conditions are met
    if cv2.waitKey(1) == 13 or x == 10 or c == 30 or d == 20:
        break

# Release the camera
cap.release()
cv2.destroyAllWindows()

# Check conditions and take actions
if x >= 5:
    m = 1
    ard = serial.Serial('com3', 9600)
    time.sleep(2)
    var = 'a'
    c = var.encode()
    speak("Face recognition complete. Welcome, sir. Door is opening for 5 seconds.")
    ard.write(c)
    time.sleep(4)
elif c == 30:
    speak("Face is not matching. Please try again.")
elif d == 20:
    speak("Face is not found. Please try again.")

if m == 1:
    speak("Door is closing")