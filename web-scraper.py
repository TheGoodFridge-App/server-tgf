#TODO: need to integrate entity analysis code into the Analysis function

import urllib
import requests
from bs4 import BeautifulSoup

from google.cloud import language
from google.cloud.language import enums



class Server_Object:
    def __init__(self, name, score, magnitude):
        self.name = name
        self.score = score
        self.magnitude = magnitude

#Server_Object arr = []

#Entity Analysis function
class Entity:
    def __init__(self, document_to_use):
        self.text_content = document_to_use

    def analyze_entities(self):
        client = language_v1.LanguageServiceClient()
        document = {"content": self.text_content, "type": type_}
        encoding_type = enums.EncodingType.UTF8
        response = client.analyze_entitity_sentiment(document, encoding_type=encoding_type)
        for entity in response.entities:
            print(u"Representative name for the entity: {}".format(entity.name))
            print(u"Entity sentiment score: {}".format(sentiment.score))
            print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))




# list of urls
urls = [
    'https://www.sustain.ucla.edu/our-initiatives/food-systems/'
]

searches = [
    'organic products'
]

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
headers = {"user-agent": USER_AGENT}

class Analysis:
    #initializes an object with the correct url
    def __init__(self, object_to_search):
        self.object_to_search = object_to_search
        #self.url = 'https://www.google.com/search?q={0}&source=lnms&tbm=nws'.format(self.object_to_search)
        object_to_search = object_to_search.replace(' ', '+')
        self.url = f"https://google.com/search?q={query}"
        self.sentiment = 0

    def run(self):
resp = requests.get(self.url, headers=headers)
i = 0
if resp.status_code == 200:
    soup = BeautifulSoup(resp.content, "html.parser")
    results = []
    for g in soup.find_all('div', class_='r'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                    soup_1 = BeautifulSoup(response.content, "html.parser")
                    text += soup_1.find_all('p')
                    i += 1
                    if (i == 10)
                        return text


for search in searches:
    obj_web_scrape = Analysis(search)
    doc = obj_web_scrape.run()
    obj_entity_analysis = Entity(doc)
    obj_entity_analysis.analyze_entities()
