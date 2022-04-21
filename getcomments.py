# created on Nov 23, 2021
# @author:          Kristina Hsu
# @email:           kcch@uw.edu
# @organization:    Department of Geography, University of Washington, Seattle
# @description:     Get comments of a specific video using a web crawler

from reprlib import recursive_repr
import requests
import time
import pandas as pd
import numpy as np
from selenium import webdriver
from bs4 import BeautifulSoup
import time, datetime, json
import sqlite3
import re
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

#url = 'https://www.douyin.com/video/7008807248432614693?modeFrom=userPost&secUid=MS4wLjABAAAA41IBn7lM0-2gLd2kWlyc4fhZAZ_pbakaFwlgNDOPErRS-YIqWUHlbDojXJj8L0Gb'
url = "https://www.douyin.com/video/6971364659605622027"

bot = webdriver.Chrome(executable_path="assets/chromedriver")
bot.get(url)

f = open("assets/video1.csv", "a", encoding="utf-8")
f.write('date, user_name, likes, comment \n')
start = datetime.datetime.now()
time_limit = 600
texts = []
count = 0

#time.sleep(10) # 過驗證

while (count < 537): 
    time.sleep(5)
    bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # expand comments

    try:
        while bot.find_element_by_class_name("N10j3PcL"):
            buttons = bot.find_elements_by_class_name("N10j3PcL") 
            for button in buttons:
                bot.implicitly_wait(3)
                ActionChains(bot).move_to_element(button).click(button).perform()
    except:
        pass

    soup = BeautifulSoup(bot.page_source, 'html.parser')
    body = soup.find('div', {'class' : 'mQjJJImN HO1_ywVX'}) # 留言處
    #temp = body.findChild('div')
    comments = soup.find_all("div", {'class' : 'CDx534Ub'}) # comment group
    #temp = body.find_all('div', recursive=False)[-1]
    #comments1 = temp.find_all('div', {'class': 'CDx534Ub'})
    #print(len(comments), len(comments1))

    if int((datetime.datetime.now() - start).seconds) >= time_limit: # if longer than 10 minute, then stop scrolling.
        break
    
    for c in comments:
        # main comment 
        try:
            date = c.find('p', {'class': 'dn67MYhq'}).text
            user_name = c.find('span', {'class': 'Nu66P_ba'}).text
            like_num = c.find('p', {'class' : 'eJuDTubq'}).text
            dat = c.find('span', {'class' : "VD5Aa1A1"}).text
            record = '%s, %s, %s, %s \n' % (date, user_name, like_num, dat)
            if ((date, user_name, like_num, dat) not in texts):
                f.write(record)
                #print(record) # main comment
                count += 1
                print("count", count)
                print(len(texts))
                texts.append((date, user_name, like_num, dat))
        except:
            pass

f.close()
bot.close()
print("finished")
print(count)

if __name__ == "__main__":
    pass