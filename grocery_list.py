from flask import Blueprint, request
from os import path
from collections import defaultdict
from firestore import db
from os import environ

grocery_list = Blueprint("grocery_list", __name__)

@grocery_list.route('/get', methods=['GET'])
def get_grocery():
    email = request.args.get('email')
    secret = request.args.get('secret')

    if secret != environ.get('APP_SECRET'):
        return 'Sorry you are not authorized to perform this action', 400
    
    try:
        ref = db.collection(u'users').document(str(email)).collection('groceries')
        docs = ref.stream()
        data = {}

        for doc in docs:
            data[doc.id] = doc.to_dict()

        data["grocery_list"] = data["grocery_list"]["grocery_list"]

        return data, 200

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400

@grocery_list.route('/', methods=['GET', 'POST'])
def post_grocery():
    email = request.args.get('email[]')
    g_list = request.args.getlist('items[]')
    secret = request.args.get('secret[]')

    if secret != environ.get('APP_SECRET'):
        return 'Sorry you are not authorized to perform this action', 400
    
    try:
        ref = db.collection(u'users').document(str(email)).collection('groceries').document('grocery_list')
        if g_list:
            ref.set({
                u'grocery_list': g_list,
            })
        ref = db.collection(u'users').document(str(email)).collection('groceries').document('purchased')
        ref.set({ 'dummy': 'dummy' })
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

@grocery_list.route('/purchased', methods=['PUT'])
def purchased():
    email = request.args.get('email')
    product = request.args.get('product')
    brand = request.args.get('brand')
    secret = request.args.get('secret')

    if secret != environ.get('APP_SECRET'):
        return 'Sorry you are not authorized to perform this action', 400
    
    try:
        ref = db.collection(u'users').document(email).collection('groceries').document('purchased')

        update_list = {}
        update_list[product] = brand

        if product and brand:
            ref.update(update_list)
            return "Success", 200

        else:
            raise Exception('Empty product name or brand')

    except Exception as e:
        ret = 'Failed with error: ' + str(e)
        return ret, 400
