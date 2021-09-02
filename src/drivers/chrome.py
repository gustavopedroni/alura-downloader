import os

from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType


def get_chrome():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument("--no-sandbox");
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    os.environ['WDM_LOCAL'] = '1'

    if os.environ['DOCKER_ENV']:
        return webdriver.Chrome(chrome_options=chrome_options)

    return webdriver.Chrome(
        ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), 
        chrome_options=chrome_options
    )
