#By: Shrenik Kankaria

import sys
import urllib
import requests
import re
from bs4 import BeautifulSoup
import csv

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

# functions to get results from a search on the website by manipulating the url
def get_results_from_search(regex, label_name, company_name, string_to_delete_before, string_to_delete_after):

    if label_name == "Certified Animal Welfare AGW":
        url_name = "https://agreenerworld.org/gd-search-results/?geodir_search=1&stype=gd_place&s={}&snear=&scertification_type%5B%5D=Animal+Welfare&sgeo_lat=&sgeo_lon=".format(company_name)
        if check_label(url_name, regex, label_name, company_name, string_to_delete_before, string_to_delete_after):
            return
    elif label_name == "Certified Grassfed by AGW":
        url_name = "https://agreenerworld.org/gd-search-results/?geodir_search=1&stype=gd_place&s={}&snear=&scertification_type%5B%5D=Grassfed&sgeo_lat=&sgeo_lon=".format(company_name)
        if check_label(url_name, regex, label_name, company_name, string_to_delete_before, string_to_delete_after):
            return
    elif label_name == "Certified Naturally Grown":
        for state in state_abbrev_list:
            url_name = "https://certified.naturallygrown.org/producers/list/227/{}".format(state)
            if check_label(url_name, regex, label_name, company_name, string_to_delete_before, string_to_delete_after):
                return
    elif label_name == "Certified B Corporation":
        url_name = "https://bcorporation.net/directory?search={}&industry=&country=&state=&city=".format(company_name)
        if check_label(url_name, regex, label_name, company_name, string_to_delete_before, string_to_delete_after):
            return
    elif label_name == "Marine Stewardship Council":
        url_name = "https://fisheries.msc.org/en/fisheries/@@search?q={}&term=&bucket=&start=0&stop=10&__start__=fishery_name%3Asequence&__end__=fishery_name%3Asequence&__start__=species%3Asequence&__end__=species%3Asequence&__start__=gear_types%3Asequence&__end__=gear_types%3Asequence&__start__=locations%3Asequence&__end__=locations%3Asequence&__start__=status%3Asequence&__end__=status%3Asequence&search=search".format(company_name)
        if check_label(url_name, regex, label_name, company_name, string_to_delete_before, string_to_delete_after):
            return
    elif label_name == "Rainforest Alliance Certified":
        url_name = "https://www.rainforest-alliance.org/find-certified?location=&category=&keyword={}&op=submit".format(company_name)
        if check_label(url_name, regex, label_name, company_name, string_to_delete_before, string_to_delete_after):
            return
    return

# checks if the product has the certain label
def check_label(url, regex, label_name, company_name, string_to_delete_before, string_to_delete_after):
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

        for text in companies_found:
            text = str(text)
            text = text.replace("\n", "")
            # print(text)
            # print(re.search(regex, text))
            if (re.search(regex, text)) != None:
                search_string = (re.search(regex, text)).group(0)
                string = str(search_string)
                string = string.replace(string_to_delete_before, '')
                string = string.replace(string_to_delete_after, '')
                string = string.strip()
                # print(string)
                if company_name.upper() == string.upper():
                    labels.append(label_name)
                    return True
    return False

def checkLabelsFromCSV(label_name, company_name, col_num):
    if label_name == "Food Alliance":
        file = "Food-Alliance-Certified.csv"
    elif label_name == "USDA Organic":
        file = "usda-organic.csv"

    with open(file, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[col_num] == company_name:
                print(company_name)
                labels.append(label_name)


def checkAllLabels(company_name):
    # checks for the different types of labels the product contains and prints the labels
    check_label("http://www.humaneheartland.org/humane-certified-producers/category/all-producers", ">([A-Z]|[0-9]).*<", "American Humane Certified", company_name, '>', '<')
    check_label("https://www.bapcertification.org/Producers", ">([A-Z]|[0-9]).*<", "Best Aquaculture Practices", company_name, '>', '<')
    check_label("https://a4ws.org/certification/certified-sites/", ">([A-Z]|[0-9]).*<", "Alliance for Water Stewardship", company_name, '>', '<')
    check_label("https://equitablefood.org/efi-certified-farms", ">([A-Z]|[0-9]).*<", "Responsibly Grown, Farmworker Assured", company_name, ">", "<")
    check_label("https://coopcoffees.coop/roaster-members/meet-our-members/", ">([A-Z]|[0-9]).*–", "Cooperative Coffees", company_name, ">", " –")
    check_label("https://www.fairforlife.org/pmws/indexDOM.php?client_id=fairforlife&page_id=certprod&lang_iso639=en", ">([A-Z]|[0-9]).*<", "Fair for Life", company_name, ">", "<")
    check_label("https://www.agriculturaljusticeproject.org/en/learn-more/", ">([A-Z]|[0-9]).*<", "Food Justice Certified", company_name, ">", "<")
    check_label("http://info.nsf.org/Certified/cvv/Listings.asp?Program=QAI&CompanyName=&TradeName=&ProductStd=&Compliance=PB&PlantState=&PlantCountry=&search=Search", ">([A-Z]|[0-9]).*<", "Certified Plant-Based", company_name, ">", "<")

    get_results_from_search(">([A-Z]|[0-9]).*<", "Certified Animal Welfare AGW", company_name, '>', '<')
    get_results_from_search(">([A-Z]|[0-9]).*<", "Certified Grassfed by AGW", company_name, '>', '<')
    get_results_from_search(">.*<", "Certified Naturally Grown", company_name, '>', '<')
    get_results_from_search(">.*<", "Certified B Corporation", company_name, '>', '<')
    get_results_from_search(">.*<", "Marine Stewardship Council", company_name, '>', '<')
    get_results_from_search(">.*<", "Rainforest Alliance Certified", company_name, '>', '<')

    checkLabelsFromCSV("Food Alliance", company_name, 0)
    checkLabelsFromCSV("USDA Organic", company_name, 4)


if __name__ == "__main__":
    # takes command line arguments
    if len(sys.argv) >= 2:
        company_name = ""
        # builds company name from a multi-word argument
        for i in range(1, len(sys.argv)):
            string = sys.argv[i] + " "
            if i == len(sys.argv) - 1:
                string = sys.argv[i]
            company_name += string
        checkAllLabels(company_name)
        print(labels)
        #return labels
