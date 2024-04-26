import cv2
import numpy as np

# Load the Haar cascade classifier
face_classifier = cv2.CascadeClassifier('C:/Users/pc/Downloads/FACELOCKING-DOOR-USING-PYTHON-AND-ARDUINO-PROGRAMING-master/FACELOCKING-DOOR-USING-PYTHON-AND-ARDUINO-PROGRAMING-master/requirements/haarcascade_frontalface_default.xml')

def face_extractor(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Adjust parameters for better face detection
    faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)
    
    # Initialize cropped_face as None
    cropped_face = None
    
    # Print detected faces coordinates for debugging
    for (x, y, w, h) in faces:
        print(f"Detected face at coordinates: x={x}, y={y}, w={w}, h={h}")
        cropped_face = img[y:y+h, x:x+w]
    
    return cropped_face


cap = cv2.VideoCapture(0)
count = 0

while True:
    ret, frame = cap.read()
    
    # Display the camera feed for debugging
    cv2.imshow("Camera Feed", frame)
    
    cropped_face = face_extractor(frame)
    
    if cropped_face is not None:
        count += 1
        face = cv2.resize(cropped_face, (200, 200))
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

        # Use the updated file path
        file_name_path = 'C:\\Users\\pc\\Desktop\\image\\image' + str(count) + '.jpg'
        cv2.imwrite(file_name_path, face)

        cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("face cropper", face)
    else:
        print('Face not found')
    
    if cv2.waitKey(1) == 13 or count == 500:
        break

cap.release()
cv2.destroyAllWindows()
print("Collecting samples complete")