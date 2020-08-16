import pprint
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import os

print(os.getcwd())

cred = credentials.Certificate("ServiceAccountKey.json")
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
        'Leaders for Breeders',
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

challenges_map = {
    "environment": [
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
    "animal": [
        'Leaders for Breeders',
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
    ],
    "human": [
        'Coffee Connoisseur',
        'Chocolate Challenge',
        'Local Lover',
        'Flower Fairy',
        'Better Bananas',
        'Responsible Rockstar',
        'Tea Trustee',
        'Tomato Taster',  # 30
        'Spice Savior'
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
    'Leaders for Breeders',
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
    'Spice Savior'
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


def get_challenge_desc():
    description = "description"
    impact = "impact"

    return {
        "environment": {
            "Waste Warrior": {
                description: "A Waste Warrior understands that waste, hazardous or not, negatively impacts the environment. They support organizations that minimize the production and mismanagement of waste so that human, animal and ecological health is protected.",
                impact: ["You are supporting responsible practices that reduce the consumption of raw materials and prevent deforestation",
                         "You are supporting organizations that effectively manage land, water, soil and other natural resources", "You are helping to protect native plant and animal species and their habitats"]
            },
            "Sustainability Superhero": {
                description: "A Sustainability Superhero wants to help save the Earth by supporting organizations that produce goods to meet the needs of people today, without sacrificing the needs of people in the future.",
                impact: ["You are supporting responsible practices that use ecological resources like water, energy, and raw materials in a manner that does not compromise future needs",
                         "You are promoting energy efficiency and the use of alternative energy", "You are supporting the minimization of waste production and consumption"]
            },
            "Emissions Slasher": {
                description: "The Emissions Slasher is aware that excessive greenhouse gas emissions are a serious threat to human, animal, and ecological health.  They support organizations that aim to minimize emissions while also promoting carbon sequestration.",
                impact: ["You are promoting energy efficiency and alternative energy", "You are helping responsibly manage land to prevent deforestation, soil erosion, etc. and raising animals in a way that minimizes emissions",
                         "You are supporting monitoring and improvement of operations to decrease emissions (i.e. reducing food transportation distances)"]
            },
            "Conservation Champion": {
                description: "The Conservation Champion succeeds in supporting organizations that reduce the unnecessary use or destruction of natural resources while also protecting natural ecosystems that are home to native plant and animal species.",
                impact: ["You are supporting responsible practices that reduce the consumption of raw materials and prevent deforestation",
                         "You are supporting organizations that effectively manage land, water, soil and other natural resources", "You are helping to protect native plant and animal species and their habitats"]
            },
            "Battle for Biodiversity": {
                description: "The Battle for Biodiversity supports organizations that fight for the protection of a diverse and resilient ecosystem.",
                impact: ["You are supporting responsible practices that protect native plant and animal species and their habitats",
                         "You are supporting organizations that work to maintain a diverse and productive ecosystem", "You are supporting pollinators (like bees) that are important for maintaining biodiversity"]
            },
            "Water Guardian": {
                description: "The Water Guardian understands the importance of clean and available water sources for the health of humans, animals and natural ecosystems. They support organizations that maintain healthy water in lakes, rivers, or the ocean.",
                impact: ["You are supporting practices that reduce water consumption and efficiently manage water resources, like lakes and rivers.",
                         "You are supporting organizations that maintain healthy water quality and create buffer zones around natural bodies of water or drinking water sources to prevent contamination"]
            },
            "Air Guardian Angel": {
                description: "An Air Guardian Angel loves healthy, clean air. They support organizations that help maintain air quality by preventing the release of toxic air pollutants, whether by minimizing their release or by growing plants that help clean the air.",
                impact: ["You are supporting responsible practices that work to reduce harmful emissions that contribute to climate change",
                         "You are also helping maintain healthy air quality through supporting various practices that promote carbon sequestration or reduce emissions", "You are helping organizations that work to minimize the distances that food is transported"]
            },
            "Fight Against Toxins": {
                description: "The Fight Against Toxins is for those who want to prevent harmful chemicals from polluting natural ecosystems, along with our sources for water and raw materials, by supporting organizations that responsibly manage or minimize the use of toxic chemicals.",
                impact: ["You are supporting responsible practices that help prevent toxic pollution from entering the natural environment",
                         "You are supporting organizations that either use no pesticide, herbicide and other chemicals, or use safer alternatives", "You are promoting practices that create buffer zones around production sites"]
            },
            "Patron for Regeneration": {
                description: "The Patron for Regeneration wants to support organizations that go above and beyond sustainability. They understand the importance of proactive work that not only conserves ecological resources and nature, but also fosters and restores it.",
                impact: ["You are supporting sustainable and resilient practices that maintain harmony within a living environment by matching natural ecosystems to the operation",
                         "You are supporting organizations that preserve ecosystem quality and work to foster and restore natural ecosystems"]
            },
            "Seafood Star": {
                description: "The Seafood Star shines as they support fisheries that want to protect and maintain ocean and sea animal health.  They buy seafood that does not endanger the sustainability of their populations and responsibly manages operations to prevent pollution.",
                impact: ["You are supporting responsible practices that work to maintain and protect fish populations and their ecosystems",
                         "You are supporting organizations that prevent toxic environmental and ocean pollution by ensuring effective storage and waste management of fisheries"]
            },
            "Dairy Delight": {
                description: "A Dairy Delight challenger is supporting dairy farms that are implementing eco-friendly practices that minimize their negative impact on the environment.",
                impact: ["You are supporting responsible practices that work to prevent toxic environmental pollution by dairy farms and related operations",
                         "You also help contribute relatively less harmful emissions by not supporting practices that prime animals to grow and develop at unnaturally fast rates"]
            },
            "Conserve with Coffee": {
                description: "The Conserve with Coffee Challenge works to prevent the production of coffee that destroys natural ecosystems.  It supports organizations that grow coffee within natural, strong forest ecosystems that have positive effects on the environment.",
                impact: ["You are supporting practices that protect native plant and animal species and their habitats", "You are supporting organizations that require fewer pesticides and fertilizers and instead utilize natural pest control and protect soil",
                         "You are supporting practices that increase carbon sequestration and improve the pollination of plants"]
            },
            "Coffee Chief (Environment & Human Rights)": {
                description: "A Coffee Chief understands that human and environmental protection go hand in hand, and that the coffee industry has a significant impact on both. They support organizations that promote farming practices that are sustainable for both the land and the surrounding communities.",
                impact: ["You are protecting workers and the environment by supporting organizations that require fewer pesticides and fertilizers and instead utilize natural pest control and protect soil",
                         "You are supporting fair, sustainable wages for farmers", "You are supporting practices that protect native plant and animal species and their habitats"]
            }
        },
        "animal": {
            "Leaders for Breeders": {
                description: "A Leader for Breeders supports proper breeding procedures that ensures optimal animal health and wellbeing. A Leader for Breeders understands that when a farm breeds selectively according to the most profitable characteristics of animals, it greatly compromises animals’ health and wellbeing.",
                impact: ["You are supporting farmers who select and breed animals who are suited to a more natural life and optimal health",
                         "You are supporting the prohibition of cloned or genetically engineered animals as they are a great risk to animal health"]
            },
            "Transport Tactitian": {
                description: "A Transportation Tactician supports humane transportation of farm animals. They understand that transportation can be very stressful for animals as they usually are deprived of food, water, and bedding.",
                impact: ["You are supporting humane treatment of animals during transportation, free from risks of stress, injury and diseases",
                         "You are helping animals to have adequate space and room during their transportations"]
            },
            "Habitat Heroes": {
                description: "Habitat Heroes support humane living conditions for farm animals. Habitat Heroes believe that animals should not be housed in crowded and dirty conditions as they often are in many industrial operations.",
                impact: ["You are supporting farms where its animals are given living conditions that accommodate the animals’ health and natural behaviours",
                         "You are supporting farms that give animals sufficient and clean space to live in"]
            },
            "Humane Handlers": {
                description: "Humane Handlers support farms in which its animals are handled with care. Humane Handlers condemns inhumane handling methods such as kicking, pushing, shoving of animals as it often causes pain and distress for animals.",
                impact: ["You are supporting farms to handle their animals with care at all times",
                         "You are helping the farm animals to experience less pain and distress during their lives on the farm"]
            },
            "Nutrition Nourisher": {
                description: "Nutrition Nourishers support farms that ensure animals are fed a diet that is optimal for their health.",
                impact: ["You are helping to ensure that animals are fed food that are optimal for their health and wellbeing",
                         "You are also supporting farms that allow the animals to express natural behaviors and eat the food they prefer the way they adapted to eating it"]
            },
            "Health Managers": {
                description: "Health Managers support farms that are equipped to optimize animal health. Health managers also believe that farm animals should be free from risks of diseases and injuries and support the use of medications only when it's necessary.",
                impact: ["You are helping animals to be able to enjoy good health free from preventable diseases and sufferings",
                         "You are helping to prevent resistance to antibiotics and other diseases for organisms that may be harmful for both animals and for humans that consume them"]
            },
            "Friends for Freedom": {
                description: "Friends for Freedom support farm animals to live a more natural life. Friends for Freedom believe that animals should live in environments where they are able to exhibit natural behaviours.",
                impact: ["You are supporting farms who allow their animals to access outdoor environments that depict natural environments and allow them to exhibit natural behaviours",
                         "You are allowing animals to have the freedom to express natural behaviours, which are pleasurable and promote biological functionings"]
            },
            "Battle for Beef": {
                description: "Battle for Beef aims to support farms that handle cows ethically in order to protect their health and wellness.",
                impact: ["You are supporting livestocks to be handled ethically to minimize pain and sufferings during their lifetime",
                         "You are contributing to livestock’s being able to exhibit their natural behaviours such as grazing on pasture", "You are supporting farms that feed its livestock organic and nutritious feed and forages"]
            },
            "Convert the Chicken": {
                description: "Convert the Chicken aims to support farms that handle chickens ethically in order to protect their health and wellness.",
                impact: ["You are supporting chickens to have adequate room and space to stretch their wings and exhibit their natural behaviours",
                         "You are supporting a stress free environment with outdoor access and natural sunshine", "You are supporting farms who use no growth stimulants not chemicals on its chickens"]
            },
            "Turkey Tactics": {
                description: "The Turkey Tactics Challenge aims to support farms that handle turkeys ethically in order to protect their health and wellness.",
                impact: ["You are supporting turkeys to have adequate room and access to outdoors", "You are supporting turkeys to be handled ethically to minimize pain and sufferings during their lifetime",
                         "You are supporting farms who raise turkeys with organic nutritious feed with no chemicals or stimulants"]
            }
        },
        "human": {
            "Coffee Connoisseur": {
                description: "A Coffee Connoisseur understands that market price fluctuations can drastically impact farmers. They support ethically sourced coffee beans and grounds from organizations that provide a premium on top of the regular coffee price to help protect farming communities.",
                impact: ["You are supporting fair, sustainable wages for farmers",
                         "You are supporting local projects (such as construction of a school) in a coffee-farming community", "You are contributing to the premium that goes directly back to farmers"]
            },
            "Tea Trustee": {
                description: "A Tea Trustee purchases sustainably and ethically source tea, whether loose leaf or in tea bags. Tea leaves are harvested by hand, and buying from a certified organization helps protect workers from forced labor or coercion to work overtime.",
                impact: ["You are supporting organizations committed to protecting labor rights", "You are helping workers exercise their freedom to unionize and speak up about wrongdoings",
                         "You are helping provide workers with wages they can support their families with"]
            },
            "Chocolate Challenge": {
                description: "The Chocolate Challenge involves recognizing that the cacao market is notorious for employing forced and child labor. It encourages purchasing cacao, whether in the form of cacao powder, nibs, or regular chocolate bars, from companies that help protect against this.",
                impact: ["You are supporting the mitigation of forced and child labor", "You are helping prioritize human rights and safe working conditions over economics",
                         "You are supporting premiums that go directly back to cacao farming communities"]
            },
            "Local Lover": {
                description: "A Local Lover is aware that purchasing seasonal, local produce supports small businesses and stimulates the local economy. They support farmers from the surrounding area by attending and purchasing seasonal produce from local farmers’ markets or co-ops.",
                impact: ["You are supporting local farms and businesses, promoting their future success",
                         "You are helping increase transparency and accountability of farms to ethical standards by directly interacting with farmers and providing them with adequate returns for their produce"]
            },
            "Better Bananas": {
                description: "The Better Bananas challenge recognizes harvesting bananas is a dangerous job, and workers are often under pressure to harvest as quickly as possible. It supports organizations that provide safe working conditions and do not rely on forced labor to harvest bananas.",
                impact: ["You are supporting organizations that provide medical care for workers who get injured on the job",
                         "You are helping promote the use of labor contracts that protect workers from working long hours", "You are supporting fair wages for workers that are independent of market prices"]
            },
            "Tomato Taster": {
                description: "A Tomato Taster recognizes that, due to the seasonality of the tomato crop, workers are extremely vulnerable to exploitation during harvest season. They support organizations that promote fair labor practices like gender equality, safe working conditions, and respect for workers’ cultural identity.",
                impact: ["You are supporting ethical labor practices and gender equality",
                         "You are helping encourage large grocery corporations to partner with ethical organizations", "You are supporting the fair compensation of workers for their labor"]
            },
            "Flower Fairy": {
                description: "A Flower Fairy is aware that flowers are typically highly regulated crops, involve lots of industrial grade pesticide, and require a large labor force to harvest flowers at just the right time. They support organizations that minimize worker vulnerability and exposure to harmful chemicals.",
                impact: ["You are supporting safe working conditions for flower farmers and workers",
                         "You are helping provide regular medical care to workers to ensure their health"]
            },
            "Spice Savior": {
                description: "A Spice Savior recognizes that procurement of spices is rooted in exploitation and imperialism. They support ethically sourced dried and packaged spices that deviate from this trend and respect the cultural identity of the original spices.",
                impact: ["You are supporting organizations that respect the cultural identity of workers and empower them rather than oppress",
                         "You are helping workers receive a direct premium for the spices they harvest, which is reinvested into the community", "You are helping protect communities from bioprospecting"]
            },
            "Responsible Rockstar": {
                description: "A Responsible Rockstar knows that there are increasingly more new products with ethical certifications. They support the continued growth of the ethical production process by always being on the lookout for new products that indicate human rights were not violated.",
                impact: ["You are helping demonstrate that ethical products need to increase in quantity by exercising your purchasing power to buy certified products",
                         "You are supporting the ethical treatment and fair payment of workers in all industries by choosing the certified product over the conventional"]
            }
        }
    }


def main():
    challenge_descriptions = get_challenge_desc()
    ref = db.collection(u'relationships').document('challenge_descriptions')
    ref.set({
        u'environment': challenge_descriptions['environment'],
        u'animal': challenge_descriptions['animal'],
        u'human': challenge_descriptions['human'],
    })


if __name__ == '__main__':
    main()
