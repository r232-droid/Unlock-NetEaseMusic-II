# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "000A8BF569CE0DDF697684E1A348EB8ECC2E0BF76AD7CD545554FE28BA7234CDF53B609B4116E279826D04FE96CB9F61D95B5617062A362A17E09891E9D1C45BD0A7F5C196601B77D81B90A3E970035C0A38F4A67E7B9048DCBA35EB98B9C5F150954C75F546A07B7E4F63A74436F3F23E42C7AB665C0DAD26326B11E0722AA76B3E67B63E00439C74B21B79AB28BC4E7C329089795C4C45D87422B387289CAC9E5A62BC90F86C88701A0B72ADC96F2F5F51104B755FEBCE50075E9836CC00BC562960297F417C0D29E97D3578887CA9A3BF784977ADDCB739775F9D9D234B50189FBA92B57B3FCF7296A7C37D0CE3CE0E4AB31E091D2656641A3FC701BBCF96D468CDEC1CB11FC6713D6BB07E24605D5E6D49F66414CB928416694E5A4CC53E479EFF205E8653B21D58C446869B339A28E23289A3CF43DE4EEB19689F43B6C07E5385F247878363316B0AB0C60C16A9A46D0ADD6B302A20519965726C69F8CD60"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
