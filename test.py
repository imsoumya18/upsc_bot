import requests
from bs4 import BeautifulSoup
from datetime import datetime

res = requests.get('https://iasbano.com/the-hindu-pdf-download-1.php', headers={"User-Agent": "XY"})
soup = BeautifulSoup(res.text, 'html.parser')
tr = soup.find_all('tr')[2]
dat = tr.find_all('td')[0].getText().split()
dat[1] = dat[1][:-1]
title = 'The Hindu Epaper ' + "{:02d}".format(int(dat[0])) + '-'
for i in range(1, 13):
    if datetime.strptime(str(i), '%m').strftime('%B') == dat[1]:
        title += "{:02d}".format(i)
        break
title += '-' + dat[2]
url = tr.find_all('td')[1].find('a').get('href')
print(title)
print(url)
