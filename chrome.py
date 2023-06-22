import time
import pyperclip

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

class ScrapeUserPage:
    user = ""
    base_url = "https://twitter.com/"
    tweet_info = {}
    tweet_selector = "[data-testid='cellInnerDiv']"
    second_tweet_selector = tweet_selector + ":nth-of-type(2)"
    share_selector = tweet_selector + " " + "div[role='group'] div:nth-child(5)"
    link_selector = "div[data-testid='Dropdown'] div"

    activeDriver = None

    def __init__(self, user="FridaySailer"):
        self.user = user
        self.activeDriver = self.driver()


    def driver(self):
        options = Options()
        options.add_argument("--window-size=1240,666")


        driver = webdriver.Chrome(options=options)
        driver.get(self.base_url + self.user)
        return driver

    def awaitDriver(self):
        element = WebDriverWait(self.activeDriver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.second_tweet_selector))
        )

    def getLastTweetURLAction(self):
            action = ActionChains(self.activeDriver)
            tweet = self.activeDriver.find_element(By.CSS_SELECTOR, self.tweet_selector)
            second_tweet = self.activeDriver.find_element(By.CSS_SELECTOR, self.second_tweet_selector)
            share_btn = self.activeDriver.find_element(By.CSS_SELECTOR, self.share_selector)

            # need to scroll into view to click share btn
            action.scroll_to_element(second_tweet)
            action.pause(0.5)
            action.click(share_btn)
            action.pause(0.5)

            action.click()
            action.perform()
            self.tweet_info["text"] = tweet.text
            self.tweet_info["tweet_url"] = pyperclip.paste()
            self.activeDriver.quit()
            return self.tweet_info

    def initAction(self, action):
        try:
            self.awaitDriver()
        finally:
            action()

users = ["fridaysailer", "elonmusk", "realdonaldtrump"]
for user in users:
    scraper = ScrapeUserPage(user)
    scraper.initAction(scraper.getLastTweetURLAction)
    print(scraper.tweet_info["text"])
    print("\n")
