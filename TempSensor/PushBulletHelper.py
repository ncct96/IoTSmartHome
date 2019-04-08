import websocket
import threading
from time import sleep
from LineChartPlotter import get_data
from TemperatureModule import temperature_monitor
from pushbullet import *

# from LineChartPlotter import get_data
# from TemperatureModule import *
# from DeviceManager import *
# from face_dataset import *

# CP's Token
token = "o.8IwCzcxqtCNgHRdgzQUunxxOWwVJ8czN"
# Nicholas's Token
# token = "o.af4UdQ8rcjnFmJlYPdFCWqahaQt8418E"

while True:
    try:
        websocket_conn = "wss://stream.pushbullet.com/websocket/" + token
        websocket_query = "https://api.pushbullet.com/v2/pushes?limit=1"
        pb = PushBullet(token)
        break
    except Exception as conn_exception:
        print("PushBullet initialization exception: " + str(conn_exception))
        sleep(5)


def push_message(title, message):
    try:
        pb.push_note(title, message)
    except Exception as pb_exception:
        print("PushBullet push message exception: " + str(pb_exception))


def push_image(file_name, file_path):
    import pathlib
    try:
        print("Pushing file")
        with open(pathlib.Path(__file__).parent / file_path, "rb") as pic:
            file_data = pb.upload_file(pic, file_name)
        pb.push_file(**file_data)
    except Exception as img_exception:
        print("PushBullet push file exception: " + str(img_exception))


def reply_listener():
    ws = websocket.create_connection(websocket_conn)
    print("Listener Running")
    while True:
        try:
            result = ws.recv()
            print(result)
            if result == '{"type": "tickle", "subtype": "push"}':
                print(pb.get_pushes())
                if "'type': 'note'" not in str(pb.get_pushes()):
                    continue
                if "'title': " in str(pb.get_pushes()):
                    continue

                command = str(pb.get_pushes()).split("body")[1]
                command = command[4: -3]
                command = command.split("'")[0]
                print(command)
                if command == "!temp" or command == "!temperature":
                    # GET TEMPERATURE
                    thread = threading.Thread(target=temperature_monitor, args=(True,))
                    thread.start()
                elif command == "!graph":
                    # SEND TEMPERATURE GRAPH
                    thread = threading.Thread(target=get_data, args=(None,))
                    thread.start()
                elif command.startswith("!graph"):
                    # SEND TEMPERATURE GRAPH (DATE SPECIFIED)
                    try:
                        import datetime
                        date = datetime.datetime.strptime(command[7:], '%d/%m/%Y')
                        thread = threading.Thread(target=get_data, args=(date,))
                        thread.start()
                    except ValueError:
                        push_message("Oops", "Wrong date format")
                elif command == "!reg -user" or command == "!reg":
                    thread = threading.Thread(target="")  # regFace
                    thread.start()
                else:
                    print("Invalid command")
                    push_message("Oops", "Invalid Command")
            else:
                print("Listening...")
        except Exception as exception:
            print("PushBullet listener exception: " + str(exception))


def start_reply_listener():
    reply_listener_thread = threading.Thread(target=reply_listener)
    reply_listener_thread.start()
