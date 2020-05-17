#TODO: need to integrate entity analysis code into the Analysis function

from bs4 import BeautifulSoup
import requests

from google.cloud import language_v1
from google.cloud.language_v1 import enums



#Entity Analysis function
class Entity:
    def __init__(self, document_to_use):
        self.text_content = document_to_use
        
    def analyze_entities(text_content):
        client = language_v1.LanguageServiceClient()
        document = {"content": text_content, "type": type_}
        encoding_type = enums.EncodingType.UTF8
        response = client.analyze_entities(document, encoding_type=encoding_type)
        for entity in response.entities:
            print(u"Representative name for the entity: {}".format(entity.name))
            print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
            print(u"Salience score: {}".format(entity.salience))
            for metadata_name, metadata_value in entity.metadata.items():
                print(u"{}: {}".format(metadata_name, metadata_value))
            for mention in entity.mentions:
                print(u"Mention text: {}".format(mention.text.content))
                print(u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name))


# list of urls
urls = [
    'https://www.sustain.ucla.edu/our-initiatives/food-systems/'
]


class Analysis:
    #initializes an object with the correct url
    def __init__(self, object_to_search):
        self.object_to_search = object_to_search
        self.url = 'https://www.google.com/search?q={0}&source=lnms&tbm=nws'.format(self.object_to_search)
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
