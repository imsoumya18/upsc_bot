import discord
import requests
from bs4 import BeautifulSoup
from datetime import datetime

bot = discord.Client()


@bot.event
async def on_ready():
    print('started')


@bot.event
async def on_message(message):
    if message.content == 'ie':
        hindu = requests.get('https://www.visioniascurrentaffairs.com')
        soup = BeautifulSoup(hindu.text, 'html.parser')
        url = soup.find('a', attrs={'class': 'green'})
        embedparam = discord.Embed(title=url.getText(), description='[Download]({})'.format(url.get('href')),
                                   color=0x0addd7)
        htimes = requests.get('https://www.careerswave.in/hindustan-times-newspaper-download/',
                              headers={"User-Agent": "XY"})
        soup = BeautifulSoup(htimes.text, 'html.parser')
        embedparam.add_field(
            name='Hindustan Times Epaper ' + soup.find('tr', attrs={'data-row_id': '0'}).find('td').getText(),
            value='[Download]({})'.format(soup.find('tr', attrs={'data-row_id': '0'}).find_all('td')[1].getText()),
            inline=False)
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
            pass

        await message.channel.send(embed=embedparam)


bot.run('ODQzNTU1NjkzMjA1NTIwNDM0.YKFkdQ.mk8DioskKq_D-9dxBI8eUzt_svk')
