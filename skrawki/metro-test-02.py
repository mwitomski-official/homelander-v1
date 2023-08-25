'''

Pozyskanie danych z konkretnego ogłoszenia w metrohouse.pl

'''

import requests
from bs4 import BeautifulSoup
import pprint as pp

#link = r"https://metrohouse.pl/nieruchomosc/DUGA350/nieruchomosc-na-sprzedaz-mieszkanie-lodz-baluty-urzednicza"
link = r"https://metrohouse.pl/nieruchomosc/XODO816/nieruchomosc-na-sprzedaz-mieszkanie-lodz-baluty-lutomierska"

r = requests.get(link)
soup = BeautifulSoup(r.text, 'html.parser')

# details = soup.find_all('div', {'class': 'table-box-style'})
details = soup.find_all('div', {'class': 'col-xs-6'})

desc = []
for item in details:
    desc.append(item.get_text().strip())

keys = desc[::2]
values = desc[1::2]
res = dict(zip(keys, values))

pp.pp(res)
