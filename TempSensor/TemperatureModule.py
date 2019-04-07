import datetime
import pyrebase
import threading
from math import *
from time import sleep

HTM_Port = 0
HTM_Type = 0
LED_Port = 0
error = 0

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
    print("Firebase exception: " + str(pyrebase_exception))


def temperature_monitor(is_command):
    from PushBulletHelper import push_message
    tries = 0
    temperature = 0
    rel_humidity = 0
    heat_index = 0

    while tries < 3:
        try:
            tries += 1
            # START DEBUG METHODS
            temperature = 30
            rel_humidity = 55
            # END DEBUG METHODS

            # START DEPLOYMENT METHODS
            # [temperature, rel_humidity] = dht(HTM_Port, HTM_Type)
            # END DEPLOYMENT METHODS

            # CHECK FOR ISNAN
            if isnan(temperature) is True or isnan(rel_humidity) is True:
                raise TypeError("NAN ERROR")

            # CONVERT CELSIUS TO FAHRENHEIT
            temperature = (temperature + 40) * 9 / 5 - 40

            # HEAT INDEX FORMULA
            heat_index = -42.379 + 2.04901523 * temperature + 10.14333127 * rel_humidity - 0.22475541 * temperature * \
                rel_humidity - 0.00683783 * temperature * temperature - 0.05481717 * rel_humidity * \
                rel_humidity + 0.00122874 * temperature * temperature * rel_humidity + 0.00085282 * \
                temperature * rel_humidity * rel_humidity - 0.00000199 * temperature * temperature * \
                rel_humidity * rel_humidity

            # CONSOLE PRINT
            print("Fahrenheit: " + str(temperature))
            print("Relative Humidity: " + str(rel_humidity) + "%")
            print("Heat Index: " + str(ceil(heat_index)))

            # ADJUSTMENT
            if rel_humidity < 13 and 80 < temperature < 112:
                heat_index -= [(13 - rel_humidity) / 4] * int(sqrt((17 - abs(temperature - 95)) / 17))
            elif rel_humidity > 85 and 80 < temperature < 87:
                heat_index += [(rel_humidity - 85) / 10] * int((87 - temperature) / 5)

            # CONVERT FAHRENHEIT BACK TO CELSIUS
            heat_index = ceil((heat_index + 40) * 5 / 9 - 40)

            # ACTIONS
            if heat_index < 89:
                # Normal temperature
                if is_command:
                    push_message("Current Temperature", str(heat_index) + "C, Normal")
            elif heat_index < 103:
                # Uncomfortable temperature
                if is_command:
                    push_message("Current Temperature", str(heat_index) + "C, Uncomfortable")
            elif heat_index < 124:
                # Dangerous temperature
                if is_command:
                    push_message("Current Temperature", str(heat_index) + "C, Dangerous")
            else:
                # Probably dead
                if is_command:
                    push_message("Current Temperature", str(heat_index) + "C, Your house might be on fire")

            break
        except Exception as exception:
            print("Temperature exception: " + str(exception))
            sleep(5)
    if tries >= 3:
        # STOP AFTER 3 TRIES
        print("Unable to fetch temperature")
        push_message("Uh oh", "We are unable to retrieve your house's temperature, please try again later")
    else:
        # STORE INTO DATABASE IF IS SCHEDULED TASK
        if not is_command:
            data = {
                "temperature": temperature,
                "humidity": rel_humidity,
                "heatIndex": heat_index
            }
            today = datetime.datetime.now()

            if today.hour < 10:
                now_hour = "0" + str(today.hour) + "00"
            else:
                now_hour = str(today.hour) + "00"

            db.child("Temperature").child(today.strftime("%Y-%m-%d")).child(now_hour).set(data, user['idToken'])


def temp_scheduler():
    while True:
        try:
            t = threading.Timer(5.0, temperature_monitor, [False])
            t.daemon = True
            t.start()
            sleep(5)
        except Exception as scheduler_exception:
            print("Task exception: " + str(scheduler_exception))
