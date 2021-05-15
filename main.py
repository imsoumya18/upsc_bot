import discord
import requests
from bs4 import BeautifulSoup

client = discord.Client()


@client.event
async def on_ready():
    print('Started')


@client.event
async def on_message(message):
    if message.content == 'newspaper':
        res = requests.get('https://www.visioniascurrentaffairs.com')
        soup = BeautifulSoup(res.text, 'html.parser')
        url = soup.find("a", attrs={"class": "green"})
        await message.channel.send('Today\'s The Hindu:\n' + url.get('href'))


client.run('TOKEN')
