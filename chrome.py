import time
import pyperclip

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

options = Options()
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options)
driver.get("https://twitter.com/fridaysailer")

tweet_selector = "article[data-testid='tweet']"
share_selector = tweet_selector + " " + "div[role='group'] div:nth-child(4)"
link_selector = "div[data-testid='Dropdown'] div"
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, tweet_selector))
    )
finally:
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR, share_selector).click()
    # driver.find_element(By.CSS_SELECTOR, link_selector).click()
    # copied_text = pyperclip.paste()
    # print(copied_text)
    
    driver.save_screenshot('screenshot.png')
    driver.quit()

    

