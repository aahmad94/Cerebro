import os
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
    def __init__(self, webhook_url, url, css_selector, modal_bool, img_tag):
        self.webhook_url = webhook_url
        self.url = url
        self.active_driver = self.driver(url)
        self.css_selector = css_selector
        self.modal_bool = modal_bool
        self.img_tag = img_tag
    
    def snap(self, zoom=90):
        if self.modal_bool:
            self.awaitModal()
        # find element on page by CSS selector
        try:
            self.active_driver.execute_script(f"document.body.style.zoom='{zoom}%';")
            time.sleep(4)
            if self.css_selector:
                css_element = self.active_driver.find_element(By.CSS_SELECTOR, self.css_selector)
                self.active_driver.execute_script(
                    "arguments[0].scrollIntoView(true);", css_element)

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
        options.add_argument("--window-size=900,1080")
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
            print("Unable to locate element with CSS selector '.close-btn'")
            print(e)


    def fwd_image(self):
        webhook = DiscordWebhook(url=self.webhook_url)
        with open("assets/screenshot.png", "rb") as f:
            webhook.add_file(file=f.read(), filename="screenshot.png")
        webhook.content = f"{self.img_tag} <{self.url}>"
        webhook.execute()
        # os.remove("assets/screenshot.png")
