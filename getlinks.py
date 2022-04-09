from selenium import webdriver
from bs4 import BeautifulSoup
import time, datetime

#"https://www.douyin.com/search/%E8%80%81%E4%BA%BA"
url = "https://www.douyin.com/search/%E8%80%81%E4%BA%BA?enter_from=search_result&publish_time=0&sort_type=0&source=normal_search&type=video"

# use a chrome core. https://chromedriver.chromium.org/downloads
bot = webdriver.Chrome(executable_path="assets/chromedriver")
bot.get(url)

f = open("assets/links.csv", "a", encoding="utf-8")
f.write('user_name, user_page, vid_title, vid_link \n')
start = datetime.datetime.now()
time_limit = 60
texts = []

while len(bot.find_elements_by_xpath('//div[contains(text(), "登录后可查看更多精彩视频")]')) != 1: 
    time.sleep(5)
    bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    soup = BeautifulSoup(bot.page_source, 'html.parser')
    vids = soup.find("ul", {'class' : 'fbe2b2b02040793723b452dc2de2b770-scss _924e252b5702097b657541b9e3b21448-scss'}).findChildren("li")
    if int((datetime.datetime.now() - start).seconds) >= time_limit: # if longer than a minute, then stop scrolling.
        break
    for vid in vids:
        try:
            dat = vid.div.a
            vid_link = dat['href']
            vid_title = dat.div.div.img['alt']
            user_page = vid.find("div", {'class': 'd8d25680ae6956e5aa7807679ce66b7e-scss'}).a['href']
            user_name = vid.find("p", {'class': '_31dc42fa6181927e1afa821a0db10ed0-scss _7cfe89a4f1868679513e50ad5cf7215c-scss d7e9f4babb665565265e75abf8b7a49f-scss'}).span.span.span.span.span.text
            record = '%s, %s, %s, %s \n' % (user_name, user_page, vid_title, vid_link)
            if (vid_title not in texts):
                f.write(record)
            texts.append(vid_title)
        except:
            pass

f.close()
bot.close()
print("finished")

if __name__ == "__main__":
    pass