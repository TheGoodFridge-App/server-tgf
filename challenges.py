from flask import Blueprint, request, jsonify
import json
import random
import requests
from firestore import db
from collections import defaultdict
from os import environ

challenges = Blueprint("challenges", __name__)

@challenges.route('/get', methods=['GET'])
def get_user_challenges():
    email = request.args.get('email')
    secret = request.args.get('secret')

    if secret != environ.get('APP_SECRET'):
        return "Sorry you are not authorized to perform this action", 400

    try:
        ref = db.collection(u'users').document(str(email)).collection('challenges').document('challenges')
        data = ref.get().to_dict()

        challenges = data['challenges']

        if len(challenges) < 3:
            challenges = add_challenges(str(email), data)

        formatted_challenges = []
        for challenge in challenges:
            formatted_challenges.append({
                'name': challenge,
                'current': challenges[challenge]['current'],
                'level': challenges[challenge]['level']
            })
        return jsonify({'challenges': formatted_challenges}), 200

    except Exception as e:
        print(e)
        ret = 'Failed with error: ' + str(e)
        return ret, 400

def add_challenges(email, challenge_data):
    ref = db.collection(u'users').document(email)
    data = ref.get().to_dict()

    issues = data['animal_issues'] + data['environment_issues'] + data['human_issues']
    #get challenges for the issues above (could cause problems if not multi-threaded but lets see)
    response = requests.get(
        'https://the-good-fridge.herokuapp.com/challenges/from_issues',
        params={'issues[]': issues, 'secret[]': environ.get('APP_SECRET')},
    )

    all_challenges = json.loads(response.content)['challenges']
    print(all_challenges)
    challenge_arr = list(challenge_data['challenges'].keys())
    ongoing_and_completed_challenges = challenge_arr + challenge_data['history']
    new_challenges_needed = 3 - len(challenge_arr)

    undone_challenges = [challenge for challenge in all_challenges if challenge not in ongoing_and_completed_challenges]
    challenges = dict(challenge_data['challenges'])

    for i in range(new_challenges_needed):
        new_challenge = undone_challenges[random.randint(0, len(undone_challenges))]
        
        challenges[new_challenge] = {
            u'current': 0,
            u'level': 1
        }
        # challenges += [{}.update({
        #     new_challenge: {'current': 0, 'level': 1}
        # })]

        del undone_challenges[undone_challenges.index(new_challenge)]

    ref = db.collection(u'users').document(email).collection('challenges').document('challenges')
    ref.set({
        'challenges': challenges,
        'history': challenge_data['history']
    })

    return jsonify(challenges)
    
@challenges.route('/completed', methods=['GET'])
def get_completed_challenges():
    email = request.args.get('email')
    secret = request.args.get('secret')

    if secret != environ.get('APP_SECRET'):
        return "Sorry you are not authorized to perform this action", 400

    try:
        ref = db.collection(u'users').document(str(email)).collection('challenges').document('challenges')
        data = ref.get().to_dict()

        history = data['history']
        return {'history': history}

    except Exception as e:
        print(e)
        ret = 'Failed with error: ' + str(e)
        return ret, 400

@challenges.route('/from_issues')
def get_challenges_from_issues():
    issues = request.args.getlist('issues[]')
    secret = request.args.get('secret[]')

    if secret != environ.get('APP_SECRET'):
        return 'Sorry you are not authorized to perform this action', 400
        
    try:
        ref = db.collection(u'relationships')
        docs = ref.stream()
        data = {}
        issue_challenges = {}

        for doc in docs:
            data[doc.id] = doc.to_dict()

        # need only issue to challenges
        data = data['issues_challenges']

        # make a dict of just arrays so its easier to get the challenges
        for doc in data:
            issue_challenges.update(data[doc])

        challenges = []
        # get the challenges for the issues provided
        for issue in issues:
            challenges += issue_challenges[issue]

        challenges = list(set(challenges))

        return {'challenges': challenges}, 200

    except Exception as e:
        print(e)
        ret = 'Failed with error: ' + str(e)
        return ret, 400


@challenges.route('/from_labels')
def get_challenges_from_labels():
    labels = request.args.getlist('labels[]')
    secret = request.args.get('secret[]')

    if secret != environ.get('APP_SECRET'):
        return 'Sorry you are not authorized to perform this action', 400
        
    try:
        ref = db.collection(u'relationships')
        docs = ref.stream()
        data = {}
        labels_challenges = {}

        for doc in docs:
            data[doc.id] = doc.to_dict()

        # need only issue to challenges
        data = data['labels_challenges']

        # make a dict of just arrays so its easier to get the challenges
        for doc in data:
            labels_challenges.update(data[doc])

        challenges = defaultdict()
        # get the challenges for the issues provided
        for label in labels:
            challenges[label] = labels_challenges[label]

        return challenges, 200

    except Exception as e:
        print(e)
        ret = 'Failed with error: ' + str(e)
        return ret, 400


@challenges.route('/descriptions')
def get_descriptions():
    challenge = request.args.get('challenge')
    secret = request.args.get('secret')

    if secret != environ.get('APP_SECRET'):
        return 'Sorry you are not authorized to perform this action', 400
        
    try:
        ref = db.collection(u'relationships')
        docs = ref.stream()
        data = {}
        challenge_descriptions = {}

        for doc in docs:
            data[doc.id] = doc.to_dict()

        # need only challenge descriptions
        data = data['challenge_descriptions']

        # make a dict of just arrays so its easier to get the challenges
        for doc in data:
            challenge_descriptions.update(data[doc])

        result = {
            "name": challenge
        }
        result.update(challenge_descriptions[challenge])

        # get the challenges for the issues provided
        return {'description': result}, 200

    except Exception as e:
        print(e)
        ret = 'Failed with error: ' + str(e)
        return ret, 400

