from flask import Flask, render_template,request,jsonify,Response
from controllers import main,unpersonal_recommender, personalized
import json
import ast
#import pickle
#from gensim import corpora, models, matutils
text=['Metis accelerates the careers of data scientists by providing full-time immersive bootcamps,\
evening professional development courses, online training and corporate programs.Train you to think and act like a data scientist.\
Teach you the most essential skills and technologies. Immerse you in real-world, complex problems.Create opportunities to connect with prospective employers.\
Provide you with excellent student support.Inject continual fun, passion, and excitement into your experience at Metis.']
##import pdb; pdb.set_trace()
app= Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
	data= unpersonal_recommender.get_top_100_groups()
	data = ast.literal_eval(data)
	print data[0]
	#print data
	return render_template('home.html', data=data)


@app.route('/78953578',methods=['GET','POST'])
def login():
	id_list = personalized.recommend_texts(text,personalized._id_df,personalized.count_vectorizer,personalized.tfidf,personalized.lsi,personalized.index)
	#print type(id_list)
	recommended_groups = personalized.get_id_list(id_list)
	#print recommended_groups
	#print type(recommended_groups)
	recommended_groups=ast.literal_eval(recommended_groups) 
	#print type(recommended_groups)
	#print id_list
	#data= unpersonal_recommender.get_top_100_groups()
	#data = ast.literal_eval(data)
	return render_template('metis.html', data=recommended_groups)
	#return 'hello'
@app.route('/about',methods=['GET','POST'])
def about():
	data= unpersonal_recommender.get_top_100_groups()
	data = ast.literal_eval(data)
	return render_template('metis.html', data=data)

@app.route('/event/',methods=['POST'])
def get_event():
	event_id = request.args['id']

	#print event_id
	event = unpersonal_recommender.get_one_event(event_id)
	#return jsonify(event)
	return json.dumps(event)


if __name__ == '__main__':
	app.run(debug=True)