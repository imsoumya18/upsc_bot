from selenium import webdriver
from datetime import date
import calendar
import time
from idm import IDMan
import requests

downloader = IDMan()

date_serch = str(date.today().day) + ' ' + calendar.month_name[date.today().month] + ' ' + str(date.today().year)
print(date_serch)

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", '/downloads')
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
driver = webdriver.Firefox(firefox_profile=profile)

driver.get('https://dailyepaper.in/the-hindu-pdf-epaper-downloa-now/')
#
# time.sleep(5)
#
# driver.find_element_by_id('webpushr-deny-button').click()
url = driver.find_element_by_xpath("//p[contains(text(), '" + "11 May 2021" + "')]/a").get_attribute('href')
# downloader.download(url, "downloads", output=None, referrer=None, cookie=None, postData=None, user=None, password=None, confirm = False, lflag = None, clip=False)
# time.sleep(60)
# driver.find_element_by_xpath("//button[contains(text(), 'Download file')]").click()
response = requests.get(url)
with open('/data.pdf') as f:
    f.write(response.content)

driver.quit()

