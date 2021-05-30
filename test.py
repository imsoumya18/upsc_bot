import discord
from discord.ext import tasks
import datetime
import requests
from bs4 import BeautifulSoup
import asyncio

TOKEN = 'TOKEN(str)'               # Replace with your token
OWN_ID = 'YOUR ID(int)'            # Replace with your own id

bot = discord.Client()


@bot.event
async def on_ready():
    print('Started')
    while True:
        res = requests.get('https://www.visioniascurrentaffairs.com')
        soup = BeautifulSoup(res.text, 'html.parser')
        url = soup.find('a', attrs={'class': 'green'})
        embedparam = discord.Embed(title=url.getText(), description='[Download]({})'.format(url.get('href')),
                                   color=0x0addd7)
        await bot.get_channel(845113175561076827).send(embed=embedparam)
        await asyncio.sleep(24*60*60)


@bot.event
async def on_message(message):
    if message.content.lower() == '--help':
        embedparam = discord.Embed(title='--help', description='Get help', color=0x0addd7)
        embedparam.add_field(name='--hindu', value='Get daily The Hindu newspaper PDF', inline=False)
        embedparam.add_field(name='--yojana', value='Get monthly Yojana magazine PDF', inline=False)
        if message.author.id == OWN_ID:
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

    elif message.content.lower() == '--server' and message.author.id == OWN_ID:
        servers = []
        async for guild in bot.fetch_guilds(limit=150):
            servers.append(guild.name)
        embedparam = discord.Embed(title='Server List', description='\n'.join(servers), color=0x0addd7)
        await message.channel.send(embed=embedparam)
        await bot.get_channel(845113175561076827).send('Hi')

    elif message.content.lower() == '--channel' and message.author.id == OWN_ID:
        for guild in bot.guilds:
            text_channel_list = []
            for channel in guild.text_channels:
                text_channel_list.append(channel.name)
            if guild == bot.guilds[0]:
                embedparam = discord.Embed(title=guild.name, description='\n'.join(text_channel_list), color=0x0addd7)
            else:
                embedparam.add_field(name=guild.name, value='\n'.join(text_channel_list), inline=False)
        await message.channel.send(embed=embedparam)


# @tasks.loop(hours=24)
# async def daily_task():
#     await bot.get_channel(845113175561076827).send('Hi')
#
#
# @daily_task.before_loop
# async def wait_until_3pm_utc():
#     now = datetime.datetime.utcnow()
#     next_run = now.replace(hour=15, minute=7, second=0)
#
#     if next_run < now:
#         next_run += datetime.timedelta(days=1)
#
#     await discord.utils.sleep_until(next_run)


bot.run(TOKEN)
