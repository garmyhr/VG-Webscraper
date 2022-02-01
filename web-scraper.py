from http.client import NON_AUTHORITATIVE_INFORMATION
from bs4 import BeautifulSoup
import requests
import operator
import time
import datetime

# Skriv et program som kjører i en terminal, som periodisk gjør en såkalt "web scrape" av forsiden på vg.no. 
# Publiseringstidspunkt, tittel og evt ingress eller annen hovedinformasjon skrives ut som enkeltlinjer, sortert på publiseringstidspunkt.
# Første scrape viser alle artikler, videre scrapes viser bare nye artikler. 
# Programmet kjører i uendelig loop, i sleep i intervallene mellom scrapes, inntil bruker avbryter med ctrl+c eller tilsvarende.

def main():
    
    link = "https://www.vg.no"
    articles = []

    soup = get_soup(link)
    data = get_data_from_soup(soup)

    # Scrapes initial articles from link
    for article in data:
        title = find_title(article)
        timestamp = find_timestamp(article)

        if title != None:
            articles.append(Article(title, timestamp))

    # Sorts initial articles by publishingtime
    articles.sort()
    for article in articles:
        print(article)
    

    # Main loop
    while(True):

        # Get last element from sorted articles
        last_timestamp = articles[-1].timestamp
        print('scanning...')
        soup = get_soup(link)
        data = get_data_from_soup(soup)

        for article in data:
            title = find_title(article)
            timestamp = find_timestamp(article)

            if timestamp == None:
                continue
            
            if last_timestamp < timestamp:
                print(Article(title, timestamp))

        time.sleep(30)


def get_soup(link):
    html_doc = requests.get(link)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    return soup

def find_title(article):
    return article.find("h3", {"class": "headline"}).get('aria-label')

def find_timestamp(article):
    if article.find('time') != None:
        timestamp = article.find('time').get('datetime')
        return datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.000Z')
        

def get_data_from_soup(soup):
    data = []
    for div in soup.find_all('div'):
        if div.get('class') != None:
            if 'article-container' in div.get('class') and div.get('class') != None:
                data.append(div)

    return data

class Article:
    def __init__(self, title, timestamp):
        self.title = title
        if isinstance(timestamp, datetime.datetime):
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.datetime.now()

    def __lt__(self, other):
        return self.timestamp < other.timestamp
    
    def __eq__(self, other):
        return self.timestamp == other.timestamp

    def __repr__(self):
        timestamp = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return f'Tittel: {self.title}\nPubliseringstidspunkt: {timestamp}\n'

if __name__ == "__main__":
    main() 