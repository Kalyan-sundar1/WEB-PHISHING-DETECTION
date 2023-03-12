import numpy as np 
from flask import Flask, request, jsonify, render_template 
import pickle 
#importing the inputScript file used to analyze the URL 
import inputScript
from flask_cors import CORS
import requests
import flask

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "bLx-wd7zyRvcRj2fC_eiUwXHaiknCIw7ZQaB5d4pAKcF"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = flask.Flask(__name__, static_url_path='')
CORS(app)


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
	
	payload_scoring = {"input_data": [{"fields": [['f0','f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12','f13','f14','f15','f16','f17','f18','f19','f20','f21','f22','f23','f24','f25','f26','f27','f28','f29']], "values": [[-1,1,1,1,-1,-1,-1,-1,-1,1,1,-1,1,-1,1,-1,-1,-1,0,1,1,1,1,-1,-1,-1,-1,1,1,-1]]}]}
	
	response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/6a9f6b1c-79ce-46bc-a11f-c2d694e7d71d/predictions?version=2022-11-10', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
	print("Scoring response")
	pred=response_scoring.json()
	output=pred['predictions'][0]['values'][0][0]
	if(output==-1): 
		pred="Your are safe!! This is a Legitimate Website."
	else:
		pred="You are on the wrong site. Be cautious!"
	return render_template('Final.html', prediction_text='{}'.format(pred), url=url)

if  __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)