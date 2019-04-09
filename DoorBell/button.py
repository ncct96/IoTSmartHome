import grovepi

pinbutton = 3

#grovepi.pinMode(button,"INPUT")

while True:
    try:
        status = digitalRead(button)
        if status:
            print("Unlock")
        else:
            print("Lock")
    except IOError:
        print("Error")