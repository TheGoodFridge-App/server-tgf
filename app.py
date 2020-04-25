from flask import Flask, request
import pyrebase
import json

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyBd7KiM7D2q22t3AF5ZJd14dRgNtxUFynQ",
    "authDomain": "chat-app-demo-88083.firebaseapp.com",
    "databaseURL": "https://chat-app-demo-88083.firebaseio.com",
    "projectId": "chat-app-demo-88083",
    "storageBucket": "chat-app-demo-88083.appspot.com",
    "messagingSenderId": "156783601000",
    "appId": "1:156783601000:web:c37c752214b3949c7f62dd",
    "measurementId": "G-ZYT0ZF0ZMN"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

@app.route("/")
def index():
    return "<h1> Hello World <h1>"

@app.route('/api/login', methods=['GET'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        ret = "Login Successful" #+ str(user)
        return ret, 200

    except Exception as e:
        response = e.args[0].response
        error = response.json()['error']
        return error

@app.route('/api/register', methods=['GET'])
def register():
    email = request.args.get('email')
    password = request.args.get('password')
    try:
        user = auth.create_user_with_email_and_password(email, password)
        # auth.send_email_verification(user['idToken'])
        ret = "Register Successful " + str(user)
        return ret, 200

    except Exception as e:
        response = e.args[0].response
        error = response.json()['error']
        return error
        # return str(e)#"Account already taken. Please sign in", 400

if __name__ == '__main__':
    app.run()
