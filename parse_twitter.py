import os
import pickle
import re
import time
import urllib3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class ParseTwitter:
    # required login to parse twitter
    login_user = None
    pwd = None

    # tweet related info
    user = None
    x_url = "https://x.com/login"
    tweet_info = {
        "tweet_url": None,
        "text": None,
        "date": None,
    }
    tweet_selector = "[data-testid='tweet']"

    active_driver = None
    action = None

    def __init__(self, user):
        self.user = user
        self.active_driver = self.driver(self.x_url)
        self.action = ActionChains(self.active_driver)

    # used to let page elemenrs load before using CSS query selectors to find page elements
    def wait(self, seconds=3):
        self.action.pause(seconds)
        self.action.perform()


    # get Twitter login credentials
    def setLoginCredentials(self):
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
            self.awaitElement('input')
            input = self.active_driver.find_element(By.CSS_SELECTOR, 'input')
            input.send_keys(self.login_user)
            input.send_keys(Keys.ENTER) 
            self.wait()
            
            input = self.active_driver.find_elements(By.CSS_SELECTOR, "input")
            if input and input[1]:
                input[1].send_keys(self.pwd)
                input[1].send_keys(Keys.ENTER)
                self.wait()
                self.getSessionCookies()
            else:
                raise Exception('Password field input element could not be found.')
        except:
            print(f"User login input element not found for user: {self.user}. Handling the error...")
            print(self.active_driver.getCurrentUrl())
    

    def getSessionCookies(self):
        cookies = self.active_driver.get_cookies()
        with open('cookies.pkl', 'wb') as file:
            pickle.dump(cookies, file)
    

    def loadSessionCookies(self):
        try:
            with open('cookies.pkl', 'rb') as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.active_driver.add_cookie(cookie)
            self.active_driver.get(self.x_url)
            self.wait()
        except:
            print("No cookies found. Logging in...")
        finally:
            if "login" in self.active_driver.current_url:
                self.login()


    def driver(self, url):
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        service = Service(ChromeDriverManager().install(), options=options)
        driver = webdriver.Chrome(service=service, options = options)

        try:
            driver.get(url)
            time.sleep(2)
            return driver
        except TimeoutException as e:
            print(f"Timeout error for user: {self.user}. Unable to load page: {url}")
            print(e)
        except:
            print(f"Error for user: {self.user}. Unable to load page: {url}")
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
    # --- no longer needed ---
    def goToUser(self):
        try:
            self.wait()
            search_selector = "input[data-testid='SearchBox_Search_Input']"
            self.awaitElement(search_selector)
            input = self.active_driver.find_element(By.CSS_SELECTOR, search_selector)
            input.send_keys(self.user)

            self.wait(0.50)
            input.send_keys(Keys.ARROW_DOWN)

            self.wait(0.50)
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
                if "Pinned" not in tweet.text and "Promoted" not in tweet.text:
                    self.tweet_selector += f":nth-of-type({i+1})"
                    break

            if (tweet):
                print(tweet.text)                 
                try:
                    avatar = tweet.find_element(By.CSS_SELECTOR, "[data-testid='Tweet-User-Avatar']")
                    self.tweet_info["date"] = tweet.find_element(By.CSS_SELECTOR, 'time').text

                    self.action.pause(1)
                    self.action.move_to_element(tweet)
                    self.action.pause(1)
                    self.action.move_to_element(avatar)
                    self.action.move_by_offset(0, 75)
                    self.action.click()
                    self.action.perform()

                    self.wait(2)
                    self.tweet_info["text"] = self.active_driver.find_element(
                        By.CSS_SELECTOR, "[data-testid='tweetText']").text
                    self.tweet_info["tweet_url"] = self.active_driver.execute_script("return window.location.href;")
                    
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
        pattern = r"(https?://x.com/.+/status/\d+)"

        # Extract the main URL with tweet ID
        match = re.search(pattern, url)
        main_url = match.group(1) if match else None     
        return main_url

    # handle login flow and query user page, then parse tweets via action
    def initAction(self, action):
        try:
            self.setLoginCredentials()
            self.loadSessionCookies()
            self.active_driver.get(f"https://x.com/{self.user}")
            self.wait()
        except:
            print(f"Unable to load user page for user: {self.user}")

        try: 
            self.awaitElement(self.tweet_selector)
        except:
            print(f"Unable to locate tweet element for user: {self.user}")
            print(f"Unable to locate tweet element for user: {self.user}")
        finally:
            action()
