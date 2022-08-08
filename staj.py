from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
import time
import csv
import pandas as pd


class TwitterBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = webdriver.Chrome('chromedriver')

    def login(self):
        bot = self.bot
        bot.get('https://twitter.com/login')
        time.sleep(1)
        email = bot.find_element_by_name('session[username_or_email]')
        password = bot.find_element_by_name('session[password]')
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(2)

    def export_excel(self):
        my_csv = pd.read_csv(
            "tweetler.csv")
        my_csv.to_excel("tweetler_excel.xlsx")

    def cek_twwet(self, hashtag):
        bot = self.bot
        bot.get('https://twitter.com/search?q='+hashtag+'&src=typed_query')

        # bot.get('https://twitter.com/search?q='+hashtag +
        #         '&src=trend_click&f=live&vertical=trends')
        # bot.get(
        #     'https://twitter.com/wavesducks/status/1410932491762999299/retweets/with_comments')
        time.sleep(3)

        file = open("tweetler.csv", "w", encoding="utf-8")
        writer = csv.writer(file)
        writer.writerow(["TWEET", "KULLANICI", "ID", "LIKE",
                        "REPLY", "RETWEET"])

        SCROLL_PAUSE_TIME = 4

        last_height = bot.execute_script(
            "return document.body.scrollHeight")

        while True:
           # o anki scrollda tüm tweetleri çekiyor.(Kısmen)

            tweets = bot.find_elements_by_tag_name("div[data-testid='tweet']")
            for i in tweets:
                # Bu for döngüsü içinde o anki scrolldaki tüm tweetlerin tek tek sınıflandırıyor ve csv dosyasına yazıyor.
                kullanici = i.find_element_by_tag_name(
                    "div[class='css-901oao css-bfa6kz r-18jsvk2 r-1qd0xha r-a023e6 r-b88u0q r-rjixqe r-bcqeeo r-1udh08x r-3s2u2q r-qvutc0']").text
                kullanici_id = i.find_element_by_tag_name(
                    "div[class='css-901oao css-bfa6kz r-14j79pv r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0']").text

                tweet = i.find_element_by_tag_name(
                    "div[class='css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']").text
                # tweet = i.find_element_by_tag_name(
                #     "div[lang='ru'; dir='auto']").text
                # tweet = i.find_element_by_xpath(
                #     "//div[@lang and @dir='auto']").text

                if tweet == "":
                    tweet = "BOŞ"

                yorum_sayisi = i.find_element_by_tag_name(
                    "div[data-testid='reply']").text

                if yorum_sayisi == "":
                    yorum_sayisi = "0"

                try:
                    retweet_sayisi = i.find_element_by_tag_name(
                        "div[data-testid='unretweet']").text
                    if retweet_sayisi == "":
                        retweet_sayisi = "0"

                except(selenium.common.exceptions.NoSuchElementException):
                    retweet_sayisi = i.find_element_by_tag_name(
                        "div[data-testid='retweet']").text
                    if retweet_sayisi == "":
                        retweet_sayisi = "0"

                try:
                    begeni_sayisi = i.find_element_by_tag_name(
                        "div[data-testid='unlike']").text
                    if begeni_sayisi == "":
                        begeni_sayisi = "0"

                except(selenium.common.exceptions.NoSuchElementException):
                    begeni_sayisi = i.find_element_by_tag_name(
                        "div[data-testid='like']").text
                    if begeni_sayisi == "":
                        begeni_sayisi = "0"

                writer.writerow([tweet, kullanici, kullanici_id, begeni_sayisi,
                                yorum_sayisi, retweet_sayisi])
                print("MESAJ: "+tweet+" KULLANICI: " + kullanici+" İD: " + kullanici_id+" LIKE: " + begeni_sayisi+" YORUM: " +
                      yorum_sayisi+" RETWEET: " + retweet_sayisi)
                print("----------")
                # Scroll down to bottom

            bot.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(SCROLL_PAUSE_TIME)

            new_height = bot.execute_script(
                "return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


twitter = TwitterBot('[ID GİRİNİZ]', '[ŞİFRE GİRİNZ]')
twitter.login()
twitter.cek_twwet('%23ayt2021')
# twitter.cek_twwet('Tarkan')
twitter.export_excel()
