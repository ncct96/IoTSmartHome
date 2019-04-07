from grovepi import *

relay_pin =5

pinMode(relay_pin, "OUTPUT")

def lock():
    try:
        digitalWrite(relay_pin, 0)
    except TypeError:
        print("TypeError")
    except IOError:
        print("IOError")

def unlock():
    try:
        digitalWrite(relay_pin, 1)
    except TypeError:
        print("TypeError")
    except IOError:
        print("IOError")