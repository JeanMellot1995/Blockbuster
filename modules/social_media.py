# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 16:28:53 2020
@author: jeanm
"""
import csv
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import re
import sys, traceback

def is_email_valid(email):
    EMAIL_REGEX = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
    valid = True
    if not EMAIL_REGEX.match(email):
        valid = False
    if email[-3:].lower() in ['jpg','png']:
        valid = False
    if email[-4:].lower() in ['jpeg']:
        valid = False
    return(valid)

def social_media_scraping(website):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    response_check = [True,False]
    url_prefix = ['','https://www.','http://www.']
    
    mail = ''
    twitter = ''
    facebook = ''
    instagram = ''
    scraped = False
    
    try:
        out = []
        for verify in response_check:
            if scraped == False:
                for prefix in url_prefix:
                    try:
                        time.sleep(1)
                        url = prefix + str(website)
                        page = requests.get(url,headers=headers,timeout=5,verify=verify)
                        soup = BeautifulSoup(page.content, 'html.parser')
                        for a in soup.find_all('a', href=True):
                            if 'mailto:' in str(a):
                                mail = a['href'].replace('mailto:','')
                                if is_email_valid(mail) == False:
                                    mail = ''
                            if 'twitter' in str(a):
                                twitter = a['href']
                            if 'facebook' in str(a):
                                facebook = a['href']
                            if 'instagram' in str(a):
                                instagram = a['href']
                        out.append((url,mail,twitter,facebook,instagram))
                        scraped = True
                        break
                    except:
                        traceback.print_exc(file=sys.stdout)
                        pass
    except:
        pass
        

    if scraped == False:
        out.append((website,mail,twitter,facebook,instagram))
        
    df = pd.DataFrame(out)
    df.columns = ['website','email','twitter','facebook','instagram']
    return(df)

if __name__ == "__main__":

    website = 'http://bellavita.berlin/'
    c = social_media_scraping(website)