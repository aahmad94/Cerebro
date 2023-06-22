import time
import pyperclip

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

options = Options()
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options)
driver.get("https://twitter.com/fridaysailer")
action = ActionChains(driver)

tweet_selector = "[data-testid='cellInnerDiv']"
second_tweet_selector = "[data-testid='cellInnerDiv']:nth-of-type(2)"
share_selector = tweet_selector + " " + "div[role='group'] div:nth-child(5)"
link_selector = "div[data-testid='Dropdown'] div"

tweet_url = ""

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, share_selector))
    )
finally:
    share_btn = driver.find_element(By.CSS_SELECTOR, share_selector)
    second_tweet_selector = driver.find_element(By.CSS_SELECTOR, second_tweet_selector)
    action.scroll_to_element(second_tweet_selector)
    action.pause(1)
    action.click(share_btn)
    action.pause(1)
    action.click()
    action.perform()
    tweet_url = pyperclip.paste()
    driver.quit()

    

