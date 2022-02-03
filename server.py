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
# print(d.head())

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
    card = d.loc[d['category'] == 'Credit repair', 'Card_name'].values
    url = d.loc[d['category'] == 'Credit repair', 'url'].values
    return render_template('Fintech_Credit.html', final = output, card = card, card_url = url)


if __name__ == '__main__':
  app.run(debug=True)
#   app.run(debug=False)
