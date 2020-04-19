from bs4 import BeautifulSoup
import requests

urls = [
    'https://www.sustain.ucla.edu/our-initiatives/food-systems/'
]

def scrape_urls():
    for url in urls:
        scrape_url(url)

def scrape_url(url):
    try:
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, 'html.parser')

        keywords = soup.get_text()
        keywords = keywords.split('\n')
        filtered_keywords = list(filter(lambda x: len(x) > 0 and x[:2] == '– ', keywords))
        filtered_keywords = list(map(lambda x: x[2:] if len(x) > 2 else x, filtered_keywords))
        for word in filtered_keywords:
            print(word)
    except requests.exceptions.RequestException as e:
        SystemExit(e)

scrape_urls()

    
        
