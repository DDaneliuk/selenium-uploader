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
import telebot
from telebot import types
from pathlib import Path
from heading import heading
from meta_login import login
from control import scan, scan_one, updater

def open_web(wait, web_target_main):
    # open opensea
    driver.get(web_target_main)

    # Store the ID of the original window
    original_window = driver.current_window_handle

    time.sleep(2)
    driver.find_element(By.XPATH, '//span[text()="MetaMask"]').click()

    # Wait for the new window or tab
    wait.until(EC.number_of_windows_to_be(2))

    # Loop through until we find a new window handle
    go_original_window(original_window)

    time.sleep(5)
    driver.find_element(By.XPATH, '//button[text()="Next"]').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//button[text()="Connect"]').click()
    time.sleep(5)

    # switch to origin window
    driver.switch_to.window(original_window)
    driver.get('https://opensea.io/asset/create')
    time.sleep(5)
    driver.find_element(By.XPATH, '//span[text()="MetaMask"]').click()
    wait.until(EC.number_of_windows_to_be(2))

    # Loop through until we find a new window handle
    go_original_window(original_window)

    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[text()="Sign"]').click()
    time.sleep(5)

    # switch to origin window
    driver.switch_to.window(original_window)

def switch_frame(target):
    try:
        driver.switch_to.frame(target)
    except:
        print(f'[-] Cant switch to {target} frame')

def upload(img_obj):
    print(f'[+] {fileID} start')
    driver.get('https://opensea.io/asset/create')
    time.sleep(3)
    # get fields and fill it
    driver.find_element(By.ID, "media").send_keys(img_obj['img'])
    driver.find_element(By.ID, "name").send_keys(img_obj['name'])
    driver.find_element(By.ID, "description").send_keys(img_obj['description'])
    # choose collection
    driver.find_element(By.ID, "collection").send_keys("TEST")
    driver.find_element(By.XPATH, '//span[text()="COWS.NOSE.ID."]').click()
    # add properties popup
    driver.find_element(By.CSS_SELECTOR, '[aria-label="Add properties"]').click()
    time.sleep(3)
    driver.find_element(By.XPATH, '//button[text()="Add more"]').click()
    driver.find_element(By.XPATH, '//button[text()="Add more"]').click()
    driver.find_element(By.XPATH, '//button[text()="Add more"]').click()
    driver.find_element(By.XPATH, '//button[text()="Add more"]').click()
    driver.find_element(By.XPATH, '//button[text()="Add more"]').click()
    driver.find_element(By.XPATH, '//button[text()="Add more"]').click()
    driver.find_element(By.XPATH, '//button[text()="Add more"]').click()

    prop_fields_key = driver.find_elements(By.CSS_SELECTOR, '[aria-label="Provide the property name"]')
    prop_fields_value = driver.find_elements(By.CSS_SELECTOR, '[aria-label="Provide the property value"]')

    for idx, f in enumerate(prop_fields_key):
        img_properties = list(img_obj['properties'])[idx]
        prop_key = list(img_properties.values())[0]
        prop_val = list(img_properties.values())[1]
        f.send_keys(prop_key)
        prop_fields_value[idx].send_keys(prop_val)

    # save
    driver.find_element(By.XPATH, '//button[text()="Save"]').click()

    # choose chain
    driver.find_element(By.ID, "chain").click()
    driver.find_element(By.XPATH, '//span[text()="Polygon"]').click()

    # press btn create
    driver.find_element(By.XPATH, '//button[text()="Create"]').click()
    time.sleep(3)

    # recaptcha
    frame_recaptcha = driver.find_element(By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")
    # open frame w/ recaptcha checkbox
    switch_frame(frame_recaptcha)
    time.sleep(1)
    driver.find_element(By.ID ,"recaptcha-anchor").click()
    print('[+] Click checkbox')
    driver.switch_to.default_content()
    time.sleep(1)
    # open frame w/ recaptcha challenge
    frame_recaptcha_challenge = driver.find_element(By.CSS_SELECTOR, "iframe[title='recaptcha challenge expires in two minutes']")
    switch_frame(frame_recaptcha_challenge)

    # start solve challenge.
    check = click_solver()
    # loop until challenge will be solver.
    # first is check if challenge is.
    while check:
        check = check_solver()
        reload_solver()
        check_recaptcha()
        check_web_errors()
        click_solver()

def check_solver():
    try:
        url = driver.current_url
        if url != "https://opensea.io/asset/create":
            title = f'Cows.Nose.id #{fileID}'
            print(f'[+] {fileID} uploaded')
            updater(fileID, title, url)
            return False
        else:   
            # if recaptcha challenge still unsolver reload recaptcha
            # And try solve again
            driver.find_element(By.CLASS_NAME, "help-button-holder")
            print("[!] Need reload")
            return True
    except NoSuchElementException:
        print("[+] Solved")
        return False 

def reload_solver():
    try:
        print("[+] Press reload")
        driver.find_element(By.ID, "recaptcha-reload-button").click()
        time.sleep(3)
    except:
        print("[-] Error, while try to reload")

def click_solver():
    try:
        print("[+] Click solver")
        ac = ActionChains(driver)
        ac.move_to_element(driver.find_element(By.CLASS_NAME, "help-button-holder")).move_by_offset(1, 1).click().perform()
        time.sleep(7)
        return True
    except:
        print("[-] Error: While try click solver")
        return False

def check_recaptcha():
    try:
        # check if recapher has error "Try again"
        driver.find_element(By.CLASS_NAME, "rc-doscaptcha-header-text")
        print(f'[+] Refresh. Try again. {fileID}')
        updater(fileID, '', '')
        driver.refresh()
        return False
    except:
        return True   

def check_web_errors():
    try:
        driver.find_element(By.CLASS_NAME, "AssetForm-status-error")
        print("[-] Web error")    
        driver.find_element(By.XPATH, '//button[text()="Create"]').click()
        time.sleep(3)

        # recaptcha
        frame_recaptcha = driver.find_element(By.CSS_SELECTOR, "iframe[title='reCAPTCHA']")
        # open frame w/ recaptcha checkbox
        switch_frame(frame_recaptcha)
        time.sleep(1)
        driver.find_element(By.ID ,"recaptcha-anchor").click()
        print('[+] Click checkbox')
        driver.switch_to.default_content()
        time.sleep(1)
        # open frame w/ recaptcha challenge
        frame_recaptcha_challenge = driver.find_element(By.CSS_SELECTOR, "iframe[title='recaptcha challenge expires in two minutes']")
        switch_frame(frame_recaptcha_challenge)
    except:
        print('[+] No Web errors')
        return True

# create final obj to upload
def get_file_obj():
    img = f"{img_dir}/{fileID}.png"
    info = f"{json_dir}/{fileID}.json"
    img_obj = {
        "img": img,
    }
    # get all data from json
    with open(info, "r") as read_file:
        data = json.load(read_file)
        img_obj['name'] = data['name']
        img_obj['description'] = data['description']
        img_obj['properties'] = data['attributes']

    return img_obj    

def go_original_window(original_window):
    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break


def bot_feed(text): 
    # bot setup
    bot = telebot.TeleBot(config.bot_token)
    bot.send_message(config.bot_id, f"{text}")

# script's main function
def main():
    global img_dir, json_dir, driver, error_state, processId, fileID

    processId=os.getppid()
    error_state = 1
    
    # display heading
    heading()

    # content folders
    img_dir = (Path("build/images")).absolute()
    json_dir = (Path("build/json")).absolute()

    # open browser
    print('[+] Open browser')
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    options.add_extension('meta.crx')
    options.add_extension('buster.crx')

    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
    })

    # Setup wait for later
    wait = WebDriverWait(driver, 20)

    # web structure
    web_target_account = config.opensea['account']

    # login into metamask
    login(driver)

    open_web(wait, web_target_account)

    while True:
        if error_state == 50:
            bot_feed(f"ID: {processId}\nMany Errors: {error_state}")
            break
        else:
            try:
                fileID = scan_one()
                if fileID:
                    # set status to img
                    updater(fileID, 'uploading', 'uploading')
                    img_obj = get_file_obj()
                    upload(img_obj)
                else:
                    print('No files to upload. Break')   
                    break
            except Exception as e:
                error_state+=1
                print(f'ID: {processId}, {e}')
            time.sleep(10)


    print(f"ID: {processId}\nSession done")
    bot_feed(f"ID: {processId}\nSession done")
    time.sleep(20)


if __name__ == '__main__':
    main()
