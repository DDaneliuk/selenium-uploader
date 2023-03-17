from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time
import csv

def check_items(file_range, file):
    for index in range(file_range):
        try:
            driver.get(f'https://opensea.io/collection/cows-nose-id?search[query]={file}&search[sortAscending]=false&search[sortBy]=BEST_BID')
            time.sleep(3)
            try_get = get_element(file)
            if try_get:
                pass
            else:
                print('Cannot get element')
            file += 1

        except Exception as e:
            print(e)

def get_clones(titles, check_text):
    clone_array = []
    for title in titles:
        if check_text == title.text:
            clone_array.append(title.text)
    if len(clone_array) > 1:
        print(f'[+] Found clone {clone_array}')
        save_clone(clone_array)
    else:  
        print(f'[+] No clone {clone_array}')
        save_clone(clone_array)

def get_element(file):
    try: 
        driver.execute_script("window.scroll(0, 700);")
        try:
            titles = driver.find_elements(By.CLASS_NAME, "eNYnCu")
            check_text = f'Cows.Nose.id #{file}'
            get_clones(titles, check_text)
        except:
            print('no title')
            title = ""    
        
        if title == check_text:
            ac = ActionChains(driver)
            ac.move_to_element(driver.find_element(By.CLASS_NAME, "eNYnCu")).move_by_offset(1, 1).click().perform()
            time.sleep(2)
            url = driver.current_url
            time.sleep(2)
        else:
            url = ""d
        create_csv(file, title, url)
        return True
    except:
        return False
    
def save_clone(clone_array):
    with open("clone.txt","a") as file:
        file.write(f"{clone_array}\n")
    
def create_csv(id, title, url):
    with open('nft-list.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id, title, url])

def main():
    global driver

    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        '''
    })

    file = 1
    file_range = 1000

    check_items(file_range, file)
    
if __name__ == '__main__':
    main()