import discord
import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime, time, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = 'TOKEN(str)'  # Bot Token
DEVELOPER_ID = 'DEVELOPER_ID(int)'  # Your Own ID
DEVELOPER_PRIVATE_CHANNEL = 'DEVELOPER_PRIVATE_CHANNEL_ID(int)'  # Developer's Private Channel ID
PUSH_LOGS_CHANNEL = 'PUSH_LOGS_CHANNEL_ID(int)'  # Push Logs Channel ID
DEVELOPER_SEND_CHANNEL = 'DEVELOPER_SEND_CHANNEL_ID(int)'  # Developer's Send Channel ID
COUNTDOWN_CHANNEL = 'COUNTDOWN_CHANNEL_ID(int)'  # Countdown Channel ID
THE_HINDU_CHANNELS = ['LIST OF THE HINDU CHANNEL IDS(int)']  # The Hindu Channel IDs
VISION_IAS_CHANNELS = ['LIST OF VISION IAS CHANNEL IDS(int)']  # Vision IAS Channel IDs
ANS_WRITING_RECORD_CHANNEL = 'ANSWER WRITING RECORD CHANNEL(int)'  # Answer Writing Record Channel
WHEN = time(1, 30, 0)  # UTC Time
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open('File Name').worksheet('Sheet Name')
secret_sheet = client.open('File Name').worksheet('Sheet Name')

bot = discord.Client()


# def hindu():
#     d = str(datetime.now().day)
#     if len(d) == 1:
#         d = '0' + d
#     m = datetime.strptime(str(datetime.now().month), '%m').strftime('%b').lower()
#     y = str(datetime.now().year)
#     res = requests.get('https://dailyepaper.in/the-hindu-pdf-epaper-free-' + d + '-' + m + '-' + y)
#     soup = BeautifulSoup(res.text, 'html.parser')
#     parts = soup.find_all('span')[28].getText().split()
#     title = 'The Hindu Epaper ' + parts[0] + '-'
#     for i in range(1, 13):
#         if datetime.strptime(str(i), '%m').strftime('%b') == parts[1]:
#             title += "{:02d}".format(i)
#             break
#     title += '-' + parts[2][:-1]
#     url = soup.find_all('a')[16].get('href')
#     return [title, url]

def hindu():
    m = datetime.strptime(str(datetime.now().month), '%m').strftime('%b').lower()
    y = str(datetime.now().year)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
    res = requests.get('https://fresherwave.com/the-hindu-pdf-free-' + m + '-' + y, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    dnld = soup.find('tr', attrs={'data-row_id': '0'})
    title = 'The Hindu Epaper ' + dnld.find_all('td')[0].getText()
    url = dnld.find_all('td')[1].getText()
    return [title, url]


@bot.event
async def on_ready():
    print('Started')
    await bot.get_channel(PUSH_LOGS_CHANNEL).send('Pushed to Heroku just now!!')


async def called_once_a_day():
    await bot.wait_until_ready()

    # countdown
    prelims = datetime(2023, 6, 1)
    today = datetime.today()
    await bot.get_channel(COUNTDOWN_CHANNEL).edit(name=str((prelims - today).days) + ' days to prelims!')

    # hindu
    vals = hindu()
    embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
    for i in THE_HINDU_CHANNELS:
        await bot.get_channel(i).send(embed=embedparam)

    # vision
    res = requests.get('http://www.visionias.in/resources/current_affairs.php?c=ca')
    soup = BeautifulSoup(res.text, 'html.parser')
    title = 'Vision IAS Current Affairs ' + soup.find('a').getText().strip()
    url = soup.find('a').get('href')
    if title != secret_sheet.cell(1, 1).value:
        embedparam = discord.Embed(title=title, description='[Download]({})'.format(url), color=0x0addd7)
        for i in VISION_IAS_CHANNELS:
            await bot.get_channel(i).send(embed=embedparam)
        secret_sheet.delete_rows(1)
        secret_sheet.insert_row([title], 1)


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
        embedparam.add_field(name='--hindu', value='Get latest The Hindu newspaper PDF', inline=False)
        embedparam.add_field(name='--vision', value='Get latest Vision IAS Current Affairs PDF', inline=False)
        if message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_PRIVATE_CHANNEL:
            embedparam.add_field(name='---------------Extras---------------', value='Extra commands for DEVELOPER ONLY',
                                 inline=False)
            embedparam.add_field(name='--ping', value='Check connection', inline=False)
            embedparam.add_field(name='--servers', value='Get all servers list', inline=False)
            embedparam.add_field(name='--q <Question No>', value='Update Mains Answer Writing in Spreadsheet',
                                 inline=False)
            embedparam.add_field(name='--send_hindu <Channel ID(s)>', value='Send The Hindu to channels immediately',
                                 inline=False)
            embedparam.add_field(name='--send_vision <Channel ID(s)>',
                                 value='Send Vision IAS magazine to channels immediately',
                                 inline=False)
            embedparam.add_field(name='--send_msg [<Channel ID(s)>] <message>',
                                 value='Send message to channels immediately', inline=False)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--hindu':
        vals = hindu()
        embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
        await message.channel.send(embed=embedparam)
        await message.delete()

    elif message.content.lower() == '--vision':
        res = requests.get('http://www.visionias.in/resources/current_affairs.php?c=ca')
        soup = BeautifulSoup(res.text, 'html.parser')
        title = 'Vision IAS Current Affairs ' + soup.find('a').getText().strip()
        url = soup.find('a').get('href')
        embedparam = discord.Embed(title=title, description='[Download]({})'.format(url), color=0x0addd7)
        await message.channel.send(embed=embedparam)
        await message.delete()

    elif message.content.lower() == '--ping' and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_PRIVATE_CHANNEL:
        await message.channel.send('--pong')

    elif message.content.lower() == '--servers' and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_PRIVATE_CHANNEL:
        servers = []
        async for guild in bot.fetch_guilds(limit=150):
            servers.append(guild.name)
        embedparam = discord.Embed(title='Server List', description='\n'.join(servers), color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.startswith(
            '--q') and message.author.id == DEVELOPER_ID and message.channel.id == ANS_WRITING_RECORD_CHANNEL:
        x = int(message.content.split()[1])
        res = requests.get('https://www.drishtiias.com/mains-practice-question/question-' + str(x))
        soup = BeautifulSoup(res.text, 'html.parser')
        paper = soup.find('span', {'class': 'paper-span'}).find_all('a')[0].getText().strip()
        paper = paper.split()[0] + paper.split()[2]
        topic = soup.find('span', {'class': 'paper-span'}).find_all('a')[1].getText().strip()
        if str(x) in sheet.col_values(1)[2:]:
            embedparam = discord.Embed(title='Question Already Done', description=', '.join(sheet.col_values(1)[2:]),
                                       color=0x0addd7)
        else:
            i = 3
            while x > int(sheet.cell(i, 1).value):
                i += 1
                if sheet.cell(i, 1).value is None:
                    break
            data = [x, paper, topic]
            sheet.insert_row(data, i)
            embedparam = discord.Embed(title='All Questions Till Now', description=', '.join(sheet.col_values(1)[2:]),
                                       color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.startswith(
            '--send_hindu') and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_SEND_CHANNEL:
        # hindu
        vals = hindu()
        embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
        for i in message.content.split()[1:]:
            await bot.get_channel(int(i)).send(embed=embedparam)

    elif message.content.startswith(
            '--send_vision') and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_SEND_CHANNEL:
        # vision
        res = requests.get('http://www.visionias.in/resources/current_affairs.php?c=ca')
        soup = BeautifulSoup(res.text, 'html.parser')
        title = 'Vision IAS Current Affairs ' + soup.find('a').getText().strip()
        url = soup.find('a').get('href')
        embedparam = discord.Embed(title=title, description='[Download]({})'.format(url), color=0x0addd7)
        for i in message.content.split()[1:]:
            await bot.get_channel(int(i)).send(embed=embedparam)

    elif message.content.startswith(
            '--send_msg') and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_SEND_CHANNEL:
        msg = message.content[message.content.find(']') + 2:]
        channels = message.content[message.content.find('[') + 1: message.content.find(']')].split(', ')
        for i in channels:
            await bot.get_channel(int(i)).send(msg)


bot.loop.create_task(background_task())
bot.run(TOKEN)
