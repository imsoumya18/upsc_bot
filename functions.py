import requests
from datetime import datetime
from bs4 import BeautifulSoup


def hindu():
    title = 'The Hindu Epaper ' + '-'.join(
        list(map(str, [datetime.today().day, datetime.today().month, datetime.today().year])))

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/70.0.3538.77 Safari/537.36"}
        res = requests.get('https://dailyepaper.in/hindu-analysis-notes-in-pdf-2023/', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        url1 = soup.find('a', text='Download Now').get('href')
    except:
        url1 = ''

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/70.0.3538.77 Safari/537.36"}
        res = requests.get('https://dailyepaper.in/hindu-analysis-notes-in-pdf-2023/', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        url2 = soup.find('a', text='Download Now').get('href')
    except:
        url2 = ''

    return [title, url1, url2]


def vision_ca():
    res = requests.get('http://www.visionias.in/resources/current_affairs.php?c=ca')
    soup = BeautifulSoup(res.text, 'html.parser')
    title = 'Vision IAS Current Affairs ' + soup.find('a').getText().strip()
    url = soup.find('a').get('href')
    return [title, url]


def next_mcq():
    res = requests.get('https://www.nextias.com/montlhy-mcq')
    soup = BeautifulSoup(res.text, 'html.parser')
    element = soup.find("div", {"class": "table_inner_content_text"})
    title = 'Next IAS MCQ ' + element.find('h6').getText()
    url = element.find('a').get('href')
    return [title, url]


def insights_ca():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/70.0.3538.77 Safari/537.36"}
    res = requests.get('https://www.insightsonindia.com/tag/current-affairs-monthly-compilations/', headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    ele = soup.find('a', attrs={'rel': 'bookmark'})
    path = ele.get('href')
    res = requests.get(path, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find('h1', attrs={'class': 'entry-title'}).getText().split(' ', 1)[1].replace(',', ' -')
    url = soup.find('div', attrs={'class': 'entry-content'}).find('h3').find('a').get('href')
    return [title, url]


