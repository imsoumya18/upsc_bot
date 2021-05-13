import discord
import requests
from bs4 import BeautifulSoup
import schedule

client = discord.Client()


def job():
    res = requests.get('https://www.visioniascurrentaffairs.com')
    soup = BeautifulSoup(res.text, 'html.parser')
    url = soup.find("a", attrs={"class": "green"})
    channel = client.get_channel(842452759705944124)
    channel.send(url.get('href'))


@client.event
async def on_ready():
    print('Started')


client.run('ODQyMzc2MDkyNTA1NDczMDc0.YJ0Z3w.7zWHI6AnHTdBz0egq0kEujsMtV4')

schedule.every().day.at('23:04')
