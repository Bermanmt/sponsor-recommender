from pymongo import MongoClient
import ast
import pandas as pd
import numpy as np
import clean_groups as cg


client = MongoClient()
db = client.meetup
#groups_col=db.groups
groups_clean_extra_col = db.groups_clean_extra
#test_col = db.test


def create_df():
	groups=groups_clean_extra_col.find({})
	groups_arr=[i for i in groups]
	groups_df = pd.DataFrame(groups_arr)
	groups_df['category_name'] = groups_df.category.map(cg.get_category_name)
	groups_df['category_id']=groups_df.category.map(cg.get_category_id)
	groups_df['sponsor_count']=groups_df.sponsors.apply(lambda x: len(x))
	groups_df['sponsor_names']=groups_df.sponsors.apply(cg.get_sponsors_names)
	groups_df['sponsor_desc']=groups_df.sponsors.apply(cg.get_sponsors_desc)
	groups_df['sponsor_details']=groups_df.sponsors.apply(cg.get_sponsors_details)
	groups_df['next_event_id']=map(cg.get_next_event_id,groups_df.next_event)
	groups_df['next_event_name']=map(cg.get_next_event_name,groups_df.next_event)
	groups_df['next_event_time']=map(cg.get_next_event_time,groups_df.next_event)
	groups_df['next_event_offset']=map(cg.get_next_event_offset,groups_df.next_event)
	groups_df['next_event_rsvp']=map(cg.get_next_event_rsvp,groups_df.next_event)
	groups_df['organizer_id']=map(cg.get_organizer_id,groups_df.organizer)
	groups_df['organizer_name']=map(cg.get_organizer_name,groups_df.organizer)
	groups_df['last_event_time']=groups_df['last_event'].apply(cg.get_last_event_time)
	groups_df['days_since_last_event']= groups_df['last_event_time'].apply(cg.get_days_since_last_event)
	groups_df['last_event_rsvp']= groups_df['last_event'].apply(cg.get_last_event_rsvp)
	groups_df['months_since_created']=groups_df.created.apply(cg.get_months_since_created)
	groups_df['members_per_month']=groups_df['members']/groups_df['months_since_created']
	groups_df['rsvp_per_members']=groups_df['last_event_rsvp']/groups_df['members']*100
	

	groups_df.description = groups_df.description.apply(cg.clean_description)


	min_groups_df = groups_df[['_id', 'city', 'category_name','category_id', 'country', 'created','description', 'id', 'join_mode','lat',\
							 'link', 'lon', 'member_profiles','members', 'name', 'next_event',\
							 'next_event_id','next_event_name', 'next_event_offset', 'next_event_rsvp', 'next_event_time',\
							 'organizer_id', 'organizer_name', 'rating', 'state', 'timezone', 'urlname',\
							 'visibility', 'who','sponsors','last_event','sponsor_count','sponsor_names','sponsor_desc','sponsor_details',\
							 'last_event_time','days_since_last_event','last_event_rsvp','months_since_created','members_per_month','rsvp_per_members']]
	return min_groups_df
       
       
       
     


