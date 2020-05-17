#TODO: need to integrate entity analysis code into the Analysis function

from bs4 import BeautifulSoup
import requests

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


class Analysis:
    #initializes an object with the correct url
    def __init__(self, object_to_search):
        self.object_to_search = object_to_search
        #self.url = 'https://www.google.com/search?q={0}&source=lnms&tbm=nws'.format(self.object_to_search)
        self.url = "https://www.google.com/search?sxsrf=ALeKk01aBV1XXhBr0o8x4xk-6x-RknZiqg%3A1589741016580&source=hp&ei=2IXBXqqLH86m_Qa1tIjABg&q=organic+milk+products&oq=organic+milk+products&gs_lcp=CgZwc3ktYWIQAzICCAAyAggAMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjIGCAAQFhAeMgYIABAWEB4yBggAEBYQHjoECCMQJzoFCAAQkQI6BQgAEIMBOgQIABBDOgQIABAKOgcIABAUEIcCOgQIABANOggIABCGAxCLA1DrFljtZGD7ZWgIcAB4AIABrAGIAawbkgEEMC4yOZgBAKABAaoBB2d3cy13aXq4AQI&sclient=psy-ab&ved=0ahUKEwiq18vkxrvpAhVOU98KHTUaAmgQ4dUDCAk&uact=5"
        self.sentiment = 0

    def run(self):
        response = requests.get(self.url)
        # gets all the webpages
        soup = BeautifulSoup(response.text, 'html.parser')
        # for each webpage, extracts text
        #TODO: attach entity analysis code and pass text into entity analysis
        for a in soup.find_all('a', href=True):
            r = requests.get(a['href'])
            new_soup = BeautifulSoup(r.text, 'html.parser')
            document = new_soup.get_text(separator=" ")
            return document


for search in searches:
    obj_web_scrape = Analysis(search)
    doc = obj_web_scrape.run()
    obj_entity_analysis = Entity(doc)
    obj_entity_analysis.analyze_entities()
