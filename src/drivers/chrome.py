import os
from seleniumwire import webdriver


def get_chrome():
    path = os.path.abspath(os.getenv('CHROMIUM_DRIVER'))
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    return webdriver.Chrome(path, chrome_options=chrome_options)
