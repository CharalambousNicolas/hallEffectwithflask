# importeer de flask library
from flask import Flask
from flask import render_template
from DbClass import DbClass
from flask import request
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = BackgroundScheduler()
scheduler.start()
loggedin = 0

app = Flask(__name__)


@app.route('/')
def homePage():
    global loggedin
    return render_template('homepage.html', loggedin=loggedin)


@app.route('/testimonials')
def testimonials():
    global loggedin
    return render_template('testimonials.html', loggedin=loggedin)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    DB_Layer = DbClass()

    global loggedin
    if request.method == 'POST':
        Inputsubject = request.form.get('subject')
        Inputmessage = request.form.get('message')
        print(Inputsubject)
        print(Inputmessage)
        DB_Layer.saveContactToDatabase(1, Inputsubject, Inputmessage)

    return render_template("contact.html", loggedin=loggedin)


@app.route('/createAccount')
def createAccount():
    global loggedin
    return render_template("createAccount.html", loggedin=loggedin)


@app.route('/totaldistance')
def totaldistance():
    global loggedin
    DB_layer = DbClass()
    totaldistance = DB_layer.getTotalDistanceFromDatabase()


    return render_template("totaldistance.html", loggedin=loggedin, data=totaldistance[0])


@app.route('/lastRun')
def lastRun():
    global loggedin
    return render_template("lastRun.html", loggedin=loggedin)


@app.route('/speed')
def speed():
    global loggedin
    DB_layer = DbClass()
    speed = DB_layer.getSpeedFromDatabase()

    return render_template("speed.html", loggedin=loggedin, speed=speed[0])


@app.route('/daybyday')
def daybyday():
    global loggedin
    return render_template("daybyday.html", loggedin=loggedin)


@app.route('/account')
def account():
    global loggedin
    return render_template("account.html", loggedin=loggedin)


# @app.route('/login')
# def login():
#     return render_template("login.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    DB_Layer = DbClass()
    error = ""
    users = DB_Layer.getUsersFromDatabase()
    global loggedin
    if request.method == 'POST':
        InputUsername = request.form.get('username')
        InputPassword = request.form.get('password')
        print(InputPassword)
        print(InputUsername)
        for i in range(len(users)):

            userData = users[i]
            print(userData)
            DBusername = userData[1]
            DBpassword = userData[2]
            if DBusername == InputUsername:
                if DBpassword == InputPassword:
                    print(
                        userData)
                    loggedin = 1
                    return render_template("totaldistance.html", loggedin=loggedin)

        else:
            error = "Email or password is incorrect."
            return render_template("login.html", error=error, loggedin=loggedin)
    if request.method == 'GET':
        return render_template("login.html", loggedin=loggedin)


import RPi.GPIO as GPIO
import time
from lcd import LCD

mylcd = LCD(13, 26, 5, 0, 0, 0, 0, 16, 12, 19, 6)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pulse = 0
distance = 0.00
rpm = 0.00
speed = 0.00
wheel_c = 0.15708
multiplier = 0
hall = 21
elapse = 0.00
start = time.time()
GPIO.setup(hall, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def get_pulse(number):
    global elapse, distance, start, pulse, speed, rpm, multiplier
    cycle = 0
    pulse += 1
    cycle += 1
    if pulse > 0:
        elapse = time.time() - start
        pulse -= 1
    if cycle > 0:
        distance += wheel_c
        cycle -= 1

    multiplier = 3600 / elapse

    speed = (wheel_c * multiplier) / 1000
    rpm = 1 / elapse * 60

    start = time.time()


mylcd.startDisplay()
mylcd.ShowText("Distance: ")
mylcd.ShowText("Speed: ")
GPIO.add_event_detect(hall, GPIO.FALLING, callback=get_pulse, bouncetime=20)


def printstuff():
    currentTime = datetime.datetime.today()
    DB_Layer = DbClass()
    DB_Layer.saveSensorValuesToDatabase(distance, speed, currentTime)
    print('rpm:{0:.2f} speed:{1:.2f} distance:{2} elapse:{3:.4f} multiplier:{4:.4f}'.format(rpm, speed, distance,
                                                                                            elapse, multiplier))
    # speed = round(speed, 2)
    mylcd.ShowText(distance)
    mylcd.ShowText(speed)
    time.sleep(2)


scheduler.add_job(func=printstuff, trigger=IntervalTrigger(seconds=5), id='checkSensors', name='saving sensor data',
                  replace_existing=True)
# start de Flask server met debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
