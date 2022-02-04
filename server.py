import numpy as np
import pandas as pd
import joblib
import sys
from flask import Flask, request, render_template

# instantiate Flask app
app = Flask(__name__, template_folder='templates')

# load model w metadata
model = joblib.load("models/pipe_nmf_model_checkpoint.joblib")
nmf_model = model['pipeline']
#Load the lookup table
data = pd.read_csv('data/Credit Card agreements and rates data.csv')
d= data.groupby(['category'],as_index=False).apply(lambda x: x.nsmallest(3, 'Min_APR'))
d.reset_index(inplace=True)
# print(d.loc[d['category'] == 'Credit repair', 'Card_name'].values)
# print(d.loc[d['category'] == 'Credit repair', 'Card_name'].values[0])
#
# print(reco_card[0])
# print(reco_url[0])

# route post requests
@app.route("/")
def my_form():
    return render_template('Fintech_Credit.html')

@app.route("/", methods = ["GET", "POST"])
def predict():
    text = request.form['textbox']
    input=[text]
    preds = nmf_model.transform(input)
    topic = preds.argmax(axis = 1)
    predictions = [model['mytopic_dict'][key] for key in topic]
    output = ''.join(predictions).capitalize()
    reco_card = d.loc[d['category'] == output, 'Card_name'].values
    reco_url = d.loc[d['category'] == output, 'url'].values
    return render_template('Fintech_Credit.html', final = output, final1 = reco_card, final2 = reco_url)

if __name__ == '__main__':
  #app.run(debug=True)
    if "serve" in sys.argv: app.run(host='0.0.0.0', port=8000, debug=False)
