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
    # check = check_exists_by_xpath()
    # while check: 
    #    print('check again')
    #    time.sleep(1)
    #    check = check_exists_by_xpath()
        
    driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"))
    time.sleep(2)
    driver.find_element(By.ID ,"recaptcha-anchor").click()
    print('[+] Click checkbox')
    driver.switch_to.default_content()
    time.sleep(2)
    frame_cather = driver.find_elements(By.TAG_NAME,'iframe')[2]

    driver.switch_to.frame(frame_cather)
    time.sleep(2)
    print('[+] Press solver')
    click_solver()
    print('[+] Check solver')
    check = check_solver()
    while check:
        reload_solver()
        check = check_solver()
        
    time.sleep(3)
    time.sleep(200)

def remove_cdc():
    options = Options()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
    })

    try:
        driver.get('https://anycoindirect.eu')
        time.sleep(80)
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()

def click_solver():
    try:
        ac = ActionChains(driver)
        ac.move_to_element(driver.find_element(By.CLASS_NAME, "help-button-holder")).move_by_offset(1, 1).click().perform()
        time.sleep(7)
    except NoSuchElementException:
        print("[+] Error: Activate solver")
        return True 

def check_solver():
    try:
        driver.find_element(By.CLASS_NAME, "help-button-holder")
        print("[!] Need reload")
        return True
    except NoSuchElementException:
        print("[+] Solved")
        return False    

def reload_solver():
    try:
        driver.find_element(By.ID, "recaptcha-reload-button").click()
        print("[+] Press reload")
        time.sleep(5)
    except:
        print("[-] Error, while reloading")

def check_exists_by_xpath():
    try:
        driver.find_element(By.XPATH, '//h1[text()="test"]')
        print("[+] Yep")
        return False
    except NoSuchElementException:
        print("Fail")
        return True

if __name__ == '__main__':
    remove_cdc()
