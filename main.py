import discord
import requests
from bs4 import BeautifulSoup

TOKEN = 'TOKEN(str)'
OWN_ID = 'YOUR ID(int)'

bot = discord.Client()


@bot.event
async def on_ready():
    print('Started')
    # text_channel_list = []
    # for guild in bot.guilds:
    #     for channel in guild.text_channels:
    #         text_channel_list.append(channel.name)
    # print('\n'.join(text_channel_list))


@bot.event
async def on_message(message):
    if message.content.lower() == '--help':
        embedparam = discord.Embed(title='--help', description='Get help', color=0x0addd7)
        embedparam.add_field(name="--hindu", value="Get daily The Hindu newspaper PDF", inline=False)
        embedparam.add_field(name="--yojana", value="Get monthly Yojana magazine PDF", inline=False)
        await message.channel.send(embed=embedparam)
    elif message.content.lower() == '--hindu':
        res = requests.get('https://www.visioniascurrentaffairs.com')
        soup = BeautifulSoup(res.text, 'html.parser')
        url = soup.find("a", attrs={"class": "green"})
        embedparam = discord.Embed(title=url.getText(), description='[Download]({})'.format(url.get('href')),
                                   color=0x0addd7)
        await message.channel.send(embed=embedparam)
    elif message.content.lower() == '--yojana':
        res = requests.get('https://chahalacademy.com/free-downloads-yojana')
        soup = BeautifulSoup(res.text, 'html.parser')
        url = soup.find("a", string='Open File')
        embedparam = discord.Embed(title=url.get('title'),
                                   description='[Download]({})'.format('https://chahalacademy.com/' + url.get('href')),
                                   color=0x0addd7)
        await message.channel.send(embed=embedparam)
    elif message.content.lower() == '--server' and message.author.id == OWN_ID:
        servers = []
        async for guild in bot.fetch_guilds(limit=150):
            servers.append(guild.name)
        embedparam = discord.Embed(title='Server List', description='\n'.join(servers), color=0x0addd7)
        await message.channel.send(embed=embedparam)


bot.run(TOKEN)
