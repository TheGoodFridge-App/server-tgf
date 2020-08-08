from flask import Blueprint, request
from firestore import db
from collections import defaultdict

challenges = Blueprint("challenges", __name__)


@challenges.route('/from_issues')
def get_challenges_from_issues():
    issues = request.args.getlist('issues[]')

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
    challenges = request.args.getlist('challenges[]')

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

        descriptions = []
        # get the challenges for the issues provided
        for challenge in challenges:
            descriptions.append(challenge_descriptions[challenge])

        return {'descriptions': descriptions}, 200

    except Exception as e:
        print(e)
        ret = 'Failed with error: ' + str(e)
        return ret, 400
