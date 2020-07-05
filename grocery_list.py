from flask import Blueprint, request, jsonify
from os import path
from collections import defaultdict
from firestore import db

grocery_list = Blueprint("grocery_list", __name__)

@grocery_list.route('/get', methods=['GET'])
def get_grocery():
    email = request.args.get('email')

    try:
        ref = db.collection(u'groceries').document(str(email))
        data = ref.get()

        return jsonify(data.to_dict()), 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

@grocery_list.route('/', methods=['GET', 'POST'])
def post_grocery():
    email = request.args.get('email[]')
    g_list = request.args.getlist('items[]')

    try:
        ref = db.collection(u'groceries').document(str(email))
        if g_list:
            ref.set({
                u'email': email,
                u'grocery_list': g_list
            })
        else:
            raise Exception('Empty grocery list')
        
        recommendations, other = check_grocery(g_list)

        grocery_dict = {
            "recommendations": recommendations,
            "other": other
        }

        return grocery_dict, 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

def check_grocery(g_list):
    recommendations = defaultdict(list)

    for item in g_list:
        paths = 'ml-data/' + item.lower() + '.txt'
        paths_plural = 'ml-data/' + item.lower() + 's' + '.txt'
        if path.exists(paths):
            f = open(paths, 'r')
            i = 0
            for line in f:
                if i >= 3:
                    break
                brand, score = line.replace('\n', '').split(', ')
                recommendations[str(item)] += [brand]
                i += 1
        
        elif path.exists(paths_plural):
            f = open(paths_plural, 'r')
            i = 0
            for line in f:
                if i >= 3:
                    break
                brand, score = line.replace('\n', '').split(', ')
                recommendations[str(item)] += [brand]
                i += 1

    return recommendations, [item for item in g_list if item not in recommendations]

    