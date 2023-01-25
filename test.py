from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


import os
import sys
from os.path import exists
import json
import time
import config
from pathlib import Path

def main():
    global driver
    print('[+] Open browser')
    options = Options()
    options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    options.add_extension('buster.crx')
    driver = webdriver.Chrome(options=options)

    driver.get("https://patrickhlauke.github.io/recaptcha/")
    time.sleep(2)
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"))
    time.sleep(2)
    driver.find_element(By.ID ,"recaptcha-anchor").click()
    print('click')
    driver.switch_to.default_content()
    time.sleep(2)
    frame_cather = driver.find_elements(By.TAG_NAME,'iframe')[2]
    print(frame_cather)
    driver.switch_to.frame(frame_cather)
    time.sleep(2)
    solver = driver.find_element(By.CLASS_NAME, "help-button-holder")
    ac = ActionChains(driver)
    ac.move_to_element(solver).move_by_offset(1, 1).click().perform()
    time.sleep(3)
    check_exists_by_xpath()
    time.sleep(200)
    

def check_exists_by_xpath():
    try:
        driver.find_element(By.CLASS_NAME, "help-button-holder")
    except NoSuchElementException:
        print("Fail")
        return False
    print("done")
    return True  

if __name__ == '__main__':
    main()
