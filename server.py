import numpy as np
import joblib
import sys
from flask import Flask, request, render_template

# instantiate Flask app
app = Flask(__name__, template_folder='templates')

# load model w metadata
model = joblib.load("models/pipe_nmf_model_checkpoint.joblib")
nmf_model = model['pipeline']

# route post requests
@app.route("/")
def my_form():
    return render_template('Fintech_Credit.html')

@app.route("/", methods = ["POST"])
def predict():
    text = request.form['name']
    input=[text]
    preds = nmf_model.transform(input)
    topic = preds.argmax(axis = 1)
    predictions = [model['mytopic_dict'][key] for key in topic]
    output = ''.join(predictions).capitalize()
    return render_template('Fintech_Credit.html', final = output)

if __name__ == '__main__':
  #app.run(debug=True)
  if "serve" in sys.argv: app.run(host='0.0.0.0', port=8080, debug=False)
