import numpy as np
import pandas as pd
import joblib
import sys
import os
from flask import Flask, flash, request, url_for, redirect, make_response, render_template,session
from flask_sqlalchemy import SQLAlchemy
import pymysql
# pymysql.install_as_MySQLdb()
import urllib.request
# from pusher import Pusher
from datetime import datetime
import httpagentparser
import hashlib
# from dbsetup import create_connection, create_session, update_or_create_page, select_all_sessions, select_all_user_visits, select_all_pages



# instantiate Flask app
app = Flask(__name__, template_folder='templates')

# for pusher app
app.secret_key = os.urandom(24)

## Add pusher app credential
# pusher = Pusher(app_id = "1343382",key = "edb004b2a6170b6f726b",secret = "503e732e570618b92013",cluster = "us2")
# def parseVisitor(data):
# #     update_or_create_page(c,data)
#     pusher.trigger(u'pageview', u'new', {
#         u'page': data[0],
#         u'session': sessionID,
#         u'ip': userIP
#     })
#     pusher.trigger(u'numbers', u'update', {
#         u'page': data[0],
#         u'session': sessionID,
#         u'ip': userIP
#     })



# Google Cloud SQL (change this accordingly)
PASSWORD ="fintech1234"
PUBLIC_IP_ADDRESS = "35.230.124.147"
DBNAME ="visitor"
DBNAME2 = "webtraffic"
PROJECT_ID ="fb-mlops-nov-21"
INSTANCE_NAME ="fintech-reco-db"

# configuration
app.config["SECRET_KEY"] = "yoursecretkey"
app.config["SQLALCHEMY_DATABASE_URI"]= f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
app.config['SQLALCHEMY_BINDS'] = {
        'webtraffic': f"mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME2}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True


db = SQLAlchemy(app)
# User ORM for SQLAlchemy
class leads(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    first_name = db.Column(db.String(50), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True)
    education = db.Column(db.String(50), nullable = True)
    searched_for = db.Column(db.String(500), nullable = False)
    topic_prediction = db.Column(db.String(50), nullable = False)
    recommendation1 = db.Column(db.String(100), nullable = False)
    recommendation2 = db.Column(db.String(100), nullable = False)
    recommendation3 = db.Column(db.String(100), nullable = False)

class webtraffic(db.Model):
    __bind_key__ = 'webtraffic'
    __tablename__ = 'webvisitors'
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    ip = = db.Column(db.String(20))
    continent = db.Column(db.String(30))
    country= db.Column(db.String(30))
    city= db.Column(db.String(100))
    os= db.Column(db.String(30))
    browser= db.Column(db.String(30))
    session= db.Column(db.String(100))
    time= db.Column(db.String(100))

def __init__(self, first_name, last_name, address, email, education, searched_for, topic_prediction, recommendation1, recommendation2, recommendation3):
    self.first_name = first_name
    self.last_name = last_name
    self.address = address
    self.email = email
    self.education = education
    self.searched_for = searched_for
    self.topic_prediction = topic_prediction
    self.recommendation1 = recommendation1
    self.recommendation2 = recommendation2
    self.recommendation3 = recommendation3

# load model w metadata
model = joblib.load("models/pipe_clf_svc_checkpoint.joblib")
clf_model = model['pipeline']
#Load the lookup table
data = pd.read_csv('data/Credit Card agreements and rates data.csv')
d= data.groupby(['category'],as_index=False).apply(lambda x: x.nsmallest(3, 'Min_APR'))
d.reset_index(inplace=True)

@app.before_request
def getAnalyticsData():
    global userOS, userBrowser, userIP, userContinent, userCity, userCountry,sessionID 
    userInfo = httpagentparser.detect(request.headers.get('User-Agent'))
    userOS = userInfo['platform']['name']
    userBrowser = userInfo['browser']['name']
    userIP = "72.229.28.185" if request.remote_addr == '0.0.0.0' else request.remote_addr
    api = "https://www.iplocate.io/api/lookup/" + userIP
    try:
        resp = urllib.request.urlopen(api)
        result = resp.read()
        result = json.loads(result.decode("utf-8"))                                                                                                     
        userCountry = result["country"]
        userContinent = result["continent"]
        userCity = result["city"]

    except:
        print("Could not find: ", userIP)
        continent, userCountry, userCity, userOS, userBrowser, sessionID = null, null,null,null,null,null
        time=datetime.now().replace(microsecond=0)
    webtraffic =  webtraffic(ip = userIP, continent = userContinent, country=userCountry, city=userCity, os=userOS, browser=userBrowser, session=sessionID, time=datetime.now().replace(microsecond=0))
    db.session.add(webtraffic)
    db.session.commit()

# route post requests
@app.route("/")
def my_form():
    return render_template('Fintech_Credit.html', leads = leads.query.all())

@app.route("/register", methods = ["GET", "POST"])
def predict():
    if request.method == 'POST':
        searched_for = request.form['textbox']
        input=[searched_for]
        predictions = clf_model.predict(input)
        topic_prediction = ''.join(predictions)
        reco_card = d.loc[d['category'] == topic_prediction, 'Card_name'].values
        reco_url = d.loc[d['category'] == topic_prediction, 'url'].values
        recommendation1 = reco_card[0]
        recommendation2 = reco_card[1]
        recommendation3 = reco_card[2]
        print("Rec1:" + recommendation1);
        print("Rec2:" + recommendation2);
        print("Rec3:" + recommendation3);
        lead = leads(first_name = request.form['first_name'], last_name = request.form['last_name'], address = request.form['address'], email = request.form['email'], education = request.form['education'], searched_for = request.form['textbox'], topic_prediction = topic_prediction, recommendation1 = recommendation1, recommendation2 = recommendation2, recommendation3 = recommendation3)
        db.session.add(lead)
        db.session.commit()

    return render_template('Fintech_Credit.html', final = topic_prediction, final1 = reco_card, final2 = reco_url)

if __name__ == '__main__':
    db.create_all()
#   app.run(debug=True)
#   app.run(debug=False)
    if "serve" in sys.argv: app.run(host='0.0.0.0', port=8000, debug=False)
