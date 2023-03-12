import numpy as np 
from flask import Flask, request, jsonify, render_template 
import pickle 
#importing the inputScript file used to analyze the URL 
import inputScript


#load model 
app = Flask(__name__)
model = pickle.load(open('Phishing_Website.pkl', 'rb'))


#Redirects to the page to give the user iput URL. 
@app.route('/')
@app.route('/index.html')
def home(): 
	return render_template('index.html') 

@app.route('/contact.html')
def contact(): 
	return render_template('contact.html') 

@app.route('/Final.html')
def predict(): 
	return render_template('Final.html') 

#Fetches the URL given by the URL and passes to inputScript
@app.route('/y_predict', methods=['POST','GET'])
def y_predict(): 

	url = request.form['URL']
	checkprediction = inputScript.main(url)
	prediction = model.predict(checkprediction)
	print(prediction)
	output=prediction[0]
	if(output==-1): 
		pred="Your are safe!! This is a Legitimate Website."
	else:
		pred="You are on the wrong site. Be cautious!"
	return render_template('Final.html', prediction_text='{}'.format(pred), url=url)

if  __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)