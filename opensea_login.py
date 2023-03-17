from selenium.webdriver.common.by import By

import sys
import time
import config

def switch_page(driver, original_window):
    # Loop through until we find a new window handle
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

def login_profile(driver, webpage):
    try:
        print('[+] OpenSea login...')
        driver.get(webpage)

        # save the ID of the original window
        original_window = driver.current_window_handle

        time.sleep(2)
        driver.find_element(By.XPATH, '//span[text()="MetaMask"]').click()
        time.sleep(5)

        # try to switch to new webpage
        switch_page(driver, original_window)

        # connect to metamask
        time.sleep(5)
        driver.find_element(By.XPATH, '//button[text()="Next"]').click()
        time.sleep(2)
        driver.find_element(By.XPATH, '//button[text()="Connect"]').click()
        time.sleep(2)

        # switch to origin window
        driver.switch_to.window(original_window)

    except Exception as e:
        print(f'[-] OpenSea login failed.\n{e}')
        sys.exit()   

def sign_profile(driver):
    try:
        print('[+] OpenSea sign...')
        # save the ID of the original window
        original_window = driver.current_window_handle
        switch_page(driver, original_window)

        # sign profile
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[text()="Sign"]').click()
        time.sleep(5)

        # switch to origin window
        driver.switch_to.window(original_window)

    except Exception as e:
        print(f'[-] OpenSea sign failed.\n{e}')
        sys.exit()  