import requests
from bs4 import BeautifulSoup

res = requests.get('https://iasbano.com/indian-express-upsc.php#download_the_hindu', headers={"User-Agent": "XY"})
print(res)
# res = requests.get('https://newspaperpdf.online/download-indian-express.php', headers={"User-Agent": "XY"})
# print(res)
