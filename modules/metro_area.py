# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 15:21:46 2021

@author: jeanm
"""

import modules.Google as g
import pandas as pd

def fetch_type_resource_from_excel(region):#fetch fom s3
    spreadsheetId = "1j8vicszZpTWk5UOKUp0lIaqAziPIi-aIqKif5uYZmHs"
    df_chain= g.fetch_excel(spreadsheetId, "{}PostalCodes".format(region), "A1:T")
    
    return df_chain

a = fetch_type_resource_from_excel('R1')

def get_metro_area(country,postalcode):
    
    if country in ['Germany','Austria','Swiss']:
        region = 'R1'
    elif country in ['France','Belgium']:
        region = 'R2'
    elif country in ['United States']:
        region = 'R3'
    elif country in ['Spain']:
        region = 'R4'
    elif country in ['Czech Republic']:
        region = 'Prague'
    else:  
        region = 'other'
        
    ressource = fetch_type_resource_from_excel(region)
    Metro_Area__c = 'other'
    for row in ressource.iterrows():
        if postalcode == row[1]["PostalCode"]:
            Metro_Area__c = row[1]["Metro_Area__c"]
    
    df = pd.DataFrame([(postalcode,Metro_Area__c)])
    df.columns = ['PostalCode','Metro_Area__c']
    return (df)  

if __name__ == "__main__":
    country = 'France'
    postalcode = '44000'
    out = get_metro_area(country,postalcode)