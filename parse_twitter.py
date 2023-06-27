import re
import urllib3

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class ParseTwitter:
    user = ""
    base_url = "https://twitter.com/"
    tweet_info = {
        "tweet_url": None,
        "tweet": None,
        "date": None,
    }
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
        try: 
            action = ActionChains(self.active_driver)
            tweets = self.active_driver.find_elements(
                By.CSS_SELECTOR, self.tweet_selector)
            tweet = None
            y_offset = 0

            for i in range(len(tweets)):
                tweet = tweets[i]
                y_offset += tweet.size["height"]
                if "Pinned Tweet" not in tweet.text and "Promoted Tweet" not in tweet.text:
                    self.tweet_selector += f":nth-of-type({i+1})"
                    break

            avatar = tweet.find_element(By.CSS_SELECTOR, "[data-testid='Tweet-User-Avatar']")
            self.tweet_info["date"] = tweet.find_element(By.CSS_SELECTOR, 'time').text
            self.tweet_info["text"] = tweet.text

            y_offset -= int(tweet.size["height"] * 0.35)
            action.pause(2)
            action.scroll(0, 0, 0, y_offset)
            action.move_to_element(avatar)
            action.move_by_offset(0, 50)
            action.click()
            action.perform()

            url = self.active_driver.execute_script("return window.location.href;")
            self.tweet_info["tweet_url"] = self.formatUrl(url)
            self.active_driver.quit()
        except NoSuchElementException:
            print(f"Element not found for user: {self.user}. Handling the error...")
            return self.tweet_info
        except urllib3.exceptions.MaxRetryError as e:
            print("MaxRetryError occurred:", str(e))
            return self.tweet_info
        
        return self.tweet_info

    def formatUrl(self, url):
        # Regex pattern to match the main URL including the tweet ID
        pattern = r"(https?://twitter.com/.+/status/\d+)"

        # Extract the main URL with tweet ID
        match = re.search(pattern, url)
        main_url = match.group(1) if match else None     
        return main_url

    def initAction(self, action):
        try:
            self.awaitDriver()
        finally:
            action()
