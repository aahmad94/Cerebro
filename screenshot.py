from selenium import webdriver

class Screenshot:
    # initialize webdriver
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        # Configure webdriver to be headless
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1920, 1080)
        self.driver.get(url)
        #wait for page to load
        self.driver.implicitly_wait(5)
        # scroll down 400 pixels
        self.driver.execute_script("window.scrollTo(0, 400);")
        self.driver.save_screenshot('screenshot.png')