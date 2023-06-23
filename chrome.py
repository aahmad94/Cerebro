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

    activeDriver = None

    def __init__(self, user="FridaySailer", mode=1):
        self.user = user
        if mode == 2:
            self.tweet_selector += ":nth-of-type(2)"
        self.activeDriver = self.driver()


    def driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--window-size=1920,1200")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(options=options)
        driver.get(self.base_url + self.user)
        return driver

    def awaitDriver(self):
        element = WebDriverWait(self.activeDriver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.tweet_selector))
        )

    def getLastTweetAction(self):
            action = ActionChains(self.activeDriver)
            tweet = self.activeDriver.find_element(By.CSS_SELECTOR, self.tweet_selector)
            self.tweet_info["tweet"] = tweet.text
            action.click(tweet)
            action.perform()
            self.tweet_info["tweet_url"] = self.activeDriver.execute_script("return window.location.href")
            self.activeDriver.quit()
            return self.tweet_info

    def initAction(self, action):
        try:
            self.awaitDriver()
        finally:
            action()
