import time

from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

class Screenshot:
    active_driver = None

    # initialize webdriver
    def __init__(self, screenshot_url, webhook_url):
        self.webhook_url = webhook_url
        self.active_driver = self.driver(screenshot_url)
    
    def snap(self):
        self.awaitModal()
        # find element on page by CSS selector
        try:
            table = self.active_driver.find_element(By.CSS_SELECTOR, '.element--textblock')
            self.active_driver.execute_script("document.body.style.zoom='67%';")
            time.sleep(2)
            self.active_driver.execute_script(
                "arguments[0].scrollIntoView(true);", table)

            # take screenshot of the page
            self.active_driver.save_screenshot('assets/screenshot.png')
            time.sleep(2)
            self.fwd_image()
        except NoSuchElementException as e:
            print(f"Unable to locate element with CSS selector 'table'")
            print(e)
        


    def driver(self, url):
        # Configure webdriver to be headless
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=720,1080")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(2)
        return driver


    def awaitModal(self):
        btn_selector = '.close-btn'
        try:
            # wait for element to be present
            WebDriverWait(self.active_driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, btn_selector)))

            # use active_driver to get element
            self.element_close_btn = self.active_driver.find_element(
                By.CSS_SELECTOR, btn_selector)

            # click on element
            self.element_close_btn.click()
            time.sleep(2)
        except TimeoutException as e:
            print(
                f"Unable to locate element with CSS selector '.close-btn'")
            print(e)


    def fwd_image(self):
        webhook = DiscordWebhook(
            url=self.webhook_url)
        with open("assets/screenshot.png", "rb") as f:
            webhook.add_file(file=f.read(), filename="economic_calendar.png")
        webhook.execute()