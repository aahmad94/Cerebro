import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class ParseTwitter:
    user = ""
    base_url = "https://twitter.com/"
    tweet_info = {}
    tweet_selector = "[data-testid='cellInnerDiv']"

    active_driver = None

    def __init__(self, user="FridaySailer"):
        self.user = user
        self.active_driver = self.driver()


    def driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(options=options)
        driver.get(self.base_url + self.user)
        return driver

    def awaitDriver(self):
        element = WebDriverWait(self.active_driver, 30).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"{self.tweet_selector}:nth-of-type(3)"))
        )

    def getLastTweetAction(self):
            action = ActionChains(self.active_driver)
            tweets = self.active_driver.find_elements(
                By.CSS_SELECTOR, self.tweet_selector)
            tweet = None
            y_offset = 0

            for i in range(len(tweets)):
                tweet = tweets[i]
                y_offset += tweet.size["height"]
                if "Pinned Tweet" not in tweets[i].text and "Promoted Tweet" not in tweets[i].text:
                    self.tweet_selector += f":nth-of-type({i+1})"
                    break

            avatar = tweet.find_element(By.CSS_SELECTOR, "[data-testid='Tweet-User-Avatar']")
            self.tweet_info["date"] = tweet.find_element(By.CSS_SELECTOR, 'time').text
            self.tweet_info["text"] = tweet.text

            y_offset -= int(tweet.size["height"] * 0.25)
            action.pause(1)
            action.scroll(0, 0, 0, y_offset)
            action.move_to_element(avatar)
            action.move_by_offset(0, 45)
            action.click()
            action.perform()

            self.tweet_info["tweet_url"] = self.active_driver.execute_script("return window.location.href;")
            self.active_driver.quit()

            return self.tweet_info

    def initAction(self, action):
        try:
            self.awaitDriver()
        finally:
            action()
