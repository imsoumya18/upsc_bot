import discord
import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime, time, timedelta

TOKEN = 'TOKEN(str)'  # Bot Token
DEVELOPER_ID = 'DEVELOPER_ID(int)'  # Your Own ID
DEVELOPER_PRIVATE_CHANNEL = 'DEVELOPER_PRIVATE_CHANNEL_ID(int)'  # Developer's Private Channel ID
DEVELOPER_SEND_CHANNEL = 'DEVELOPER_SEND_CHANNEL_ID(int)'  # Developer's Private Channel ID
CHANNELS = ['LIST OF CHANNEL IDS(int)']  # Channel IDs
WHEN = time(2, 30, 0)  # UTC Time

bot = discord.Client()


@bot.event
async def on_ready():
    print('Started')


async def called_once_a_day():
    await bot.wait_until_ready()

    # hindu
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
    embedparam = discord.Embed(title=title, description='[Download]({})'.format(url), color=0x0addd7)

    # hindustan times
    htimes = requests.get('https://www.careerswave.in/hindustan-times-newspaper-download/',
                          headers={"User-Agent": "XY"})
    soup = BeautifulSoup(htimes.text, 'html.parser')
    embedparam.add_field(
        name='Hindustan Times Epaper ' + soup.find('tr', attrs={'data-row_id': '0'}).find('td').getText(),
        value='[Download]({})'.format(soup.find('tr', attrs={'data-row_id': '0'}).find_all('td')[1].getText()),
        inline=False)

    # indian express
    try:
        res = requests.get('https://iasbano.com/indian-express-upsc.php#download_the_hindu',
                           headers={"User-Agent": "XY"})
        soup = BeautifulSoup(res.text, 'html.parser')
        tr = soup.find_all('tr')[2]
        dat = tr.find_all('td')[0].getText().split()
        dat[1] = dat[1][:-1]
        title = 'The Indian Express Epaper ' + "{:02d}".format(int(dat[0])) + '-'
        for i in range(1, 13):
            if datetime.strptime(str(i), '%m').strftime('%B') == dat[1]:
                title += "{:02d}".format(i)
                break
        title += '-' + dat[2]
        url = tr.find_all('td')[1].find('a').get('href')
        embedparam.add_field(name=title, value='[Download]({})'.format(url), inline=False)
    except:
        embedparam.add_field(name='Sorry😔', value='Error fetching The Indian Express today', inline=False)
    for i in CHANNELS:
        await bot.get_channel(i).send(embed=embedparam)


async def background_task():
    now = datetime.utcnow()
    if now.time() > WHEN:
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()
        await asyncio.sleep(seconds)
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
        embedparam.add_field(name='--htimes', value='Get daily Hindustan Times newspaper PDF', inline=False)
        embedparam.add_field(name='--ie', value='Get daily The Indian Express newspaper PDF', inline=False)
        embedparam.add_field(name='--yojana', value='Get monthly Yojana magazine PDF', inline=False)
        if message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_PRIVATE_CHANNEL:
            embedparam.add_field(name='---------------Extras---------------', value='Extra commands for DEVELOPER ONLY',
                                 inline=False)
            embedparam.add_field(name='--server', value='Get all servers list', inline=False)
            embedparam.add_field(name='--channel', value='Get all channels list', inline=False)
            embedparam.add_field(name='--news <Channel ID(s)>', value='Send newspapers to channels immediately', inline=False)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--hindu':
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
        embedparam = discord.Embed(title=title, description='[Download]({})'.format(url), color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--htimes':
        res = requests.get('https://www.careerswave.in/hindustan-times-newspaper-download/',
                           headers={"User-Agent": "XY"})
        soup = BeautifulSoup(res.text, 'html.parser')
        embedparam = discord.Embed(
            title='Hindustan Times Epaper ' + soup.find('tr', attrs={'data-row_id': '0'}).find('td').getText(),
            description='[Download]({})'.format(
                soup.find('tr', attrs={'data-row_id': '0'}).find_all('td')[1].getText()), color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--ie':
        try:
            res = requests.get('https://iasbano.com/indian-express-upsc.php#download_the_hindu',
                               headers={"User-Agent": "XY"})
            soup = BeautifulSoup(res.text, 'html.parser')
            tr = soup.find_all('tr')[2]
            dat = tr.find_all('td')[0].getText().split()
            dat[1] = dat[1][:-1]
            title = 'The Indian Express Epaper ' + "{:02d}".format(int(dat[0])) + '-'
            for i in range(1, 13):
                if datetime.strptime(str(i), '%m').strftime('%B') == dat[1]:
                    title += "{:02d}".format(i)
                    break
            title += '-' + dat[2]
            url = tr.find_all('td')[1].find('a').get('href')
            embedparam = discord.Embed(title=title, description='[Download]({})'.format(url), color=0x0addd7)
        except:
            embedparam = discord.Embed(title='Sorry😔', description='Error fetching The Indian Express today', color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--yojana':
        res = requests.get('https://chahalacademy.com/free-downloads-yojana')
        soup = BeautifulSoup(res.text, 'html.parser')
        url = soup.find('a', string='Open File')
        embedparam = discord.Embed(title=url.get('title'),
                                   description='[Download]({})'.format('https://chahalacademy.com/' + url.get('href')),
                                   color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--server' and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_PRIVATE_CHANNEL:
        servers = []
        async for guild in bot.fetch_guilds(limit=150):
            servers.append(guild.name)
        embedparam = discord.Embed(title='Server List', description='\n'.join(servers), color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--channel' and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_PRIVATE_CHANNEL:
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

    elif message.content.startswith('--news') and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_SEND_CHANNEL:

        # hindu
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
        embedparam = discord.Embed(title=title, description='[Download]({})'.format(url), color=0x0addd7)

        # hindustan times
        htimes = requests.get('https://www.careerswave.in/hindustan-times-newspaper-download/',
                              headers={"User-Agent": "XY"})
        soup = BeautifulSoup(htimes.text, 'html.parser')
        embedparam.add_field(
            name='Hindustan Times Epaper ' + soup.find('tr', attrs={'data-row_id': '0'}).find('td').getText(),
            value='[Download]({})'.format(soup.find('tr', attrs={'data-row_id': '0'}).find_all('td')[1].getText()),
            inline=False)

        # indian express
        try:
            res = requests.get('https://iasbano.com/indian-express-upsc.php#download_the_hindu',
                               headers={"User-Agent": "XY"})
            soup = BeautifulSoup(res.text, 'html.parser')
            tr = soup.find_all('tr')[2]
            dat = tr.find_all('td')[0].getText().split()
            dat[1] = dat[1][:-1]
            title = 'The Indian Express Epaper ' + "{:02d}".format(int(dat[0])) + '-'
            for i in range(1, 13):
                if datetime.strptime(str(i), '%m').strftime('%B') == dat[1]:
                    title += "{:02d}".format(i)
                    break
            title += '-' + dat[2]
            url = tr.find_all('td')[1].find('a').get('href')
            embedparam.add_field(name=title, value='[Download]({})'.format(url), inline=False)
        except:
            embedparam.add_field(name='Sorry😔', value='Error fetching The Indian Express today', inline=False)
        for i in message.content.split()[1:]:
            await bot.get_channel(int(i)).send(embed=embedparam)
        print(message.content.split())


bot.loop.create_task(background_task())
bot.run(TOKEN)
