# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 22:03:13 2020

@author: -
"""
import pandas as pd
import glob
import os
import re
import datetime
import json 
import pytz
from tzwhere import tzwhere
from time import gmtime, strftime



def coord_to_timezone(coord):
    tzwhere1 = tzwhere.tzwhere()
    coord = json.loads(coord.replace("'",'"'))['location']
    
    timezone_str = tzwhere1.tzNameAt(float(coord['lat']), float(coord['lng']))
    return(timezone_str)


def Buyer_type(x):
    if x in ['restaurant','cafe','bar','bakery']:
        return(x)
    else:
        return('other')

def get_attribute(dictionary, attributes):
    out = ''
    for attribute in attributes:
        for i in dictionary:
            if attribute in i['types']:
                out = i['long_name']
    return(out)            
    
def get_open_hours(weekdays,day):
    for days in weekdays:
        if day in days:
            open_hours = days.replace(day,'')
            open_hours_clean = open_hours.replace(': ','')
            return(open_hours_clean)
        
def formating(result):
    
    
    if 'address_components' in result.keys():
        PostalCode = get_attribute(result['address_components'],['postal_code'])
        Street = str(get_attribute(result['address_components'],['street_number'])) + ' ' + str(get_attribute(result['address_components'],['route']))
        City_District = get_attribute(result['address_components'],['sublocality_level_1'])
        City = get_attribute(result['address_components'],['locality']) 
        County = get_attribute(result['address_components'],['administrative_area_level_2'])
        State = get_attribute(result['address_components'],['administrative_area_level_1'])
        Country = get_attribute(result['address_components'],['country'])
    else:
        PostalCode = ""
        Street = ""
        City_District = ""
        City = "" 
        County = ""
        State = ""
        Country = ""
    
    if 'types' in result.keys():
        types = result['types']
        Primary_Type__c = Buyer_type(result['types'][0])
    else:
        types = ""
        Primary_Type__c = ""
    
    if 'website' in result.keys():
        website = result['website']
    else:
        website = ""
        
    if 'international_phone_number' in result.keys():
        Phone = str(result['international_phone_number']).replace(' ','').replace('-','')
    else:
        Phone = ""
        
    if 'opening_hours' in result.keys():
        opening_hours_text = result['opening_hours']['weekday_text']

        Monday__c = get_open_hours(opening_hours_text,'Monday') 
        Tuesday__c = get_open_hours(opening_hours_text,'Tuesday')
        Wednesday__c = get_open_hours(opening_hours_text,'Wednesday')
        Thursday__c = get_open_hours(opening_hours_text,'Thursday')
        Friday__c = get_open_hours(opening_hours_text,'Friday')
        Saturday__c = get_open_hours(opening_hours_text,'Saturday')
        Sunday__c = get_open_hours(opening_hours_text,'Sunday')
    else:
        Monday__c = ""
        Tuesday__c = ""
        Wednesday__c = "" 
        Thursday__c = ""
        Friday__c = ""
        Saturday__c = ""
        Sunday__c = ""
        
    if 'name' in result.keys():
        Company = result['name']
    else:
        Company = ""
        
    if 'reference' in result.keys():
        Google_Place_ID__c = result['reference']
    else:
        Google_Place_ID__c = ""
        
    if 'price_level' in result.keys():
        Price__c = result['price_level']
    else:
        Price__c = ""
        
    if 'rating' in result.keys():
        Gmaps_Rating__c = result['rating']
    else:
        Gmaps_Rating__c = ""
        
    if 'user_ratings_total' in result.keys():
        GMaps_Reviews__c = result['user_ratings_total']
    else:
        GMaps_Reviews__c = ""
        
    if 'business_status' in result.keys():
        Operational_Status__c = result['business_status']
    else:
        Operational_Status__c = ""
    
    if 'geometry' in result.keys():
        time_zone = coord_to_timezone(result['geometry']['location'])
        Time_Zone__c = time_zone
    else:
        Time_Zone__c = ""
    
        
    
    Hidden_ID__c = 'INBOUND_{}'.format(strftime("%W_%Y", gmtime()))

    
    
    Status = 'New'
    OwnerId = '00G1r000003KThS'
    RecordTypeID = '0121r000000VeWWAA0'#inbound record type
    Leadsource = 'Mapping/Other'#inbound app vs web
    Scrape__c = '1'#tbd
    Delivery__c = '0'
    FirstName = ''
    LastName = 'N/A'
    
   
    out = [[Hidden_ID__c,City_District,City,County,State,Country,Time_Zone__c,Company,Google_Place_ID__c,Street,PostalCode,Phone,Primary_Type__c,types,website,Price__c,Monday__c,Tuesday__c,Wednesday__c,Thursday__c,Friday__c,Saturday__c,Sunday__c,Gmaps_Rating__c,GMaps_Reviews__c,Operational_Status__c,Status,OwnerId,RecordTypeID,Leadsource,Scrape__c,Delivery__c,FirstName,LastName]]
    df = pd.DataFrame(out)
    df.columns = ['Hidden_ID__c','City_District','City','County','State','Country','Time_Zone__c','Company','Google_Place_ID__c','Street','PostalCode','Phone','Primary_Type__c','types','website','Price Level','Monday__c','Tuesday__c','Wednesday__c','Thursday__c','Friday__c','Saturday__c','Sunday__c','Gmaps_Rating__c','GMaps_Reviews__c','Operational_Status__c','Status','OwnerId','RecordTypeID','Leadsource','Scrape__c','Delivery__c','FirstName','LastName']  

    return(df)

if __name__ == "__main__":
    print('ok')    
