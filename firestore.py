import firebase_admin
from firebase_admin import credentials, firestore
from os import environ

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
