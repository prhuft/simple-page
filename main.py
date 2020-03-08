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
import logging

#### global vars
version_idxs = ['A','B']
version_idx = 'A'
visit_dict = {key: 0 for key in version_idxs} # counts donate page visits
home_visits = 0

#### build the data table to be displayed
with open('main.csv') as f: 
        data_df = pd.read_csv(f).reset_index() #TODO: reset index
        
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
    if qdict['cols'] is not None: # constrain columns
        df = df[qdict['cols'].split('&')]
    if qdict['row'] is not None: # constrain rows
        df = df.iloc[int(qdict['row'])]
    elif qdict['rows'] is not None:
        row1,row2 = [int(x) for x in qdict['rows'].split('-')]
        df = df.iloc[row1:row2]
    for key in [key for key in qdict if key in df.keys() and qdict[key] is not None]: # constrain remaining rows by column key value
        df = df[df[key] == qdict[key]]
#     if ext == 'json':
#         pass
    return "<h1>Checkout this hot data (hehe.. get it? because global warming)</h1>" + df.to_html()
    
#### generate the index.html files
files = [f for f in os.listdir('.') if 
         (os.path.isfile(f) and f[-4:]=='html' and 'index' not in f)]
for idx in version_idxs:
    with open("index"+ idx +".html", 'w') as f:
        text = f"""<html>
             <body>   
             <h1>Welcome to my webpage (version={idx})</h1>
             <p>Directory <br /> \n"""
        for file in files:
            if 'donate' in file:
                text += f"<a href = '{file}?from={idx}'>{file[:-5]}</a><br /> \n"
            else: # could use a regex insertion here instead?
                text += f"<a href = '{file}'>{file[:-5]}</a><br /> \n"     
        text += "</p> \t \n</body>\n</html>"
        f.write(text)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0")
