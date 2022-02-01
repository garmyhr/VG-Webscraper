from http.client import NON_AUTHORITATIVE_INFORMATION
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime

def main():
    
    articles = []
    link = "https://www.vg.no"
    soup = get_soup(link)
    data = get_data_from_soup(soup)

    get_initial_articles(data, articles)

    # Sort and print initial articles
    articles.sort()
    for article in articles:
        print(article)
    
    # Main loop
    while(True):

        # Get last element from sorted articles
        last_timestamp = articles[-1].timestamp
        last_title = articles[-1].title
        print('scanning...')
        soup = get_soup(link)
        data = get_data_from_soup(soup)

        for article in data:
            title = find_title(article)
            timestamp = find_timestamp(article)

            if timestamp == None:
                continue
            
            if last_timestamp < timestamp and last_title != title:
                articles.append(Article(title, timestamp))
                print(Article(title, timestamp))

        for x in range (0,5):  
            b = "Scanning" + "." * x
            print (b, end='\r')
            time.sleep(1)
        print('Scanning    ', end='\r')

def get_soup(link):
    html_doc = requests.get(link)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    return soup

def find_title(article):
    return article.find("h3", {"class": "headline"}).get('aria-label')

def find_timestamp(article):
    if article.find('time') != None:
        timestamp = article.find('time').get('datetime')
        return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.000Z')
        
def get_data_from_soup(soup):
    data = []
    for div in soup.find_all('div'):
        if div.get('class') != None:
            if 'article-container' in div.get('class') and div.get('class') != None:
                data.append(div)

    return data

def get_initial_articles(data, articles):

    for article in data:
        title = find_title(article)
        timestamp = find_timestamp(article)

        if title != None and timestamp != None:
            articles.append(Article(title, timestamp))

class Article:
    def __init__(self, title, timestamp):
        self.title = title
        if isinstance(timestamp, datetime):
            self.timestamp = timestamp
        else:
            cur_time = datetime.now()
            self.timestamp = datetime(cur_time.year, cur_time.month, cur_time.day)

    def __lt__(self, other):
        return self.timestamp < other.timestamp
    
    def __eq__(self, other):
        return self.timestamp == other.timestamp

    def __repr__(self):
        timestamp = self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        return f'Tittel: {self.title}\nPubliseringstidspunkt: {timestamp}\n'

if __name__ == "__main__":
    main() 
