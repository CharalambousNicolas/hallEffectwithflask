# importeer de flask library
from flask import Flask
from flask import render_template
from DbClass import DbClass
from flask import request

loggedin = 0
# Maak een applicatie-object aan
app = Flask(__name__)


@app.route('/')
def homePage():
    global loggedin
    return render_template('homepage.html', loggedin=loggedin)


@app.route('/testimonials')
def testimonials():
    global loggedin
    return render_template('testimonials.html', loggedin=loggedin)


@app.route('/contact')
def contact():
    global loggedin
    return render_template('contact.html', loggedin=loggedin)


@app.route('/createAccount')
def createAccount():
    global loggedin
    return render_template("createAccount.html", loggedin=loggedin)


@app.route('/totaldistance')
def totaldistance():
    global loggedin
    DB_layer = DbClass()
    totaldistance = DB_layer.getTotalDistanceFromDatabase()
    print(totaldistance)
    return render_template("totaldistance.html", loggedin=loggedin)


@app.route('/lastRun')
def lastRun():
    global loggedin
    return render_template("lastRun.html", loggedin=loggedin)


@app.route('/today')
def today():
    global loggedin
    return render_template("today.html", loggedin=loggedin)


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
    users = DB_Layer.getDataFromDatabase()
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


# start de Flask server met debug
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
