from flask import Flask, render_template,request,jsonify
from controllers import main,unpersonal_recommender
import json
import ast
##import pdb; pdb.set_trace()
app= Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
	data= unpersonal_recommender.get_top_100_groups()
	data = ast.literal_eval(data)
	return render_template('home.html', data=data)

@app.route('/event/',methods=['POST'])
def get_event():
	event_id = request.args['id']
	print event_id
	event = unpersonal_recommender.get_one_event(event_id)
	return jsonify(event)



if __name__ == '__main__':
	app.run(debug=True)