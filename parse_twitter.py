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

    activeDriver = None

    def __init__(self, user="FridaySailer"):
        self.user = user
        self.activeDriver = self.driver()


    def driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1200")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)
        driver.get(self.base_url + self.user)
        return driver

    def awaitDriver(self):
        element = WebDriverWait(self.activeDriver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"{self.tweet_selector}:nth-of-type(4)"))
        )

    def getLastTweetAction(self):
            action = ActionChains(self.activeDriver)
            tweets = self.activeDriver.find_elements(
                By.CSS_SELECTOR, self.tweet_selector)
            tweet_idx = 0
            
            for i in range(len(tweets)):
                if "Pinned Tweet" not in tweets[i].text and "Promoted Tweet" not in tweets[1].text:
                    tweet_idx = i
                    break

            next_tweet = tweets[tweet_idx + 1]
            self.tweet_info["tweet"] = tweets[i].text

            # move cursor to next_tweet and move up by y_offset for clickable surface
            y_offset = next_tweet.size["height"] * 0.50
            y_offset += tweets[tweet_idx].size["height"] * 0.33
            action.move_to_element_with_offset(tweets[i+1], -260, y_offset * -1)
            action.click()
            action.perform()
            self.tweet_info["tweet_url"] = self.activeDriver.execute_script("return window.location.href")
            self.activeDriver.quit()

            return self.tweet_info

    def initAction(self, action):
        try:
            self.awaitDriver()
        finally:
            action()
