"""
project: p3
submitter: huft
partner: none

About the data: 
 * Source: https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data
 * Description: Data for the global average temperature, from years 1750 to 2015. Data shown here has been truncated to 1000 rows, and so only shows 1932 to 2015. 
""" 

#### modules
import pandas as pd
import os
from flask import Flask, request, jsonify
import re
import logging

#### global vars
version_idxs = ['A','B']
visit_dict = {key: 0 for key in version_idxs} # counts donate page visits
home_visits = 0

#### build the data table to be displayed
with open('main.csv') as f: 
        data_df = pd.read_csv(f)
        
#### set up a flask app
app = Flask(__name__)

@app.route('/')
def home_page():  
    global version_idx, home_visits
    if home_visits <= 10:
        version_idx = version_idxs[home_visits % 2]
        if home_visits == 10:
            version_idx = sorted([(idx,visit_dict[idx]) for idx in visit_dict],key=lambda x: 10-int(x[1]))[0][0]
        home_visits += 1
    with open("index"+ version_idx +".html") as f:
        html = f.read()
    return html

@app.route('/api.html')
def api_page():
    with open('api.html') as f:
        return f.read()

@app.route('/donate.html')
def donate_page():
    version = request.args.get('from')
    if version in visit_dict:
        visit_dict[version] += 1
    with open('donate.html') as f:
        return f.read()

@app.route('/browse.<ext>')
def browse_page(ext='html'):
    df = data_df
    qwords = ['cols','rows', 'row'] + list(df.keys())
    qdict = {key:request.args.get(key) for key in qwords}
#     # e.g. ?cols=col1&col2&col3?rows=100&1000
    if qdict['cols'] is not None: # constrain columns by keys
        df = df[qdict['cols'].split('&')]
    if qdict['row'] is not None: # select single row
        df = df.iloc[[int(qdict['row'])]]
    elif qdict['rows'] is not None: # constrain rows by integer position
        row1,row2 = [int(x) for x in qdict['rows'].split('-')]
        df = df.iloc[row1:row2]
    #TODO: make filterable by column value
    for key in [key for key in qdict if key in df.keys() and qdict[key] is not None]:
        df = df[df[key] == qdict[key]]
    if ext == 'json':
        rows = [row[1].to_dict() for row in df.iterrows()]
        if not len(rows) - 1:
            rows = rows[0]
        return jsonify(rows)
    return """<h1>Checkout this hot data</h1> 
           <h3>(hehe.. get it? because global warming)</h3>""" + df.to_html()

@app.route('/email', methods=["POST"])
def email():
    email = str(request.data, "utf-8")
    if re.match(r"[a-zA-Z0-9]+\.*[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+",
                email):
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + '\n')
        return jsonify("thanks")
    return jsonify("please carefully re-enter your email, this time without typos.")
    
if __name__ == '__main__':
    app.run(host="0.0.0.0")
