from flask import Flask, request, jsonify

from grocery_list import grocery_list
from challenges import challenges
from api import api
from firestore import db

app = Flask(__name__)
app.register_blueprint(grocery_list, url_prefix="/grocery_list")
app.register_blueprint(challenges, url_prefix="/challenges")
app.register_blueprint(api, url_prefix='/api')

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # make the json pretty


@app.route("/")
def index():
    return "<h1> Hello World </h1>"


if __name__ == '__main__':
    app.run(debug=True)
