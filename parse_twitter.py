import re
import urllib3

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class ParseTwitter:
    # required login to parse twitter
    login_user = None
    pwd = None

    # tweet related info
    user = None
    login_url = "https://twitter.com/i/flow/login"
    base_url = "https://twitter.com/"
    tweet_info = {
        "tweet_url": None,
        "tweet": None,
        "date": None,
    }
    tweet_selector = "[data-testid='tweet']"

    active_driver = None
    action = None

    def __init__(self, user="FridaySailer"):
        self.user = user
        self.active_driver = self.driver(self.login_url)
        self.action = ActionChains(self.active_driver)

    # used to let page elemenrs load before using CSS query selectors to find page elements
    def wait(self, seconds=3):
        self.action.pause(seconds)
        self.action.perform()


    # get Twitter login credentials
    def getCreds(self):
        with open('assets/credentials.txt', 'r') as file:
            file_contents = file.read()

        login_index = file_contents.find('login_user=')
        pass_index = file_contents.find('pwd=')

        self.login_user = file_contents[login_index + len('login_user='):].split('\n', 1)[0]
        self.pwd = file_contents[pass_index + len('pwd='):].split('\n', 1)[0]

    # navigate modal and login
    #TODO: save login token & re-use till expiry rather than login again (slow)
    def login(self):
        try:
            self.wait()
            input = self.active_driver.find_element(By.CSS_SELECTOR, 'input')
            input.send_keys(self.login_user)
            input.send_keys(Keys.ENTER)
            
            self.wait()
            input = self.active_driver.find_elements(By.CSS_SELECTOR, "input")[1]
            input.send_keys(self.pwd)
            input.send_keys(Keys.ENTER)
        except NoSuchElementException as e:
            print(f"User login input element not found for user: {self.user}. Handling the error...")
    
    
    def driver(self, url):
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=options)
        
        driver.get(url)
        return driver


    def awaitElement(self, selector):
        try:
            element = WebDriverWait(self.active_driver, 60).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, selector))
            )
        except TimeoutException as e:
            print(f"Timeout error for user: {self.user}. Unable to locate element with CSS selector '{self.tweet_selector}'")
            print(e)
            return self.tweet_info             


    # after logging in, from Twitter feed, use search bar to find user
    def goToUser(self):
        try:
            self.wait(5)
            search_selector = "input[data-testid='SearchBox_Search_Input']"
            input = self.active_driver.find_element(By.CSS_SELECTOR, search_selector)
            self.awaitElement(search_selector)
            input.send_keys(self.user)

            self.wait()
            input.send_keys(Keys.ARROW_DOWN)

            self.wait()
            input.send_keys(Keys.ARROW_DOWN)
            input.send_keys(Keys.ENTER)
        except NoSuchElementException as e:
            print(f"User {self.user} could not be found in search bar")


    def getLastTweetAction(self):
        try: 
            self.awaitElement(self.tweet_selector)
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

            if (tweet):
                try:
                    avatar = tweet.find_element(By.CSS_SELECTOR, "[data-testid='Tweet-User-Avatar']")
                    self.tweet_info["date"] = tweet.find_element(By.CSS_SELECTOR, 'time').text

                    y_offset -= int(tweet.size["height"] * 0.35)

                    self.action.pause(1)
                    self.action.scroll(0, 0, 0, y_offset)
                    self.action.move_to_element(avatar)
                    self.action.move_by_offset(0, 50)
                    self.action.click()
                    self.action.perform()

                    self.wait(2)
                    self.tweet_info["text"] = self.active_driver.find_element(
                        By.CSS_SELECTOR, "[data-testid='tweetText']").text
                    self.tweet_info["tweet_url"] = self.formatUrl(
                        self.active_driver.execute_script("return window.location.href;"))
                    
                    self.active_driver.quit()
                except: 
                    print(f"Could not click into link itself for user {self.user}")
        except NoSuchElementException:
            print(f"Element not found for user: {self.user}")
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

    # handle login flow and query user page, then parse tweets via action
    def initAction(self, action):
        try:
            self.awaitElement("div[aria-labelledby='modal-header']")
        finally:
            self.getCreds()
            self.login()
            self.goToUser()
        
        try: 
            self.awaitElement(self.tweet_selector)
        finally:
            action()
