#TODO: need to integrate entity analysis code into the Analysis function

from bs4 import BeautifulSoup
import requests

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
