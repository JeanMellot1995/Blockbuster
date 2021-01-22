# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 10:52:18 2021

@author: jeanm
"""
import modules.Google as g
import pandas as pd
from fuzzywuzzy import fuzz
import difflib
from simple_salesforce import Salesforce
from rapidfuzz import process, utils
import tldextract

def getdomain(url):
    ext = tldextract.extract(url)
    return ext.domain


def fetch_chain_resource_from_excel(tab):
    spreadsheetId = "1_YtKSNgiXRr15LOXLFenrDGLwzF6p0OkIGjs1QR0oH0"
    df_chain= g.fetch_excel(spreadsheetId,tab, "A:T")
    df_chain['domain'] = df_chain.apply(lambda x: getdomain(x['Website']) ,axis = 1)
    df_chain.columns = map(str.lower, df_chain.columns)
    return df_chain

def check_lead_is_chain(website):
    excluded_domain = ['facebook', 'business', 'instagram', 'yelp', "google", "mobile-webview"]
    ressource = fetch_chain_resource_from_excel("Chain identification")
    domain_lead = getdomain(website)
    is_chain = False
    group_id = ""
    for chain in ressource.iterrows():
        if domain_lead == chain[1]["domain"]:
            is_chain = True
            group_id = chain[1]["Id"]
    if domain_lead in excluded_domain:
        is_chain = False
        group_id = ""
    df = pd.DataFrame([(website,is_chain,group_id)])
    df.columns = ['website','is_chain','group_id']
    return(df)
    









