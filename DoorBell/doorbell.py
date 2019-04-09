#import grovepi
#from picamera import PiCamera
from time import sleep

def captureVisitor():
    #camera = PiCamera()
    #camera.capture('/home/pi/Desktop/visitor.jpg)
    from TempSensor.PushBulletHelper import push_image
    file = 'User.1.1.jpg'
    push_image("visitor.png", file)
