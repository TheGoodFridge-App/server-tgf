from flask import Flask, request, jsonify
import pyrebase
import json
import firebase_admin
from firebase_admin import credentials, firestore

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

cred = credentials.Certificate('./serviceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

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
        return error, 400
        # return str(e)#"Account already taken. Please sign in", 400

@app.route('/api/values', methods=['GET', 'POST', 'PUT'])
def post_values():
    email = request.args.get('email')
    value1 = "True" == request.args.get('value1')
    value2 = "True" == request.args.get('value2')
    value3 = "True" == request.args.get('value3')

    try:
        ref = db.collection(u'users').document(str(email))
        ref.set({
            u'value1': value1,
            u'value2': value2,
            u'value3': value3,
        })
        return 'Sucess', 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

@app.route('/api/values/update', methods=['POST', 'PUT'])
def update_values():
    email = request.args.get('email')
    value1 = "True" == request.args.get('value1')
    value2 = "True" == request.args.get('value2')
    value3 = "True" == request.args.get('value3')

    try:
        ref = db.collection(u'users').document(str(email))
        ref.update({
            u'value1': value1,
            u'value2': value2,
            u'value3': value3,
        })
        return 'Sucess', 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

@app.route('/data', methods=['GET'])
def get_data():
    email = request.args.get('email')

    try:
        ref = db.collection(u'users').document(str(email))
        data = ref.get()

        return jsonify(data.to_dict()), 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400



#suggestions (get the product, get the data from sentiment)


if __name__ == '__main__':
    app.run()
