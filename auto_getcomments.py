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


url = 'https://www.douyin.com/video/7008807248432614693?modeFrom=userPost&secUid=MS4wLjABAAAA41IBn7lM0-2gLd2kWlyc4fhZAZ_pbakaFwlgNDOPErRS-YIqWUHlbDojXJj8L0Gb'
#'https://www.douyin.com/video/7014499168886508838'

file = pd.read_csv('assets/links.csv')[24:]
df = file.reset_index(drop = True)

f1 = open("assets/vid_stats.csv", "a", encoding="utf-8")
f1.write('vid_idx,vid_name,vid_link,heart_num,comment_num,star_num\n')

f = open("assets/comments.csv", "a", encoding="utf-8")
f.write('vid_idx,date,user_name,likes,comment')

bot = webdriver.Chrome(executable_path="assets/chromedriver")
for i in range(1): #len(df)):
    time.sleep(5)
    bot.get('https:' + df['vid_link'][i])

    start = datetime.datetime.now()
    time_limit = 300
    texts = []
    count = 0

    #time.sleep(10) # 過驗證

    soup = BeautifulSoup(bot.page_source, 'html.parser')
    stats = soup.find_all("span", {'class' : 'CE7XkkTw'})
    f1.write('%s,%s,%s,%s\n' % (i, stats[0].text, stats[1].text, stats[2].text))

    
    while (count < (int(stats[1].text) * 0.9)): #暂时没有更多评论
        time.sleep(5)
        bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # expand comments
        try:
            while bot.find_element_by_class_name("zeyRYM2J"):
                buttons = bot.find_elements_by_class_name("zeyRYM2J") 
                for button in buttons:
                    bot.implicitly_wait(3)
                    ActionChains(bot).move_to_element(button).click(button).perform()

            while bot.find_element_by_class_name("N10j3PcL"):
                print("click once")
                buttons = bot.find_elements_by_class_name("N10j3PcL") 
                for button in buttons:
                    bot.implicitly_wait(3)
                    ActionChains(bot).move_to_element(button).click(button).perform()
        except:
            pass

        soup = BeautifulSoup(bot.page_source, 'html.parser')
        body = soup.find('div', {'class' : 'mQjJJImN HO1_ywVX'}) # 留言處
        comments = soup.find_all("div", {'class' : 'CDx534Ub'}) # comment group

        if int((datetime.datetime.now() - start).seconds) >= time_limit: # if longer than 5 minute, then stop scrolling.
            break
        
        for c in comments:
            try:
                date = c.find('p', {'class': 'dn67MYhq'}).text
                user_name = c.find('span', {'class': 'Nu66P_ba'}).text
                like_num = c.find('p', {'class' : 'eJuDTubq'}).text
                dat = c.find('span', {'class' : "VD5Aa1A1"}).text

                record = '%s,%s,%s,%s,%s\n' % (i, date, user_name, like_num, dat)
                print("ready")
                if ((date, user_name, like_num, dat) not in texts):
                    f.write(record)
                    count += 1
                    texts.append((date, user_name, like_num, dat))
            except:
                pass
    

f.close()


bot.close()
print("finished")
print(count)

if __name__ == "__main__":
    pass