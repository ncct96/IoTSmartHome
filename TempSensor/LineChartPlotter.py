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


def plot_graph():
    try:
        plt.plot(y, x)
        plt.xlabel('Time')
        plt.ylabel('Temperature')
        plt.xticks(rotation=40)
        plt.title('Temperature Variance (Yesterday)')
        ax = plt.gca()
        ax.xaxis.set_label_coords(1.05, -0.025)
        plt.grid(True)
        plt.savefig("E:/Desktop/graph.png")
        # plt.show()
    except Exception as graph_exception:
        print(graph_exception)

    from PushBulletHelper import push_image
    push_image("temperature.png", "E:\\Desktop\\graph.png")


def get_data():
    try:
        firebase = pyrebase.initialize_app(config)
        auth = firebase.auth()
        user = auth.sign_in_with_email_and_password("chiupeeng@gmail.com", "ChiuPeeng98")
        db = firebase.database()

        today = datetime.now() - timedelta(1)
        print(today)
        for i in range(24):
            if i < 10:
                hour = "0" + str(i) + "00"
            else:
                hour = str(i) + "00"

            # result = db.child("Temperature").child(today.strftime("%Y-%m-%d")).child(hour).get()
            result = db.child("Temperature").child(today.strftime("2019-03-29")).child(hour).get()

            if result.val() is not None:
                items = (result.val())
                x.append(str(items['heatIndex']))
                y.append(hour)
                print(hour + " heatIndex: " + str(items['heatIndex']) + " temperature: " + str(items['temperature']) + " humidity: " + str(items['humidity']))
            else:
                print(hour + "00 No data")

        plot_graph()
    except Exception as db_exception:
        print(db_exception)

