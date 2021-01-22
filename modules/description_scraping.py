# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 18:54:53 2021

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 17:56:56 2021

@author: jeanm
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import csv
import pandas as pd
import traceback, sys


def driver_options_setup():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    return(options)
    
def popup_handler(driver):
    time.sleep(2)
    driver.switch_to.frame(0)
    driver.find_element_by_xpath('/html/body/div/c-wiz/div[2]/div/div/div/div/div[2]/form/div').click()
    time.sleep(0.2)
    
def description_selection(driver):
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/span[1]/span[1]/button")))
    try:
        description = driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/span[1]/span[1]/button").text
        return(description)
    except:
        description = driver.find_element_by_xpath("/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/span[1]/span/span[2]/span[2]/span[1]/button").text     
        return(description)
    
    
    
def descriptions_scraping(placeid):
    url = 'https://www.google.com/maps/place/?q=place_id:{}&hl=en'.format(placeid)
    driver_options = driver_options_setup()
    driver = webdriver.Chrome(options=driver_options)
    driver.get(url)

    try:
        popup_handler(driver)
    except:
        pass

    try:
        description = description_selection(driver)
        df = pd.DataFrame([(placeid,description)])
        df.columns = ['Google_Place_ID__c','description']
        return(df)
    except Exception:
        print(Exception)
    
    

if __name__ == "__main__":

    apikey = 'AIzaSyDrA3v-y90GfvEoZXnR_oRW9YAnXrsX3i8'
    placeid = 'ChIJ-Rm2UcNRqEcRe0v0bm3LC2U'
    
    b = descriptions_scraping(placeid)