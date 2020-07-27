from flask import Blueprint, request, jsonify
from firestore import db

api = Blueprint("api", __name__)

@api.route('/values', methods=['GET', 'POST', 'PUT'])
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

@api.route('/values/update', methods=['GET', 'POST', 'PUT'])
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

@api.route('/data', methods=['GET'])
def get_data():
    email = request.args.get('email')

    try:
        ref = db.collection(u'users').document(str(email))
        data = ref.get()

        return jsonify(data.to_dict()), 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400