''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''

import cv2
import numpy as np
import os
import pyrebase
from FacialRecognition.lock_module import *

config = {
    "apiKey": "AIzaSyCd8ZWijyCfiyWvZPZ9BZ4Ajc5ynGBWVek",
    "authDomain": "iotsmarthome-93fb2.firebaseapp.com",
    "databaseURL": "https://iotsmarthome-93fb2.firebaseio.com",
    "projectId": "iotsmarthome-93fb2",
    "storageBucket": "iotsmarthome-93fb2.appspot.com",
    "messagingSenderId": "1042090494244"
}

try:
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password("testing2822@gmail.com", "ncct2822")
    db = firebase.database()
except Exception as pyrebase_exception:
    print(pyrebase_exception)

def faceRecog():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);

    font = cv2.FONT_HERSHEY_SIMPLEX

    # indicate id counter
    id = 0

    # names related to ids: example ==> Marcelo: id=1,  etc
    names = ['Nicholas', 'Joyce', 'Brandon', 'Eric']

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video widht
    cam.set(4, 480)  # set video height

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:

        ret, img = cam.read()
        # img = cv2.flip(img, -1) # Flip vertically

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])

            # Check if confidence is less them 100 ==> "0" is perfect match
            if (confidence < 100):
                id = names[id]
                similarity = 100 - confidence
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                similarity = 100 - confidence
                confidence = "  {0}%".format(round(100 - confidence))

            if (similarity >= 50):
                print("Verified")
                print(similarity)
                unlock()
                break
            else:
                From
                PushBulletHelper
                import push_image

                push_image("intruder.png", img)

            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('camera', img)

        k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break

    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
