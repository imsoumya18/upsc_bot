import requests
from bs4 import BeautifulSoup
from datetime import datetime, time, timedelta

res = requests.get('http://www.visionias.in/resources/current_affairs.php?c=ca')
soup = BeautifulSoup(res.text, 'html.parser')
title = soup.find('a').getText().strip()
url = soup.find('a').get('href')

print(datetime.strptime(str(datetime.now().month), '%m').strftime('%B'))
print(title)
print(url)
