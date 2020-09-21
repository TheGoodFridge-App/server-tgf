#By: Shrenik Kankaria

import sys
import urllib
import requests
import re
from bs4 import BeautifulSoup
import csv
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore

cred = credentials.Certificate(#certificate path
)

app = firebase_admin.initialize_app(cred)

db = firestore.client()

# array containing labels the product contains
labels = []

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
headers = {"user-agent": USER_AGENT}
text = ""

state_abbrev_list = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV",
                     "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]

# sets necessary products in the database
def setDb(document_name, dict_to_set, merge):
    if merge == True:
        ref = db.collection(u'products_associated_with_labels').document(document_name).set(dict_to_set, merge=True)
    else:
        ref = db.collection(u'products_associated_with_labels').document(document_name).set(dict_to_set)

# gets the products associated with the label
def get_product(url, regex, label_name, string_to_delete_before, string_to_delete_after, document_name, merge=False):
    try:
        if label_name == "Responsibly Grown, Farmworker Assured":
            resp = requests.get(url, headers={"User-Agent": "XY"})
        else:
            resp = requests.get(url)
    except:
        print("Error")
    text = ""
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        titles = []
        l = label_name

        if l == "American Humane Certified" or l == "Certified Animal Welfare AGW" or l == "Certified Grassfed by AGW" or l == "Marine Stewardship Council" or l == "Cooperative Coffees":
            companies_found = soup.find_all('a', href=True, title=True)
        elif l == "Best Aquaculture Practices":
            companies_found = soup.find_all('td', class_="column-2 text-left")
        elif l == "Certified Naturally Grown":
            companies_found = soup.find_all('h4')
        elif l == "Alliance for Water Stewardship":
            companies_found = soup.find_all('td', class_="column-1")
        elif l == "Certified B Corporation":
            companies_found = soup.find_all('h3', class_="heading4 card__title")
        elif l == "Rainforest Alliance Certified":
            companies_found = soup.find_all('span', class_="field-title field")
        elif l == "Responsibly Grown, Farmworker Assured":
            companies_found = soup.find_all('td')
        elif l == "Fair for Life":
            companies_found = soup.find_all('a', href=True)
        elif l == "Food Justice Certified":
            companies_found = soup.find_all('h3', class_="one-em-margin-top")
        elif l == "Certified Plant-Based":
            companies_found = soup.find_all('font')
        # elif l == "Fair Food Program":
        #     companies_found = soup.find_all('p')
        # elif l == "Regenerative Organic Certified":
        #     companies_found = soup.find_all('span')

        # print(companies_found)
        dict = {}
        for text in companies_found:
            text = str(text)
            text = text.replace("\n", "")
            if (re.search(regex, text)) != None:
                search_string = (re.search(regex, text)).group(0)
                string = str(search_string)
                string = string.replace(string_to_delete_before, '')
                string = string.replace(string_to_delete_after, '')
                string = string.strip()
                if string[0] in dict:
                    if string not in dict[string[0]]:
                        dict[string[0]].append(string)
                else:
                    dict[string[0]] = [string]
        setDb(document_name, dict, merge)

    return False

def getProductsFromCSV(label_name, document_name, col_num, merge=False):
    if label_name == "Food Alliance":
        file = "Food-Alliance-Certified.csv"
    elif label_name == "USDA Organic":
        file = "usda-organic.csv"

    dict = {}
    with open(file, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            try:
                string = row[col_num]
                if string != None:
                    if string[0] in dict:
                        if string not in dict[string[0]]:
                            dict[string[0]].append(string)
                    else:
                        dict[string[0]] = [string]
            except:
                print("Error")
        setDb(document_name, dict, merge)

# gets the products associated with the labels that don't have searchable lists and ones that don't exceed 1 MB
def getAllProducts():
    get_product("http://www.humaneheartland.org/humane-certified-producers/category/all-producers", ">([A-Z]|[0-9]).*<", "American Humane Certified", '>', '<', "american_humane_certified")
    get_product("http://www.humaneheartland.org/humane-certified-producers/category/all-producers/2", ">([A-Z]|[0-9]).*<", "American Humane Certified", '>', '<', "american_humane_certified", True)
    get_product("https://www.bapcertification.org/Producers", ">([A-Z]|[0-9]).*<", "Best Aquaculture Practices", '>', '<', "best_aquaculture_practices")
    get_product("https://a4ws.org/certification/certified-sites/", ">([A-Z]|[0-9]).*<", "Alliance for Water Stewardship", '>', '<', "alliance_for_water_stewardship")
    get_product("https://equitablefood.org/efi-certified-farms", ">([A-Z]|[0-9]).*<", "Responsibly Grown, Farmworker Assured", ">", "<", "responsibly_grown_farmworker_assured")
    get_product("https://coopcoffees.coop/roaster-members/meet-our-members/", ">([A-Z]|[0-9]).*–", "Cooperative Coffees", ">", " –", "cooperative_coffees")
    get_product("https://www.fairforlife.org/pmws/indexDOM.php?client_id=fairforlife&page_id=certprod&lang_iso639=en", ">([A-Z]|[0-9]).*<", "Fair for Life", ">", "<", "fair_for_life")
    get_product("https://www.agriculturaljusticeproject.org/en/learn-more/", ">([A-Z]|[0-9]).*<", "Food Justice Certified", ">", "<", "food_justice_certified")
    get_product("http://info.nsf.org/Certified/cvv/Listings.asp?Program=QAI&CompanyName=&TradeName=&ProductStd=&Compliance=PB&PlantState=&PlantCountry=&search=Search", ">([A-Z]|[0-9]).*<", "Certified Plant-Based", ">", "<", "certified_plant_based")

    getProductsFromCSV("Food Alliance", "food_alliance", 0)

if __name__ == "__main__":
    getAllProducts()
