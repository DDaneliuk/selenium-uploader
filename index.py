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

BLUE, RED, WHITE, YELLOW, MAGENTA, GREEN, END = '\33[94m', '\033[91m', '\33[97m', '\33[93m', '\033[1;35m', '\033[1;32m', '\033[0m'

def setup():
    # set up uploader
    global start_index, files_range
    start_index = int(input("[?] Введіть номер файлу з якого почати: "))
    files_range = int(input("[?] Кількість картинок, які хочете завантажити за цикл: "))
    # check if file exist
    if exists(f'{img_dir}/{start_index}.png' and f'{json_dir}/{start_index}.json'):
        print('[+] File is in directory')
    else:
        sys.exit('[-] No your file in directory. Check your files')

def login_meta():
    print('[+] Start login')
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)
    driver.refresh()
    time.sleep(2)
    driver.find_element(By.XPATH, '//button[text()="Get started"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[text()="I agree"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[text()="Import wallet"]').click()
    # 12 fields
    driver.find_element(By.ID, "import-srp__srp-word-0").send_keys(config.keys['key1'])
    driver.find_element(By.ID, "import-srp__srp-word-1").send_keys(config.keys['key2'])
    driver.find_element(By.ID, "import-srp__srp-word-2").send_keys(config.keys['key3'])
    driver.find_element(By.ID, "import-srp__srp-word-3").send_keys(config.keys['key4'])
    driver.find_element(By.ID, "import-srp__srp-word-4").send_keys(config.keys['key5'])
    driver.find_element(By.ID, "import-srp__srp-word-5").send_keys(config.keys['key6'])
    driver.find_element(By.ID, "import-srp__srp-word-6").send_keys(config.keys['key7'])
    driver.find_element(By.ID, "import-srp__srp-word-7").send_keys(config.keys['key8'])
    driver.find_element(By.ID, "import-srp__srp-word-8").send_keys(config.keys['key9'])
    driver.find_element(By.ID, "import-srp__srp-word-9").send_keys(config.keys['key10'])
    driver.find_element(By.ID, "import-srp__srp-word-10").send_keys(config.keys['key11'])
    driver.find_element(By.ID, "import-srp__srp-word-11").send_keys(config.keys['key12'])

    # password
    driver.find_element(By.ID, "password").send_keys(config.password)
    driver.find_element(By.ID, "confirm-password").send_keys(config.password)

    driver.find_element(By.ID, "create-new-vault__terms-checkbox").click()

    # submit
    driver.find_element(By.XPATH, '//button[text()="Import"]').click()

    time.sleep(5)
    driver.find_element(By.XPATH, '//button[text()="All done"]').click()
    print('[+] Login successful!')

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
    time.sleep(2)

    # switch to origin window
    driver.switch_to.window(original_window)

# upload
def upload_form(img, info, index):
    # final obj for upload
    img_obj = {
        "img": img,
    }
    # get all data from json
    with open(info, "r") as read_file:
        data = json.load(read_file)
        img_obj['name'] = data['name']
        img_obj['description'] = data['description']
        img_obj['properties'] = data['attributes']
        for a in data['attributes']:
            pass

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
    switch_frame()
    time.sleep(1)
    driver.find_element(By.ID ,"recaptcha-anchor").click()
    print('[+] Click checkbox')
    driver.switch_to.default_content()
    time.sleep(1)
    solver_frame = driver.find_element(By.CSS_SELECTOR, "iframe[title='recaptcha challenge expires in two minutes']")
    driver.switch_to.frame(solver_frame)
    check = click_solver()

    # addition time for cather
    while check:
        check = check_solver()
        reload_solver()
        click_solver()

    driver.get('https://opensea.io/asset/create')

def switch_frame():
    try:
        driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, "iframe[title='reCAPTCHA']"))
    except:
        print('[-] Switch again')
        time.sleep(2)    
        switch_frame()

def click_solver():
    try:
        print("[+] Click solver")
        ac = ActionChains(driver)
        ac.move_to_element(driver.find_element(By.CLASS_NAME, "help-button-holder")).move_by_offset(1, 1).click().perform()
        time.sleep(7)
        return True
    except:
        print("[+] Error: Activate solver")
        return False

def check_solver():
    try:
        driver.find_element(By.CLASS_NAME, "help-button-holder")
        print("[!] Need reload")
        return False
    except NoSuchElementException:
        print("[+] Solved")
        return True 

def reload_solver():
    try:
        print("[+] Press reload")
        driver.find_element(By.ID, "recaptcha-reload-button").click()
        time.sleep(5)
    except:
        print("[-] Error, while reloading")        

def upload():
    global file_counter
    file_counter=start_index

    for index in range(files_range):
        print(f'[+] Start uploading {file_counter}.png')
        img = f"{img_dir}/{file_counter}.png"
        info = f"{json_dir}/{file_counter}.json"
        upload_form(img, info, file_counter)
        file_counter +=1

def go_original_window(original_window):
    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

def heading():
    spaces = " " * 98
    sys.stdout.write(GREEN + spaces + """
    █ █       █ █   █ █ █ █ █ █   █ █ █ █ █ █
    █ █ █     █ █   █ █               █ █
    █ █  █    █ █   █ █               █ █
    █ █   █   █ █   █ █ █ █ █         █ █
    █ █     █ █ █   █ █               █ █
    █ █       █ █   █ █               █ █
    """ + END + BLUE +
    '\n' + '{}Upload your awesome nft collection faster{}'.format(BLUE, END).center(60) + '\n' + "")

def bot_feed(text): 
    # bot setup
    bot = telebot.TeleBot(config.bot_token)
    bot.send_message(config.bot_id, f"{text}")

# script's main function
def main():
    global img_dir, json_dir, driver

    os.system("clear||cls")
    
    # display heading
    heading()

    # content folders
    img_dir = Path("build/images")
    img_dir = img_dir.absolute()
    json_dir = json_dir = Path("build/json")
    json_dir.absolute()

    # display heading
    setup()
    # open browser
    print('[+] Open browser')
    options = Options()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    options.add_extension('meta.crx')
    options.add_extension('buster.crx')

    driver = webdriver.Chrome(options=options)

    # Setup wait for later
    wait = WebDriverWait(driver, 20)

    # web structure
    web_target_account = config.opensea['account']

    # login into metamask
    try:
        login_meta()
    except:
        print('[-] Login failed. Try again')

    open_web(wait, web_target_account)
    try:
       bot_feed("Start upload")
       upload()
    except Exception as e:
        error = f"Upload failed at: {file_counter} \n ERROR: {e}"
        bot_feed(error)
        print(e)
        
    print("Session done")
    bot_feed("Session done")
    time.sleep(20)


if __name__ == '__main__':
    main()
