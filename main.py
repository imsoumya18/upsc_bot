import discord
import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, time, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials

TOKEN = 'TOKEN(str)'  # Bot Token
DEVELOPER_ID = 'DEVELOPER_ID(int)'  # Your Own ID
DEVELOPER_PRIVATE_CHANNEL = 'DEVELOPER_PRIVATE_CHANNEL_ID(int)'  # Developer's Private Channel ID
PUSH_LOGS_CHANNEL = 'PUSH_LOGS_CHANNEL_ID(int)'  # Push Logs Channel ID
DEVELOPER_SEND_CHANNEL = 'DEVELOPER_SEND_CHANNEL_ID(int)'  # Developer's Send Channel ID
REQUEST_CHANNEL = 'ADD_REQUESTS_CHANNEL_ID(int)'  # Add Requests Channel
COUNTDOWN_CHANNEL = 'COUNTDOWN_CHANNEL_ID(int)'  # Countdown Channel ID
THE_HINDU_CHANNELS = ['LIST OF THE HINDU CHANNEL IDS(int)']  # The Hindu Channel IDs
VISION_IAS_CHANNELS = ['LIST OF VISION IAS CHANNEL IDS(int)']  # Vision IAS Channel IDs
NEXT_IAS_CHANNELS = ['LIST OF NEXT IAS CHANNEL IDS(int)']  # Next IAS Channel IDs
ANS_WRITING_RECORD_CHANNEL = 'ANSWER WRITING RECORD CHANNEL(int)'  # Answer Writing Record Channel
WHEN = (datetime.combine(date.today(), time(7, 00, 00)) + timedelta(hours=-5, minutes=-30)).time()  # IST Time
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
secret_sheet = client.open('File Name').worksheet('Sheet Name')

bot = discord.Client()


def hindu():
    title = 'The Hindu Epaper ' + '-'.join(
        list(map(str, [datetime.today().day, datetime.today().month, datetime.today().year])))

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        res = requests.get('https://dailyepaper.in/home-point', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        th_page = soup.find_all('tbody')[1].find('a').get('href')
        res = requests.get(th_page, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        urls = soup.find_all('a')
        for i in urls:
            if i.getText() == 'Download':
                url1 = i.get('href')
                break
    except:
        url1 = ''

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        res = requests.get('https://dailyepaper.in/home-point', headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        th_page = soup.find_all('tbody')[1].find('a').get('href')
        res = requests.get(th_page, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        urls = soup.find_all('a')
        for i in urls:
            if i.getText() == 'Download':
                url2 = i.get('href')
                break
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


@bot.event
async def on_ready():
    print('Started')
    await bot.get_channel(PUSH_LOGS_CHANNEL).send('Pushed to Heroku just now!!')


async def called_once_a_day():
    await bot.wait_until_ready()

    # hindu
    vals = hindu()
    embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
    embedparam.add_field(name='Alternative Link', value='[Download]({})'.format(vals[2]))
    sent = []
    failed = []
    for i in THE_HINDU_CHANNELS:
        try:
            await bot.get_channel(i).send(embed=embedparam)
            sent.append(str(i))
        except:
            failed.append(str(i))
            continue
    embedparam2 = discord.Embed(title='Hindu sent to :white_check_mark:', description=' '.join(sent), color=0x0addd7)
    if len(failed) != 0:
        embedparam2.add_field(name='Failed :no_entry_sign:', value=' '.join(failed))
    await bot.get_channel(DEVELOPER_PRIVATE_CHANNEL).send(embed=embedparam2)

    # vision
    vals = vision_ca()
    if vals[0] != secret_sheet.cell(1, 1).value:
        embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
        sent = []
        failed = []
        for i in VISION_IAS_CHANNELS:
            try:
                await bot.get_channel(i).send(embed=embedparam)
                sent.append(str(i))
            except:
                failed.append(str(i))
                continue
        embedparam2 = discord.Embed(title='Vision IAS sent to :white_check_mark:', description=' '.join(sent),
                                    color=0x0addd7)
        if len(failed) != 0:
            embedparam2.add_field(name='Failed :no_entry_sign:', value=' '.join(failed))
        await bot.get_channel(DEVELOPER_PRIVATE_CHANNEL).send(embed=embedparam2)
        secret_sheet.delete_rows(1)
        secret_sheet.insert_row([vals[0]], 1)

    # next
    vals = next_mcq()
    if vals[0] != secret_sheet.cell(2, 1).value:
        embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
        sent = []
        failed = []
        for i in NEXT_IAS_CHANNELS:
            try:
                await bot.get_channel(i).send(embed=embedparam)
                sent.append(str(i))
            except:
                failed.append(str(i))
                continue
        embedparam2 = discord.Embed(title='Next IAS sent to :white_check_mark:', description=' '.join(sent),
                                    color=0x0addd7)
        if len(failed) != 0:
            embedparam2.add_field(name='Failed :no_entry_sign:', value=' '.join(failed))
        await bot.get_channel(DEVELOPER_PRIVATE_CHANNEL).send(embed=embedparam2)
        secret_sheet.delete_rows(2)
        secret_sheet.insert_row([vals[0]], 2)

    # countdown
    prelims = datetime(2023, 6, 1)
    today = datetime.today()
    await bot.get_channel(COUNTDOWN_CHANNEL).edit(name=str((prelims - today).days) + ' days to prelims!')


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
        embedparam.add_field(name='--next', value='Get latest Next IAS Monthly MCQ PDF', inline=False)
        embedparam.add_field(name='--add_hindu', value='Add the channel to get daily The Hindu', inline=False)
        embedparam.add_field(name='--add_vision', value='Add the channel to get monthly Vision IAS Magazine',
                             inline=False)
        embedparam.add_field(name='--add_next', value='Add the channel to get monthly Next IAS MCQ PDF', inline=False)
        if message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_PRIVATE_CHANNEL:
            embedparam.add_field(name='---------------Extras---------------', value='Extra commands for DEVELOPER ONLY',
                                 inline=False)
            embedparam.add_field(name='--ping', value='Check connection', inline=False)
            embedparam.add_field(name='--servers', value='Get all servers list', inline=False)
            embedparam.add_field(name='--send_hindu <Channel ID(s)>', value='Send The Hindu to channels immediately',
                                 inline=False)
            embedparam.add_field(name='--send_vision <Channel ID(s)>',
                                 value='Send Vision IAS magazine to channels immediately',
                                 inline=False)
            embedparam.add_field(name='--send_next <Channel ID(s)>',
                                 value='Send Next IAS MCQ to channels immediately',
                                 inline=False)
            embedparam.add_field(name='--resend',
                                 value='Resend all to all channels immediately',
                                 inline=False)
            embedparam.add_field(name='--send_msg [<Channel ID(s)>] <message>',
                                 value='Send message to channels immediately', inline=False)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--hindu':
        # hindu
        vals = hindu()
        embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
        embedparam.add_field(name='Alternative Link', value='[Download]({})'.format(vals[2]))
        embedparam2 = discord.Embed(title='The Hindu Request :white_check_mark:', description=str(message.channel.id),
                                    color=0x0addd7)
        embedparam2.add_field(name='Requested By',
                              value=str(message.author.name) + '#' + str(message.author.discriminator))
        embedparam2.add_field(name='Server name', value=str(message.author.guild.name))
        await message.channel.send(embed=embedparam)
        await bot.get_channel(DEVELOPER_PRIVATE_CHANNEL).send(embed=embedparam2)
        await message.delete()

    elif message.content.lower() == '--vision':
        # vision
        vals = vision_ca()
        embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
        embedparam2 = discord.Embed(title='Vision IAS Request :white_check_mark:', description=str(message.channel.id),
                                    color=0x0addd7)
        embedparam2.add_field(name='Requested By',
                              value=str(message.author.name) + '#' + str(message.author.discriminator))
        embedparam2.add_field(name='Server name', value=str(message.author.guild.name))
        await message.channel.send(embed=embedparam)
        await bot.get_channel(DEVELOPER_PRIVATE_CHANNEL).send(embed=embedparam2)
        await message.delete()

    elif message.content.lower() == '--next':
        # next
        vals = next_mcq()
        embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
        embedparam2 = discord.Embed(title='Next IAS Request :white_check_mark:', description=str(message.channel.id),
                                    color=0x0addd7)
        embedparam2.add_field(name='Requested By',
                              value=str(message.author.name) + '#' + str(message.author.discriminator))
        embedparam2.add_field(name='Server name', value=str(message.author.guild.name))
        await message.channel.send(embed=embedparam)
        await bot.get_channel(DEVELOPER_PRIVATE_CHANNEL).send(embed=embedparam2)
        await message.delete()

    elif message.content.lower() == '--add_hindu':
        embedparam = discord.Embed(title='The Hindu Add Request', description=str(message.channel.id), color=0x0addd7)
        embedparam.add_field(name='Requested By',
                             value=str(message.author.name) + '#' + str(message.author.discriminator))
        embedparam.add_field(name='Server name', value=str(message.author.guild.name))
        await bot.get_channel(REQUEST_CHANNEL).send(embed=embedparam)
        embedparam = discord.Embed(title='Channel Added',
                                   description='This Hindu will be sent daily in this channel as soon as developer approves',
                                   color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--add_vision':
        embedparam = discord.Embed(title='Vision IAS Add Request', description=str(message.channel.id), color=0x0addd7)
        embedparam.add_field(name='Requested By',
                             value=str(message.author.name) + '#' + str(message.author.discriminator))
        embedparam.add_field(name='Server name', value=str(message.author.guild.name))
        await bot.get_channel(REQUEST_CHANNEL).send(embed=embedparam)
        embedparam = discord.Embed(title='Channel Added',
                                   description='Vision IAS Magazine will be sent monthly in this channel as soon as developer approves',
                                   color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--add_next':
        embedparam = discord.Embed(title='Next IAS Add Request', description=str(message.channel.id), color=0x0addd7)
        embedparam.add_field(name='Requested By',
                             value=str(message.author.name) + '#' + str(message.author.discriminator))
        embedparam.add_field(name='Server name', value=str(message.author.guild.name))
        await bot.get_channel(REQUEST_CHANNEL).send(embed=embedparam)
        embedparam = discord.Embed(title='Channel Added',
                                   description='Next IAS MCQ will be sent monthly in this channel as soon as developer approves',
                                   color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.lower() == '--ping' and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_PRIVATE_CHANNEL:
        await message.channel.send('--pong')

    elif message.content.lower() == '--servers' and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_PRIVATE_CHANNEL:
        servers = []
        i = 0
        async for guild in bot.fetch_guilds(limit=150):
            servers.append(str(i + 1) + '. ' + repr(guild))
            i += 1
        embedparam = discord.Embed(title='Server List', description='\n'.join(servers), color=0x0addd7)
        await message.channel.send(embed=embedparam)

    elif message.content.startswith(
            '--send_hindu') and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_SEND_CHANNEL:
        # hindu
        vals = hindu()
        embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
        embedparam.add_field(name='Alternative Link', value='[Download]({})'.format(vals[2]))
        sent = []
        failed = []
        for i in message.content.split()[1:]:
            try:
                await bot.get_channel(int(i)).send(embed=embedparam)
                sent.append(i)
            except:
                failed.append(i)
                continue
        embedparam2 = discord.Embed(title='Hindu sent to :white_check_mark:', description=' '.join(sent),
                                    color=0x0addd7)
        if len(failed) != 0:
            embedparam2.add_field(name='Failed :no_entry_sign:', value=' '.join(failed))
        await bot.get_channel(DEVELOPER_PRIVATE_CHANNEL).send(embed=embedparam2)

    elif message.content.startswith(
            '--send_vision') and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_SEND_CHANNEL:
        # vision
        vals = vision_ca()
        embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
        sent = []
        failed = []
        for i in message.content.split()[1:]:
            try:
                await bot.get_channel(int(i)).send(embed=embedparam)
                sent.append(i)
            except:
                failed.append(i)
                continue
        embedparam2 = discord.Embed(title='Vision IAS sent to :white_check_mark:', description=' '.join(sent),
                                    color=0x0addd7)
        if len(failed) != 0:
            embedparam2.add_field(name='Failed :no_entry_sign:', value=' '.join(failed))
        await bot.get_channel(DEVELOPER_PRIVATE_CHANNEL).send(embed=embedparam2)

    elif message.content.startswith(
            '--send_next') and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_SEND_CHANNEL:
        # next
        vals = next_mcq()
        embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
        sent = []
        failed = []
        for i in message.content.split()[1:]:
            try:
                await bot.get_channel(int(i)).send(embed=embedparam)
                sent.append(i)
            except:
                failed.append(i)
                continue
        embedparam2 = discord.Embed(title='Next IAS sent to :white_check_mark:', description=' '.join(sent),
                                    color=0x0addd7)
        if len(failed) != 0:
            embedparam2.add_field(name='Failed :no_entry_sign:', value=' '.join(failed))
        await bot.get_channel(DEVELOPER_PRIVATE_CHANNEL).send(embed=embedparam2)

    elif message.content.startswith('--resend') and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_SEND_CHANNEL:
        # resend all
        # hindu
        vals = hindu()
        embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
        embedparam.add_field(name='Alternative Link', value='[Download]({})'.format(vals[2]))
        sent = []
        failed = []
        for i in THE_HINDU_CHANNELS:
            try:
                await bot.get_channel(i).send(embed=embedparam)
                sent.append(str(i))
            except:
                failed.append(str(i))
                continue
        embedparam2 = discord.Embed(title='Hindu sent to :white_check_mark:', description=' '.join(sent),
                                    color=0x0addd7)
        if len(failed) != 0:
            embedparam2.add_field(name='Failed :no_entry_sign:', value=' '.join(failed))
        await bot.get_channel(DEVELOPER_PRIVATE_CHANNEL).send(embed=embedparam2)

        # vision
        vals = vision_ca()
        if vals[0] != secret_sheet.cell(1, 1).value:
            embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
            sent = []
            failed = []
            for i in VISION_IAS_CHANNELS:
                try:
                    await bot.get_channel(i).send(embed=embedparam)
                    sent.append(str(i))
                except:
                    failed.append(str(i))
                    continue
            embedparam2 = discord.Embed(title='Vision IAS sent to :white_check_mark:', description=' '.join(sent),
                                        color=0x0addd7)
            if len(failed) != 0:
                embedparam2.add_field(name='Failed :no_entry_sign:', value=' '.join(failed))
            await bot.get_channel(DEVELOPER_PRIVATE_CHANNEL).send(embed=embedparam2)
            secret_sheet.delete_rows(1)
            secret_sheet.insert_row([vals[0]], 1)

        # next
        vals = next_mcq()
        if vals[0] != secret_sheet.cell(2, 1).value:
            embedparam = discord.Embed(title=vals[0], description='[Download]({})'.format(vals[1]), color=0x0addd7)
            sent = []
            failed = []
            for i in NEXT_IAS_CHANNELS:
                try:
                    await bot.get_channel(i).send(embed=embedparam)
                    sent.append(str(i))
                except:
                    failed.append(str(i))
                    continue
            embedparam2 = discord.Embed(title='Next IAS sent to :white_check_mark:', description=' '.join(sent),
                                        color=0x0addd7)
            if len(failed) != 0:
                embedparam2.add_field(name='Failed :no_entry_sign:', value=' '.join(failed))
            await bot.get_channel(DEVELOPER_PRIVATE_CHANNEL).send(embed=embedparam2)
            secret_sheet.delete_rows(2)
            secret_sheet.insert_row([vals[0]], 2)

    elif message.content.startswith(
            '--send_msg') and message.author.id == DEVELOPER_ID and message.channel.id == DEVELOPER_SEND_CHANNEL:
        msg = message.content[message.content.find(']') + 2:]
        channels = message.content[message.content.find('[') + 1: message.content.find(']')].split(', ')
        for i in channels:
            await bot.get_channel(int(i)).send(msg)


bot.loop.create_task(background_task())
bot.run(TOKEN)
