import time
import pyperclip

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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

    def __init__(self, user="FridaySailer", mode=1):
        self.user = user
        if mode == 2:
            self.tweet_selector += ":nth-of-type(2)"
            self.second_tweet_selector = self.second_tweet_selector[0:-2] + "3" + self.second_tweet_selector[-1:]
            self.share_selector = self.tweet_selector + " " + "div[role='group'] div:nth-child(5)"
        self.activeDriver = self.driver()


    def driver(self):
        options = Options()
        options.add_argument("--window-size=1920,1200")


        driver = webdriver.Chrome(options=options)
        driver.get(self.base_url + self.user)
        return driver

    def awaitDriver(self):
        element = WebDriverWait(self.activeDriver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.second_tweet_selector))
        )

    def getLastTweetAction(self):
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
            action.pause(0.5)

            self.tweet_info["tweet"] = tweet.text
            self.tweet_info["tweet_url"] = pyperclip.paste()
            self.activeDriver.quit()
            return self.tweet_info

    def initAction(self, action):
        try:
            self.awaitDriver()
        finally:
            action()
