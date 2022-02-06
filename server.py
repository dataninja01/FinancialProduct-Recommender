import numpy as np
import pandas as pd
import joblib
import sys
from flask import Flask, request, render_template, session, jsonify
import urllib.request
from pusher import Pusher
from datetime import datetime
import httpagentparser
import json
import os
import hashlib
from dbsetup import create_connection, create_session, update_or_create_page, select_all_sessions, select_all_user_visits, select_all_pages


# instantiate Flask app
app = Flask(__name__, template_folder='templates')


app.secret_key = os.urandom(24)

## Add pusher app credential
pusher = Pusher(app_id = "1343382",key = "edb004b2a6170b6f726b",secret = "503e732e570618b92013",cluster = "us2")


## Setup database
database = "./pythonsqlite.db"
conn = create_connection(database)
c = conn.cursor()
userOS = None
userIP = None
userCity = None
userBrowser = None
userCountry = None
userContinent = None
sessionID = None

## Setup data format
def main():
    global conn, c
    
def parseVisitor(data):
    update_or_create_page(c,data)
    pusher.trigger(u'pageview', u'new', {
        u'page': data[0],
        u'session': sessionID,
        u'ip': userIP
    })
    pusher.trigger(u'numbers', u'update', {
        u'page': data[0],
        u'session': sessionID,
        u'ip': userIP
    })

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
    getSession()
    
def getSession():
    global sessionID
    time = datetime.now().replace(microsecond=0)
    if 'user' not in session:
        lines = (str(time)+userIP).encode('utf-8')
        session['user'] = hashlib.md5(lines).hexdigest()
        sessionID = session['user']
        pusher.trigger(u'session', u'new', {
            u'ip': userIP,
            u'continent': userContinent,
            u'country': userCountry,
            u'city': userCity,
            u'os': userOS,
            u'browser': userBrowser,
            u'session': sessionID,
            u'time': str(time),
        })
        data = [userIP, userContinent, userCountry, userCity, userOS, userBrowser, sessionID, time]
        create_session(c,data)
    else:
        sessionID = session['user']


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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard/<session_id>', methods=['GET'])
def sessionPages(session_id):
    result = select_all_user_visits(c,session_id)
    return render_template("dashboard-single.html",data=result)
    
@app.route('/get-all-sessions')
def get_all_sessions():
    data = []
    dbRows = select_all_sessions(c)
    for row in dbRows:
        data.append({
            'ip' : row['ip'],
            'continent' : row['continent'],
            'country' : row['country'], 
            'city' : row['city'], 
            'os' : row['os'], 
            'browser' : row['browser'], 
            'session' : row['session'],
            'time' : row['created_at']
        })
    return jsonify(data)


if __name__ == '__main__':
#     app.run(debug=True)
    if "serve" in sys.argv: app.run(host='0.0.0.0', port=8000, debug=False)
