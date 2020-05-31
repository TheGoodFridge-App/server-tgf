#TODO: need to integrate entity analysis code into the Analysis function

import urllib
import requests
from bs4 import BeautifulSoup

from google.cloud import language
from google.cloud.language import enums



class server_obj:
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
        type_ = enums.Document.Type.PLAIN_TEXT
        client = language.LanguageServiceClient()
        lang = "en"
        document = {"content": self.text_content, "type": type_, "language": lang}
        encoding_type = enums.EncodingType.UTF8
        response = client.analyze_entity_sentiment(document, encoding_type=encoding_type)
        list = []
        for entity in response.entities:
            sentiment = entity.sentiment
            if (sentiment.score!=0.0 and entity.name != "Money" and entity.name != "Fashion" and entity.name != "Investment" and entity.name != "Energy" and entity.name != "Home" and entity.name != "Beauty" and entity.name != "Thanks" and entity.name != "Finance" and entity.name != "Building" and entity.name != "Health" and entity.name != "Company" and entity.name != "Companies" and entity.name!="producer" and entity.name!="data-entity" and entity.name!="data-entity-type" and entity.name!="producers" and entity.name!="entity-substitution" and entity.name!="data-entity-substitution" and entity.type != 'LOCATION' and entity.type != 'EVENT' and entity.type != 'PERSON' and entity.type != 'PRICE'):
                if (entity.name[0].isupper()):
                    list.append(server_obj(entity.name, sentiment.score, sentiment.magnitude))
                    #print(u"Representative name for the entity: {}".format(entity.name))
                    #print(u"Entity sentiment score: {}".format(sentiment.score))
                    #print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))
                    #print(u"Entity type: {}".format(entity.type))
        list.sort(key=lambda x: x.score, reverse=True)
        for obj in list:
            print(u"{}, {}".format(obj.name, obj.score))
            #print(u"Entity sentiment score: {}".format(obj.score))
            #print(u"Entity sentiment magnitude: {}".format(obj.magnitude))




products = [
    #"milk"
    #"cereal"
    #"coffee"
    #"candy"
    #"chocolate"
    #"beer"
    #"drinks"
    #"fast food"
    #"bananas"
    #"apple"
    #"orange"
    #"avocado"
    #"bread"
    #"rice"
    #"eggs"
    #"onions"
    #"garlic"
    #"lettuce"
    #"nut"
    #"salt"
    #"pepper"
    "sugar"
    #"honey"
    #"cookies"


]
searches = [
    "ethical levels of"
    "most ethical"
    "how ethical are different"
    #"fairtrade"
    "ranking ethical"
]

# desktop user-agent
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
# mobile user-agent
MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
headers = {"user-agent": USER_AGENT}
text = ""

class Analysis:
    #initializes an object with the correct url
    def __init__(self, object_to_search):
        self.object_to_search = object_to_search
        #self.url = 'https://www.google.com/search?q={0}&source=lnms&tbm=nws'.format(self.object_to_search)
        query = object_to_search.replace(' ', '+')
        self.url = f"https://google.com/search?q={query}"

    def run(self):
        resp = requests.get(self.url, headers=headers)
        i = 0
        text = ""
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            results = []
            for g in soup.find_all('div', class_='r'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    if link is not None:
                        response = requests.get(link, headers=headers)
                        if response.status_code == 200:
                            try:
                                soup_1 = BeautifulSoup(response.content, "html.parser")
                                text += str(soup_1.find_all('p'))
                                i += 1
                                if (i == 8):
                                    break
                                    #print(text)
                                    #return text
                            except:
                                pass
        return(text)


for search in searches:
    for product in products:
        sep = " "
        seq = (search, product, "brands")
        str1 = sep.join(seq)
        obj_web_scrape = Analysis(str1)
        doc = obj_web_scrape.run()
        obj_entity_analysis = Entity(doc)
        obj_entity_analysis.analyze_entities()
