import pickle
from gensim.utils import SaveLoad
from gensim import corpora, models, matutils
import numpy as np
from bson.objectid import ObjectId
import pymongo
import json

client = pymongo.MongoClient()
db = client.meetup
#groups_col=db.groups
groups_clean_extra_col = db.groups_clean_extra

_id_df = pickle.load(open( './controllers/lsi_id_df.pkl', "rb" ))
count_vectorizer = pickle.load(open( './controllers/count_vectorizer.pkl', "rb" ))
tfidf = models.tfidfmodel.TfidfModel.load('./controllers/tfidf.pkl')
lsi = models.LsiModel.load('./controllers/lsi')
index = SaveLoad.load('./controllers/index.pkl')

def recommend_texts(text,_id_df,count_vectorizer,tfidf,lsi,index):
	# _id_df = pickle.load(open( 'lsi_id_df.pkl', "rb" ))
	# count_vectorizer = pickle.load(open( 'count_vectorizer.pkl', "rb" ))
	# tfidf = models.tfidfmodel.TfidfModel.load('tfidf.pkl')
	# lsi = models.LsiModel.load('lsi')
	# #corpus_lsi = models.LsiModel.load('lsi_corpus')
	# index = SaveLoad.load('index.pkl')
	metis_vecs = count_vectorizer.transform(np.array(text)).transpose()
	metis_corpus= matutils.Sparse2Corpus(metis_vecs)
	metis_tfidf_corpus = tfidf[metis_corpus]
	metis_lsi_corpus = lsi[metis_tfidf_corpus]
	metis_doc_vecs = [doc for doc in metis_lsi_corpus]
	index.num_best=1000
	my_index=index[metis_doc_vecs]
	id_list = [str(_id_df[i[0]]) for i in my_index[0]]
	return id_list

def get_id_list(id_list):
	groups =[]
	for i in id_list:
		group = groups_clean_extra_col.find_one({'_id':ObjectId(i)},{'_id':0})
		groups.append(json.dumps(group))
	return groups

# print recommend_texts(['Metis accelerates the careers of data scientists by providing full-time immersive bootcamps,\
# evening professional development courses, online training and corporate programs.Train you to think and act like a data scientist.\
# Teach you the most essential skills and technologies. Immerse you in real-world, complex problems.Create opportunities to connect with prospective employers.\
# Provide you with excellent student support.Inject continual fun, passion, and excitement into your experience at Metis.'])
