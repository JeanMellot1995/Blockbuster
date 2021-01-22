# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 12:23:55 2021

@author: jeanm
"""
import requests
import pandas as pd
import modules.description_scraping as description
import modules.social_media as socials
import modules.get_types as types
import modules.chain_detection as chain
import modules.api_formating as formating
import modules.metro_area as metro_area

    
def Google_API_call(apikey,placeid):
   
    searchurl = 'https://maps.googleapis.com/maps/api/place/details/json?place_id={}&key={}'.format(placeid,apikey) #request limited to the placeid for it to be free    
    result = requests.get(searchurl).json()

    #upload to S3
    
    return result['result']

def enrichment_flow(apikey,placeid):
    a = Google_API_call(apikey,placeid)
    a_clean = formating.formating(a)
    
    b = description.descriptions_scraping(placeid)
    d = types.get_type_and_category(b["description"][0]) #if d != 'null'
    f = metro_area.get_metro_area(a_clean["Country"][0],a_clean["PostalCode"][0])
    
    df = pd.merge(a_clean,b,on ='Google_Place_ID__c',how ='left') 
    df = pd.merge(df,d,on ='description',how ='left') 
    df = pd.merge(df,f,on ='PostalCode',how ='left') 
    
    if "website" in a.keys():  
        c = socials.social_media_scraping(a["website"])
        e = chain.check_lead_is_chain(a["website"])
        df = pd.merge(df,c,on ='website',how ='left') 
        df = pd.merge(df,e,on ='website',how ='left')
        
    return df

if __name__ == "__main__":

    apikey = 'AIzaSyDrA3v-y90GfvEoZXnR_oRW9YAnXrsX3i8'
    placeid = 'ChIJ23AduPZ2nkcRFoHlACA53CY'
    
    a = Google_API_call(apikey,placeid)
    a_clean = formating.formating(a)
    out = (enrichment_flow(apikey,placeid))