import os
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager



def get_chrome():
    path = os.path.abspath(os.getenv('CHROMIUM_DRIVER'))
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
