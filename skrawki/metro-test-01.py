'''
Test pozyskania pojedynczej strony z ogłoszeniami w serwisie metrohouse.pl
'''

import requests
from bs4 import BeautifulSoup

# link = r"https://metrohouse.pl/na-sprzedaz/mieszkanie/-/rynek-wtorny/"
link = r"https://metrohouse.pl/na-sprzedaz/mieszkanie/-/rynek-wtorny/page-2"

r = requests.get(link)
soup = BeautifulSoup(r.text, 'html.parser')

names = soup.find_all('div', {'class': 'propertylist-item col-lg-12 col-md-12 col-sm-6 col-xs-12 agreement'})

if names:
    for n in names:
        name_title = n.find('img', {'class': 'propertylist-image'}).get('title')
        name_price = n.find('span', {'itemprop': 'price'}).get('content').strip()
        print(name_title, ', cena: ', name_price, 'PLN')