import numpy as np
import joblib
import sys
from flask import Flask, request, render_template

# instantiate Flask app
app = Flask(__name__, template_folder='templates')

# load model w metadata
model = joblib.load("models/pipe_clf_checkpoint.joblib")
model_clf = model['pipeline']

# route post requests
@app.route('/')
def my_form():
    return render_template('form.html')
    
@app.route("/", methods = ["POST"])
def predict():
    text = request.form['text1']
    input=[text]
    preds = model_clf.predict(input)
    predictions = [model['class labels'][key] for key in preds]
    output = ''.join(predictions).capitalize()
    return render_template('form.html', text=text, final = output)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
