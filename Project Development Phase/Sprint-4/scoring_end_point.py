import numpy as np
from flask import Flask,render_template,request
import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "<hG98mgRIr5gqmayEXjjBeFTSE0WVRIX1y-GSVPognOpe>"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/962a52df-ab21-4ac8-b05d-07b75cd4536e/predictions?version=2022-11-17', json=payload_scoring,
 headers={'Authorization': 'Bearer ' + mltoken})
print("Scoring response")
print(response_scoring.json())
app= Flask(__name__)
model=pickle.load(open(r'new1.pkl','rb'))
@app.route('/')
def home() :
  return render_template("webpage.html")
@app.route('/login',methods = ['POST'])
def login() :
  year = request.form["year"]
  do = request.form["do"]
  ph = request.form["ph"]
  co = request.form["co"]
  bod = request.form["bod"]
  tc = request.form["tc"]
  na = request.form["na"]
  total = [[int(year),float(do),float(ph),float(co),float(bod),float(na),float(tc)]]
  
  # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [int(year),float(do), float(ph), float(co), float(bod), float(na), float(tc)], "values": total}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/823bcd15-d246-4027-ae6d-a984d3e1b053/predictions?version=2022-11-03', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())
    predictions=response_scoring.json()
    
    predict = int(predictions['predictions'][0]['values'][0][0])
  y_pred = model.predict(total)
  y_pred = y_pred[[0]]
  if(y_pred >= 95 and y_pred<=100):
    return render_template("webpage.html",showcase = 'Excellent, The Predicted Value is' + str(y_pred))
  elif(y_pred >= 89 and y_pred<=94):
    return render_template("webpage.html",showcase = 'Very Good, The Predicted Value is' + str(y_pred))
  elif(y_pred >= 80 and y_pred<=88):
    return render_template("webpage.html",showcase = 'Good, The Predicted Value is' + str(y_pred))
  elif(y_pred >= 65 and y_pred<=79):
    return render_template("webpage.html",showcase = 'Fair, The Predicted Value is' + str(y_pred))
  elif(y_pred >= 45 and y_pred<=64):
    return render_template("webpage.html",showcase = 'Marginal, The Predicted Value is' + str(y_pred))
  else:
    return render_template("webpage.html",showcase = 'Poor, The Predicted Value is' + str(y_pred))


if __name__ == '__main__':
     app.run(debug = False)