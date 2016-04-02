from dataframe_handling import create_df
import pymongo
import numpy as np
import json
from bson.objectid import ObjectId

client = pymongo.MongoClient()
db = client.meetup
#groups_col=db.groups
groups_clean_extra_col = db.groups_clean_extra

def recommend_unpersonal():
	df= create_df()
	recommender_df = df.copy()
	recommender_df = recommender_df[['city','state','category_name','members','description','name','next_event_rsvp','rating','sponsor_count','days_since_last_event','last_event_rsvp','months_since_created','members_per_month','rsvp_per_members']]
	recommender_df.members=(recommender_df.members-recommender_df.members.min())/recommender_df.members.max()
	recommender_df.rating=recommender_df.rating.apply(lambda x: x/recommender_df.rating.max())
	recommender_df.days_since_last_event=recommender_df.days_since_last_event.fillna(recommender_df.months_since_created*30.4)
	recommender_df.days_since_last_event = recommender_df.days_since_last_event.apply(lambda x: 1/x)
	recommender_df.days_since_last_event = recommender_df.days_since_last_event.apply(lambda x: (x-recommender_df.days_since_last_event.min())/recommender_df.days_since_last_event.max())
	recommender_df.last_event_rsvp=recommender_df.last_event_rsvp.apply(lambda x: (x-recommender_df.last_event_rsvp.min())/recommender_df.last_event_rsvp.max())
	recommender_df.last_event_rsvp=recommender_df.last_event_rsvp.fillna(0)
	recommender_df.members_per_month=recommender_df.members_per_month.apply(lambda x: (x-recommender_df.members_per_month.min())/recommender_df.members_per_month.max())
	recommender_df.rsvp_per_members=recommender_df.rsvp_per_members.apply(lambda x: (x-recommender_df.rsvp_per_members.max())/recommender_df.rsvp_per_members.max())
	recommender_df['aggregate'] = recommender_df.loc[:,['members','rating','last_event_rsvp','days_since_last_event','members_per_month','rsvp_per_members']].sum(axis=1)
	recommender_df['ranking'] = (recommender_df['aggregate']-recommender_df['aggregate'].min())
	recommender_df['ranking'] =recommender_df['ranking']/recommender_df['ranking'].max()
	ranked_df = recommender_df[['name','category_name','sponsor_count','ranking']].sort_values(by=['ranking'], ascending=False)
	return ranked_df[:500].T.to_dict().values()

def get_top_100_groups():
	top_groups= groups_clean_extra_col.find({'category':{'$exists':True},'group_photo':{'$exists':True}},{'_id':1,'name':1,'sponsor_score':1,'category':1,'group_photo':1}).sort([("sponsor_score", pymongo.DESCENDING)]).limit(100)
	top_list = []
	for i in top_groups:
		i['_id']=str(i['_id'])
		top_list.append(i)
	return json.dumps(top_list)

def get_one_event(_id):
	event=groups_clean_extra_col.find_one({'_id':ObjectId(_id)},{'_id':0})
	return event
