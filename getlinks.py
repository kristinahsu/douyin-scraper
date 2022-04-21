from selenium import webdriver
from bs4 import BeautifulSoup
import time, datetime

#"https://www.douyin.com/search/%E8%80%81%E4%BA%BA"
#url = "https://www.douyin.com/search/%E8%80%81%E4%BA%BA?enter_from=search_result&publish_time=0&sort_type=0&source=normal_search&type=video"
#url = "https://www.douyin.com/search/%E4%B8%B4%E7%BB%88%E5%85%B3%E6%80%80?source=normal_search&aid=409d8872-337d-4e45-9d61-897dc969ef06&enter_from=recommend&gid=7076738369971145998"
url = 'https://www.douyin.com/search/%E4%B8%B4%E7%BB%88%E5%85%B3%E6%80%80?publish_time=0&sort_type=0&source=switch_tab&type=video'

# use a chrome core. https://chromedriver.chromium.org/downloads
bot = webdriver.Chrome(executable_path="assets/chromedriver")
bot.get(url)

f = open("assets/links.csv", "a", encoding="utf-8")
f.write('user_name, user_page, vid_title, vid_link \n')
start = datetime.datetime.now()
time_limit = 120
texts = []
count = 1

while count != 0: 
    time.sleep(10)
    #bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(bot.page_source, 'html.parser')
    vids = soup.find("ul", {'class' : 'qrvPn3bC H2eeMN3S'}).findChildren("li")
    count = len(vids)
    if int((datetime.datetime.now() - start).seconds) >= time_limit: # if longer than a minute, then stop scrolling.
        break
    for vid in vids:
        try:
            user_page = vid.find('div', {'class': 'aKgCOHgk'}).a['href'].strip()
            user_name = vid.find('p', {'class':'Vlezrry7 OfYxdv9U pcIyTAK4'}).text.strip()
            vid_title = vid.find('div', {'class':'Z6bzLUc0 UETFf9cv'}).img['alt'].strip()
            vid_link = vid.find("div", {'class':'xv7dvZKu'}).a['href'].strip()
            
            record = '%s, %s, %s, %s \n' % (user_name, user_page, vid_title, vid_link)
            if (vid_title not in texts):
                f.write(record)
            texts.append(vid_title)
        except:
            pass
        count -= 1

f.close()
bot.close()
print("finished")

if __name__ == "__main__":
    pass