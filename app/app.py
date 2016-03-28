from flask import Flask, render_template
from controllers import main
import json

app= Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
	return render_template('home.html')



if __name__ == '__main__':
	app.run(debug=True)