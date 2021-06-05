import requests
from bs4 import BeautifulSoup

res = requests.get('https://iasbano.com/indian-express-upsc.php#download_the_hindu', headers={"User-Agent": "XY"})
soup = BeautifulSoup(res.text, 'html.parser')
tr = soup.find_all('tr')[2]
title = tr.find_all('td')[0].getText()
url = tr.find_all('td')[1].find('a').get('href')
print(title)
print(url)
