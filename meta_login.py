from selenium.webdriver.common.by import By

import sys
import time
import config

def login(driver):
    try:
        print('[+] Start login')
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        driver.refresh()
        time.sleep(3)
        driver.find_element(By.XPATH, '//button[text()="Get started"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[text()="I agree"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[text()="Import wallet"]').click()
        
        # 12 fields
        key_index=1
        for index in range(12):
            driver.find_element(By.ID, f"import-srp__srp-word-{index}").send_keys(config.keys[f'key{key_index}'])
            key_index+=1

        # password
        driver.find_element(By.ID, "password").send_keys(config.password)
        driver.find_element(By.ID, "confirm-password").send_keys(config.password)

        driver.find_element(By.ID, "create-new-vault__terms-checkbox").click()

        # submit
        driver.find_element(By.XPATH, '//button[text()="Import"]').click()

        time.sleep(5)
        driver.find_element(By.XPATH, '//button[text()="All done"]').click()
        print('[+] Login successful!')

    except:
        print('[-] Login failed. Try again')
        sys.exit()   