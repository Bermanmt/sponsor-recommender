import requests
from pymongo import MongoClient
import ast
import pandas as pd
import numpy as np
from clean_groups import clean_description

client = MongoClient()
db = client.meetup
groups_col=db.groups
groups_clean_col = db.groups_clean
test_col = db.test

api_key='466c256e2d1d455e4d3e4861bd32b'

##Get group information for defined location and radius

def save_groups_clean(api_key,location,radius,offset):
    groups = requests.get('https://api.meetup.com/find/groups?key='+api_key+'&sign=true&photo-host=public&location='+location+\
                          '&radius='+str(radius)+'&page=200&offset='+str(offset))
    groups_info = ast.literal_eval(groups.text)
    for group in groups_info:
        group['cleaned']=True
        group['member_profiles']=[]
        group['events']=[]
        try:
            group['next_event_id']=group['next_event']['id']
            group['next_event_name']=group['next_event']['name']
            group['next_event_time']=group['next_event']['time']
            group['next_event_offset']=group['next_event']['utc_offset']
            group['next_event_rsvp']=group['next_event']['yes_rsvp_count']
            group['organizer_id'] = group['organizer']['id']
            group['organizer_name'] = group['organizer']['name']
        except KeyError:
            group['next_event_id']=np.nan
            group['next_event_name']=np.nan
            group['next_event_time']=np.nan
            group['next_event_offset']=np.nan
            group['next_event_rsvp']=np.nan
            group['organizer_id'] = np.nan
            group['organizer_name'] = np.nan
        group['description']=clean_description(group['description'])
        inserted_group = groups_clean_col.insert_one(group)
        print inserted_group.inserted_id



