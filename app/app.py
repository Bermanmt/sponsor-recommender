from flask import Flask, render_template
from controllers import main,unpersonal_recommender
import json
import ast

app= Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
	data= unpersonal_recommender.get_top_100_groups()
	data = ast.literal_eval(data)
	return render_template('home.html', data=data)



if __name__ == '__main__':
	app.run(debug=True)