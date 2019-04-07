''''
Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
	==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
	==> Each face will have a unique numeric integer ID as 1, 2, 3, etc                       

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18    

'''

import cv2
import os
import pyrebase
from FacialRecognition.face_training import *

config = {
    "apiKey": "AIzaSyD4kiF1wDR89lWdSReLGdrblEVjiw794d8",
    "authDomain": "smarthome-f5af7.firebaseapp.com",
    "databaseURL": "https://smarthome-f5af7.firebaseio.com",
    "projectId": "smarthome-f5af7",
    "storageBucket": "smarthome-f5af7.appspot.com",
    "messagingSenderId": "223998686071"
}

try:
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password("chiupeeng@gmail.com", "ChiuPeeng98")
    db = firebase.database()
except Exception as pyrebase_exception:
    print(pyrebase_exception)

def regFace():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height

    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #face_detector = cv2.CascadeClassifier('D:\\Users\\Nicholas\\PycharmProjects\\IoTSmartHome\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')

    # For each person, enter one numeric face id
    face_id = input('\n Enter user id end press <return> (ONLY NUMBER) ==>  ')
    name = input('\n Enter your name ==>')
    #face_id = id

    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    # Initialize individual sampling face count
    count = 0

    while(True):

        ret, img = cam.read()
        # img = cv2.flip(img, -1) # flip video image vertically
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = np.array(gray, dtype='uint8')
        faces = face_detector.detectMultiScale(gray, 1.5, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])
            cv2.imshow('image', img)

        k = cv2.waitKey(100) & 0xff  # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 30:  # Take 30 face sample and stop video
            print("\n [INFO] Uploading your details")
            data = {"name" : name}
            db.child("users").child(id).set(data, user['idToken'])
            break


    # Do a bit of cleanup
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    trainFace()
    cv2.destroyAllWindows()
