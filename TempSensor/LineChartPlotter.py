import pathlib
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pyrebase import pyrebase

config = {
    "apiKey": "AIzaSyD4kiF1wDR89lWdSReLGdrblEVjiw794d8",
    "authDomain": "smarthome-f5af7.firebaseapp.com",
    "databaseURL": "https://smarthome-f5af7.firebaseio.com",
    "projectId": "smarthome-f5af7",
    "storageBucket": "smarthome-f5af7.appspot.com",
    "messagingSenderId": "223998686071"
}

x = []
y = []


def get_data(date):
    try:
        x.clear()
        y.clear()
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()

        if date is None:
            today = datetime.now() - timedelta(1)
            today = today.strftime("%Y-%m-%d")
            # today = today.strftime("2019-03-29")  # DEBUG
        else:
            today = date.strftime("%Y-%m-%d")

        print(today)
        for i in range(24):
            if i < 10:
                hour = "0" + str(i) + "00"
            else:
                hour = str(i) + "00"

            result = db.child("Temperature").child(today).child(hour).get()

            if result.val() is not None:
                items = (result.val())
                x.append(str(items['heatIndex']))
                y.append(hour)
                print(hour + " heatIndex: " + str(items['heatIndex']) + " temperature: " + str(
                    items['temperature']) + " humidity: " + str(items['humidity']))
            else:
                print(hour + " No data")

        if len(x) < 1:
            from PushBulletHelper import push_message
            push_message("Oops", "No temperature data was found for that day")
        else:
            from PushBulletHelper import push_image
            try:
                plt.plot(y, x)
                plt.xlabel('Time')
                plt.ylabel('Temperature')
                plt.xticks(rotation=40)
                plt.title('Temperature Variance ' + today)
                ax = plt.gca()
                ax.xaxis.set_label_coords(1.05, -0.025)
                plt.grid(True)

                file = 'graphs\\temperature_' + today + '.png'
                plt.savefig(pathlib.Path(__file__).parent / file)
                # plt.show()
                push_image("temperature.png", file)
            except Exception as graph_exception:
                print("Graphing exception:" + str(graph_exception))
    except Exception as db_exception:
        print("Database exception:" + str(db_exception))
