from flask import Flask, request, jsonify
import pyrebase
import json
import firebase_admin
from firebase_admin import credentials, firestore
from os import environ

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

cred = {
    u"type": "service_account",
    u"project_id": "thegoodfridge-74422",
    u"private_key_id": environ.get('PRIVATE_KEY_ID', ''),
    u"private_key": environ.get('PRIVATE_KEY', '').replace('\\n', '\n'),
    u"client_email": environ.get('CLIENT_EMAIL', ''),
    u"client_id": environ.get('CLIENT_ID', ''),
    u"auth_uri": "https://accounts.google.com/o/oauth2/auth",
    u"token_uri": "https://oauth2.googleapis.com/token",
    u"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    u"client_x509_cert_url": environ.get('CLIENT_CERT_URL', '')
}

cred = credentials.Certificate(cred)

default_app = firebase_admin.initialize_app(cred)

db = firestore.client()

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True #make the json pretty

@app.route("/")
def index():
    return "<h1> Hello World </h1>"

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
    email = request.args.get('email[]')
    first_name = request.args.get('first_name[]')
    last_name = request.args.get('last_name[]')

    value1 = "true" == request.args.get('environment[]')
    value2 = "true" == request.args.get('animal[]')
    value3 = "true" == request.args.get('human[]')

    environment_issues = request.args.getlist('environment_issues[]')
    animal_issues = request.args.getlist('animal_issues[]')
    human_issues = request.args.getlist('human_issues[]')

    try:
        ref = db.collection(u'users').document(str(email))
        ref.set({
            u'first_name': first_name,
            u'last_name': last_name,
            u'environment': value1,
            u'animal': value2,
            u'human': value3,
            u'environment_issues': environment_issues,
            u'animal_issues': animal_issues,
            u'human_issues': human_issues
        })
        return 'Success', 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

@app.route('/api/values/update', methods=['GET', 'POST', 'PUT'])
def update_values():
    email = request.args.get('email[]')
    first_name = request.args.get('first_name[]')
    last_name = request.args.get('last_name[]')

    value1 = "true" == request.args.get('environment[]')
    value2 = "true" == request.args.get('animal[]')
    value3 = "true" == request.args.get('human[]')

    environment_issues = request.args.getlist('environment_issues[]')
    animal_issues = request.args.getlist('animal_issues[]')
    human_issues = request.args.getlist('human_issues[]')

    try:
        ref = db.collection(u'users').document(str(email))
        ref.update({
            u'first_name': first_name,
            u'last_name': last_name,
            u'environment': value1,
            u'animal': value2,
            u'human': value3,
            u'environment_issues': environment_issues,
            u'animal_issues': animal_issues,
            u'human_issues': human_issues
        })
        return 'Success', 200

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


@app.route('/grocery_list')
def update_grocery():
    email = request.args.get('email')
    g_list = request.args.get('list')

    if g_list:
        g_list = g_list.replace('\'', '')
        g_list = g_list.replace(', ', ',')
        g_list = g_list.split(',')

    try:
        ref = db.collection(u'users').document(str(email))
        if g_list:
            ref.update({
                u'grocery_list': g_list
            })

        else:
            g_list = jsonify(ref.get().to_dict()['grocery_list'])
        return g_list, 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

def check_grocery(g_list):
    print(g_list)

@app.route('/goal', methods=['GET', 'POST', 'PUT'])
def goal():
    email = request.args.get('email')
    goal = request.args.get('goal')
    progress = request.args.get('progress')

    if goal:
        goal = int(goal)

    if progress:
        progress = int(progress)

    try:
        ref = db.collection(u'users').document(str(email))

        if goal:
            if progress:
                update = {"goals": {'goal': goal, 'progress': progress}}
            else:
                update = {"goals": {'goal': goal}}
        else:
            update = {"goals": {"progress": progress}}
        
        ref.update(update)

        return "Success", 200
    
    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

#suggestions (get the product, get the data from sentiment)


if __name__ == '__main__':
    app.run(debug=True)
