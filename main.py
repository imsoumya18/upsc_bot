import discord
from datetime import datetime, time, timedelta
import requests
from bs4 import BeautifulSoup
import asyncio

TOKEN = 'TOKEN(str)'               # Replace with your token
OWN_ID = 'YOUR ID(int)'            # Replace with your own id
WHEN = time(3, 0, 0)

bot = discord.Client()


@bot.event
async def on_ready():
    print('Started')
    # while True:
    #     res = requests.get('https://www.visioniascurrentaffairs.com')
    #     soup = BeautifulSoup(res.text, 'html.parser')
    #     url = soup.find('a', attrs={'class': 'green'})
    #     embedparam = discord.Embed(title=url.getText(), description='[Download]({})'.format(url.get('href')),
    #                                color=0x0addd7)
    #     await bot.get_channel(845113175561076827).send(embed=embedparam)
    #     await asyncio.sleep(1)


async def called_once_a_day():
    await bot.wait_until_ready()
    channel = bot.get_channel(845113175561076827)
    await channel.send('Loop running')


async def background_task():
    while True:
        now = datetime.utcnow()
        target_time = datetime.combine(now.date(), WHEN)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)
        await called_once_a_day()
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)


@bot.event
async def on_message(message):
    if message.content.lower() == '--help':
        embedparam = discord.Embed(title='--help', description='Get help', color=0x0addd7)
        embedparam.add_field(name='--hindu', value='Get daily The Hindu newspaper PDF', inline=False)
        embedparam.add_field(name='--yojana', value='Get monthly Yojana magazine PDF', inline=False)
        if message.author.id == OWN_ID and message.channel.id == 847856568581357578:
            embedparam.add_field(name='---------------Extras---------------', value='Extra commands for DEVELOPER ONLY',
                                 inline=False)
            embedparam.add_field(name='--server', value='Get all servers list', inline=False)
            embedparam.add_field(name='--channel', value='Get all channels list', inline=False)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--hindu':
        res = requests.get('https://www.visioniascurrentaffairs.com')
        soup = BeautifulSoup(res.text, 'html.parser')
        url = soup.find('a', attrs={'class': 'green'})
        embedparam = discord.Embed(title=url.getText(), description='[Download]({})'.format(url.get('href')),
                                   color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--yojana':
        res = requests.get('https://chahalacademy.com/free-downloads-yojana')
        soup = BeautifulSoup(res.text, 'html.parser')
        url = soup.find('a', string='Open File')
        embedparam = discord.Embed(title=url.get('title'),
                                   description='[Download]({})'.format('https://chahalacademy.com/' + url.get('href')),
                                   color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--server' and message.author.id == OWN_ID and message.channel.id == 847856568581357578:
        servers = []
        async for guild in bot.fetch_guilds(limit=150):
            servers.append(guild.name)
        embedparam = discord.Embed(title='Server List', description='\n'.join(servers), color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--channel' and message.author.id == OWN_ID and message.channel.id == 847856568581357578:
        for guild in bot.guilds:
            text_channel_list = []
            for channel in guild.text_channels:
                try:
                    text_channel_list.append(channel.name)
                except:
                    text_channel_list.append('<Censored>')
            if guild == bot.guilds[0]:
                embedparam = discord.Embed(title=guild.name, description='\n'.join(text_channel_list), color=0x0addd7)
            else:
                embedparam.add_field(name=guild.name, value='\n'.join(text_channel_list), inline=False)
        await message.channel.send(embed=embedparam)


bot.loop.create_task(background_task())
bot.run(TOKEN)
