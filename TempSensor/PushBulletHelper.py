import websocket
from pushbullet import *
from TempSensor.LineChartPlotter import get_data
from TempSensor.TemperatureModule import *
from TempSensor.DeviceManager import *
#from FacialRecognition.face_dataset import *

#CP's Token
#token = "o.TYslgAbhFtbyO4AjFeOpOHTaI7Pz0G3Q"

#Nicholas's Token
token = "o.af4UdQ8rcjnFmJlYPdFCWqahaQt8418E"
websocket_conn = "wss://stream.pushbullet.com/websocket/" + token
websocket_query = "https://api.pushbullet.com/v2/pushes?limit=1"
pb = PushBullet(token)


def push_message(title, message):
    try:
        push = pb.push_note(title, message)
    except Exception as exception:
        print(exception)


def push_image(file_name, file_path):
    try:
        print("Pushing file")
        with open(file_path, "rb") as pic:
            file_data = pb.upload_file(pic, file_name)
        push = pb.push_file(**file_data)
    except Exception as exception:
        print(exception)


def reply_listener():
    ws = websocket.create_connection(websocket_conn)
    print("Listener Running")
    while True:
        try:
            result = ws.recv()
            if result == '{"type": "tickle", "subtype": "push"}':
                command = str(pb.get_pushes()).split("body")[1]
                command = command[4: -3]
                command = command.split("'")[0]
                print(command)
                if command == "!temp" or command == "!temperature":
                    # GET TEMPERATURE
                    thread = threading.Thread(target=temperature_monitor, args=(True,))
                    thread.start()
                elif command == "!lock -status" or command == "!lck -status":
                    # GET LOCK STATUS
                    thread = threading.Thread(target=None)
                    thread.start()
                elif command == "!light -status":
                    # GET LIGHT STATUS
                    thread = threading.Thread(target=None)
                    thread.start()
                elif command == "!fan -on":
                    # TURN ON FAN
                    thread = threading.Thread(target=fan_control(True))
                    thread.start()
                elif command == "!fan -off":
                    # TURN OFF FAN
                    thread = threading.Thread(target=fan_control(False))
                    thread.start()
                elif command == "!light -on":
                    # TURN ON LIGHT
                    thread = threading.Thread(target=light_control(True))
                    thread.start()
                elif command == "!light -off":
                    # TURN OFF LIGHT
                    thread = threading.Thread(target=light_control(False))
                    thread.start()
                elif command == "!lock -on" or command == "!lock":
                    # ENABLE LOCK
                    thread = threading.Thread(target=lock_door(True))
                    thread.start()
                elif command == "!lock -off":
                    # DISABLE LOCK
                    thread = threading.Thread(target=lock_door(False))
                    thread.start()
                elif command == "!a" or command == "!alarm" or command == "!alert":
                    # SOUND ALARM
                    thread = threading.Thread(target=None)
                    thread.start()
                elif command == "!temp -graph":
                    # SEND TEMPERATURE GRAPH
                    thread = threading.Thread(target=get_data)
                    thread.start()
                #elif command == "!reg -user" or command == "!reg":
                    #thread = threading.Thread(target=regFace)
                    #thread.start()
                else:
                    print("Invalid command")
            else:
                print("Listening...")
        except Exception as exception:
            print(exception)


def start_reply_listener():
    reply_listener_thread = threading.Thread(target=reply_listener)
    reply_listener_thread.start()


# start_reply_listener()
