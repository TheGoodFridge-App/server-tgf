import pprint
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./ServiceAccountKey.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()

# hash map from values to issues
values_issues = {
    'environment': [
        'Environment Regeneration',
        'Reduced Emissions',
        'Conservation',
        'Biodiversity',
        'Waste Management',
        'Water Management',
        'Air Quality',
        'Pollution Reduction'
    ],
    'animal': [
        'Appropriate Breeding',
        'Transportation',
        'Humane Slaughter',
        'Living Conditions',
        'Handling',
        'Proper Nutrition',
        'Health Management',
        'Access to Outdoors'
    ],
    'human': [
        'Sustainable Wages',
        'Gender Equity/Equality',
        'No Child Labor',
        'No Forced Labor',
        'Small-scale Workers',
        'Working Conditions',
        'Cultural Identity',
        'Community Empowerment'
    ]
}

# list of labels
# warning: do NOT change the ordering of the lists. future hash maps (like issues_labels) depend on this ordering to be consistent
labels = {
    'environment': [
        'Fair Trade Certified',  # 0
        'Shade Grown or Bird Friendly Coffee',
        'Rainforest Alliance Certified',
        'Food Alliance Certified',
        'USDA Organic',
        'AGA Grassfed',
        'Protected Harvest Certified',
        'Marine Stewardship Council',
        'Best Aquaculture Practices (BAP)',
        'Responsibly Grown, Farmworker Assured',
        'Certified B Corporation',  # 10
        'California Sustainable Wine-Growing Program',
        'Roundtable on Sustainable Palm Oil',
        'Bonsucro',
        'Alliance for Water Stewardship',
        'Aquaculture Stewardship Council',
        'Vegan',
        'Certified Plant-Based',
        'Regenerative Organic Certified',
        'UEP Cage-Free'
    ],
    'animal': [
        'USDA Organic',  # 0
        'AGA Grassfed',
        'Certified Grassfed by AGW',
        'Certified Animal Welfare AGW',
        'UEP Cage-Free',
        'Food Alliance',
        'BAP Certification',
        'ASC',
        'Certified Naturally Grown',
        'American Humane Certified',
        'Certified Humane',  # 10
        'Global Animal Partnership lvl 1',
        'Global Animal Partnership lvl 2',
        'Global Animal Partnership lvl 3',
        'Global Animal Partnership lvl 4',
        'Global Animal Partnership lvl 5'
    ],
    'human': [
        'Fair Trade Certified',  # 0
        'Rainforest Alliance',
        "Local Farmer's Market",
        'Whole Trade',
        'Fair for Life',
        'Food Justice Certified',
        'Fair Food Program',
        'Responsibly Grown, Farmworker Assured',
        'Cooperative Coffees',
        'Regenerative Organic Certified',
        'UEBT Certified'  # 10
    ]
}

# hash map from issues to labels


def get_issues_labels():
    values = labels.keys()
    result = {}
    for value in values:
        arr = labels[value]
        if value == 'environment':
            result.update({'environment': {
                'Environment Regeneration': [arr[1], arr[2], arr[5], arr[9], arr[18]],
                'Reduced Emissions': [arr[1], arr[2], arr[3], arr[6], arr[9], arr[11], arr[16], arr[17], arr[18], arr[19]],
                'Conservation': [arr[0], arr[1], arr[2], arr[3], arr[6], arr[7], arr[8], arr[9], arr[15], arr[18]],
                'Biodiversity': [arr[0], arr[1], arr[2], arr[3], arr[6], arr[7], arr[8], arr[13], arr[15], arr[18]],
                'Waste Management': [arr[0], arr[2], arr[3], arr[5], arr[6], arr[8], arr[9], arr[18], arr[19]],
                'Water Management': [arr[0], arr[1], arr[2], arr[3], arr[5], arr[6], arr[8], arr[9], arr[11], arr[14], arr[15], arr[18], arr[19]],
                'Air Quality': [arr[1], arr[2], arr[3], arr[18], arr[19]],
                'Pollution Reduction': [arr[0], arr[1], arr[2], arr[3], arr[4], arr[6], arr[8], arr[15], arr[18], arr[19]]
            }})
        elif value == 'animal':
            result.update({'animal': {
                'Appropriate Breeding': [arr[0], arr[3], arr[8], arr[10]],
                'Transportation': [arr[3], arr[5], arr[6], arr[8], arr[9], arr[10], arr[11], arr[12], arr[13], arr[14], arr[15]],
                'Humane Slaughter': [arr[3], arr[5], arr[6], arr[9], arr[10], arr[11], arr[12], arr[13], arr[14], arr[15]],
                'Living Conditions': [arr[0], arr[1], arr[3], arr[4], arr[5], arr[8], arr[9], arr[10], arr[12], arr[13], arr[14], arr[15]],
                'Handling': [arr[2], arr[3], arr[4], arr[8], arr[9], arr[10]],
                'Proper Nutrition': [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[7], arr[8], arr[9], arr[10]],
                'Health Management': [arr[0], arr[1], arr[3], arr[4], arr[7], arr[8], arr[9], arr[10], arr[11], arr[12], arr[13], arr[14], arr[15]],
                'Access to Outdoors': [arr[0], arr[3], arr[4], arr[5], arr[8], arr[9], arr[10], arr[13], arr[14], arr[15]]
            }})
        elif value == 'human':
            result.update({'human': {
                'Sustainable Wages': [arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10]],
                'Gender Equity/Equality': [arr[0], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8]],
                'No Child Labor': [arr[0], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10]],
                'No Forced Labor': [arr[0], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10]],
                'Small-scale Workers': [arr[8]],
                'Working Conditions': [arr[0], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7], arr[8], arr[9], arr[10]],
                'Cultural Identity': [arr[0], arr[1], arr[4], arr[5], arr[9], arr[10]],
                'Community Empowerment': [arr[0], arr[1], arr[2], arr[4], arr[5], arr[7], arr[8], arr[9], arr[10]]
            }})
    return result


formatted_challenges = {
    'environment': [
        'Seafood Star',  # 0
        'Sustainability Superhero',
        'Emissions Slasher',
        'Conservation Champion',
        'Battle for Biodiversity',
        'Waste Warrior',
        'Water Guardian',
        'Air Guardian Angel',
        'Fight Against Toxins',
        'Patron for Regeneration',
        'Dairy Delight',  # 10
        'Conserve with Coffee'
    ],
    'animal': [
        'Leaders of Breeders',
        'Transport Tactitian',
        'Habitat Heroes',
        'Humane Handlers',
        'Nutrition Nourisher',
        'Health Managers',
        'Friends for Freedom',
        'Ethical Eggs',
        'Battle for Beef',  # 20
        'Convert the Chicken',
        'Turkey Tactics'
    ],
    'human': [
        'Coffee Connoisseur',
        'Chocolate Challenge',
        'Local Lover',
        'Flower Fairy',
        'Better Bananas',
        'Responsible Rockstar',
        'Tea Trustee',
        'Tomato Taster',  # 30
        'Spice Savior',
        'Empowerment Exemplar'
    ]
}

challenges = [
    'Seafood Star',  # 0
    'Sustainability Superhero',
    'Emissions Slasher',
    'Conservation Champion',
    'Battle for Biodiversity',
    'Waste Warrior',
    'Water Guardian',
    'Air Guardian Angel',
    'Fight Against Toxins',
    'Patron for Regeneration',
    'Dairy Delight',  # 10
    'Conserve with Coffee',
    'Leaders of Breeders',
    'Transport Tactitian',
    'Habitat Heroes',
    'Humane Handlers',
    'Nutrition Nourisher',
    'Health Managers',
    'Friends for Freedom',
    'Ethical Eggs',
    'Battle for Beef',  # 20
    'Convert the Chicken',
    'Turkey Tactics',
    'Coffee Connoisseur',
    'Chocolate Challenge',
    'Local Lover',
    'Flower Fairy',
    'Better Bananas',
    'Responsible Rockstar',
    'Tea Trustee',
    'Tomato Taster',  # 30
    'Spice Savior',
    'Empowerment Exemplar'
]

# hash map from issues to challenges
issues_challenges = {
    'environment': {
        'Environment Regeneration': [challenges[9], challenges[4]],
        'Reduced Emissions': [challenges[2], challenges[1], challenges[9], challenges[10]],
        'Conservation': [challenges[3], challenges[1], challenges[11], challenges[0], challenges[6], challenges[9], challenges[11]],
        'Biodiversity': [challenges[4], challenges[1], challenges[0], challenges[9], challenges[11]],
        'Waste Management': [challenges[5], challenges[1], challenges[8], challenges[3], challenges[0]],
        'Water Management': [challenges[6], challenges[1], challenges[0], challenges[3]],
        'Air Quality': [challenges[7], challenges[1], challenges[2], challenges[10], challenges[11]],
        'Pollution Reduction': [challenges[8], challenges[0], challenges[6], challenges[5], challenges[7], challenges[9], challenges[10], challenges[11]]
    },
    'animal': {
        'Appropriate Breeding': [challenges[12], challenges[20], challenges[21], challenges[22]],
        'Transportation': [challenges[20], challenges[21], challenges[22], challenges[13]],
        'Humane Slaughter': [challenges[20], challenges[21], challenges[22]],
        'Living Conditions': [challenges[20], challenges[21], challenges[22], challenges[14]],
        'Handling': [challenges[20], challenges[21], challenges[22], challenges[15]],
        'Proper Nutrition': [challenges[20], challenges[21], challenges[22], challenges[16]],
        'Health Management': [challenges[20], challenges[21], challenges[22], challenges[17]],
        'Access to Outdoors': [challenges[20], challenges[21], challenges[22], challenges[18]]
    },
    'human': {
        'Sustainable Wages': [challenges[23], challenges[29], challenges[24], challenges[27], challenges[30], challenges[31]],
        'Gender Equity/Equality': [challenges[29], challenges[24], challenges[27], challenges[31], challenges[26]],
        'No Child Labor': [challenges[23], challenges[29], challenges[24], challenges[31], challenges[26], challenges[28]],
        'No Forced Labor': [challenges[23], challenges[29], challenges[24], challenges[27], challenges[31], challenges[28]],
        'Small-scale Workers': [challenges[25]],
        'Working Conditions': [challenges[24], challenges[29], challenges[28], challenges[27], challenges[30], challenges[31]],
        'Cultural Identity': [challenges[30], challenges[26], challenges[25], challenges[27], challenges[31], challenges[28]],
        'Community Empowerment': [challenges[23], challenges[29], challenges[24], challenges[25], challenges[30], challenges[28]]
    }
}


def get_labels_challenges():
    result = {}
    for value in labels:
        arr = labels[value]
        if value == 'environment':
            result.update({value: {
                arr[0]: [challenges[1], challenges[3], challenges[4], challenges[5], challenges[6], challenges[8], challenges[11]],
                arr[1]: [challenges[1], challenges[2], challenges[3], challenges[4], challenges[6], challenges[7], challenges[8], challenges[11]],
                arr[2]: [challenges[9], challenges[1], challenges[2], challenges[3], challenges[4], challenges[5], challenges[6], challenges[7], challenges[8], challenges[11]],
                arr[3]: [challenges[1], challenges[2], challenges[3], challenges[4], challenges[5], challenges[6], challenges[7], challenges[8]],
                arr[4]: [challenges[8], challenges[10], challenges[11]],
                arr[5]: [challenges[9], challenges[5], challenges[6]],
                arr[6]: [challenges[1], challenges[2], challenges[3], challenges[4], challenges[5], challenges[6], challenges[8]],
                arr[7]: [challenges[1], challenges[3], challenges[4], challenges[0]],
                arr[15]: [challenges[1], challenges[3], challenges[4], challenges[6], challenges[8], challenges[0]],
                arr[8]: [challenges[1], challenges[3], challenges[4], challenges[5], challenges[6], challenges[8], challenges[0]],
                arr[9]: [challenges[9], challenges[1], challenges[2], challenges[3], challenges[5], challenges[6]],
                arr[10]: [challenges[1]],
                arr[11]: [challenges[1], challenges[2], challenges[5]],
                arr[12]: [challenges[1]],
                arr[13]: [challenges[1], challenges[4]],
                arr[14]: [challenges[1], challenges[6]],
                arr[16]: [challenges[1], challenges[2]],
                arr[17]: [challenges[1], challenges[2]],
                arr[18]: [challenges[9], challenges[1], challenges[2], challenges[3], challenges[4],
                          challenges[5], challenges[6], challenges[7], challenges[8], challenges[11]]
            }})
        elif value == 'human':
            result.update({value: {
                arr[0]: [challenges[23], challenges[29], challenges[24], challenges[27], challenges[26], challenges[31]],
                arr[1]: [challenges[23], challenges[29], challenges[24], challenges[27], challenges[26]],
                arr[4]: [challenges[23], challenges[29], challenges[24], challenges[27], challenges[26], challenges[31]],
                arr[5]: [challenges[25]],
                arr[6]: [challenges[30]],
                arr[7]: [challenges[30], challenges[28]],
                arr[8]: [challenges[23]],
                arr[9]: [challenges[23], challenges[29]],
                arr[2]: [challenges[25]],
                arr[3]: [challenges[27], challenges[24]]
            }})
        elif value == 'animal':
            result.update({value: {
                arr[0]: [challenges[12], challenges[14], challenges[16], challenges[17], challenges[18], challenges[21], challenges[22]],
                arr[1]: [challenges[14], challenges[16], challenges[17], challenges[21]],
                arr[2]: [challenges[15], challenges[16]],
                arr[3]: [challenges[12], challenges[13], challenges[14], challenges[15], challenges[16], challenges[17], challenges[18], challenges[20]],
                arr[4]: [challenges[14], challenges[15], challenges[16], challenges[17], challenges[18]],
                arr[5]: [challenges[13], challenges[14], challenges[16], challenges[18], challenges[20]],
                arr[6]: [],
                arr[7]: [challenges[16], challenges[17]],
                arr[8]: [challenges[12], challenges[13], challenges[14], challenges[15], challenges[16], challenges[17], challenges[18], challenges[22]],
                arr[9]: [challenges[13], challenges[14], challenges[15], challenges[16], challenges[17], challenges[18], challenges[21], challenges[22]],
                arr[10]: [challenges[12], challenges[13], challenges[15], challenges[16], challenges[17], challenges[18]],
                arr[11]: [challenges[17], challenges[20]],
                arr[12]: [challenges[17], challenges[20]],
                arr[13]: [challenges[17], challenges[20]],
                arr[14]: [challenges[17], challenges[20]],
                arr[15]: [challenges[17], challenges[20]]
            }})

    return result


def main():
    labels_challenges = get_labels_challenges()

    ref = db.collection(u'relationships').document('labels_challenges')
    ref.set({
        u'environment': labels_challenges['environment'],
        u'animal': labels_challenges['animal'],
        u'human': labels_challenges['human'],
    })

    # pprint.pprint(issues_labels)

    # pprint.pprint(issues_challenges)
    labels_challenges = get_labels_challenges()
    pprint.pprint(labels_challenges)


if __name__ == '__main__':
    main()
