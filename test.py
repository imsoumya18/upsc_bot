import requests
from bs4 import BeautifulSoup

res = requests.get('https://www.careerswave.in/hindustan-times-newspaper-download/', headers={"User-Agent": "XY"})
soup = BeautifulSoup(res.text, 'html.parser')
title = 'Hindustan Times Epaper ' + soup.find('tr', attrs={'data-row_id': '0'}).find('td').getText()
print(title)
print(soup.find('tr', attrs={'data-row_id': '0'}).find_all('td')[1].getText())
