import requests
from pymongo import MongoClient
import ast
import pandas as pd
import numpy as np
from datetime import datetime

from HTMLParser import HTMLParser

## Clean the description paragraphs

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def remove_backspaces(text):
    split_text = text.split()
    for i in split_text:
        i.replace('\n',' ')
    return ' '.join(split_text)

def clean_description(descr):
    try:
        no_tags = strip_tags(descr)
        return remove_backspaces(no_tags)
    except TypeError:
        return np.nan


## Create Columns for categoty name and category id
def get_category_name(category):
    try:
        return category['name']
    except TypeError:
        return np.nan
    
def get_category_id(category):
    try:
        return category['id']
    except TypeError:
        return np.nan
        
## Get columns for event id and event organizer
def get_next_event_id(event):
    try:
        return event['id']
    except TypeError:
        return np.nan

def get_next_event_name(event):
    try:
        return event['name']
    except TypeError:
        return np.nan

def get_next_event_time(event):
    try:
        return event['time']
    except TypeError:
        return np.nan
    
def get_next_event_offset(event):
    try:
        return event['utc_offset']
    except TypeError:
        return np.nan
    
def get_next_event_rsvp(event):
    try:
        return event['yes_rsvp_count']
    except TypeError:
        return np.nan 

def get_organizer_id(organizer):
    try:
        return organizer['member_id']
    except TypeError:
        return np.nan

def get_organizer_name(organizer):
    try:
        return organizer['name']
    except TypeError:
        return np.nan


#Separate Sponsor Information
def get_sponsors_names(sponsor_list):
    if len(sponsor_list)==0:
        return np.nan
    else:
        sponsor_names=[]
        for i in sponsor_list:
            sponsor_names.append(i['name'])
        return sponsor_names
    
def get_sponsors_desc(sponsor_list):
    if len(sponsor_list)==0:
        return np.nan
    else:
        sponsor_info=[]
        for i in sponsor_list:
            try:
                sponsor_info.append(i['info'])
            except KeyError:
                sponsor_info.append(np.nan)
        return sponsor_info
    
def get_sponsors_details(sponsor_list):
    if len(sponsor_list)==0:
        return np.nan
    else:
        sponsor_info=[]
        for i in sponsor_list:
            try:
                sponsor_info.append(i['details'])
            except KeyError:
                sponsor_info.append(np.nan)
        return sponsor_info

#Get Last event info
def get_last_event_time(x):
    try:
        return x['time']
    except TypeError:
        return np.nan

def get_last_event_rsvp(lastevent):
    try:
        return lastevent['yes_rsvp_count']
    except TypeError:
        return np.nan

def get_days_since_last_event(lastevent):
    try:
        diff = datetime.utcnow()-datetime.fromtimestamp(lastevent/1000)
        #print diff
        return diff.days
    except TypeError:
        return np.nan
    except ValueError:
        return np.nan

def get_months_since_created(created_date):
    date=datetime.fromtimestamp(created_date/1000)
    diff = datetime.utcnow()-date
    if diff.days/30.4<=1:
        return 1.0
    else:
        avg_months = round(diff.days/30.4)
        return avg_months

