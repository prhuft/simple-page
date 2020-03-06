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
version_idx = None #version_idxs[0]
visit_dict = {key: 0 for key in version_idxs} # counts donate page visits
home_visits = 0
        
#### set up a flask app
app = Flask(__name__)

@app.route('/')
def home():  
    global version_idx
    global home_visits
    if home_visits <= 10:
        version_idx = version_idxs[home_visits % 2]
        if home_visits == 10:
            version_idx = sorted([(idx,visit_dict[idx]) for idx in visit_dict],key=lambda x: 5-int(x[1]))[0][0]
        home_visits += 1
    app.logger.critical(f'home_visits = {home_visits}')
    app.logger.critical(f'visit_dict = {visit_dict}')
    app.logger.critical(f'version_idx = {version_idx}')

    with open("index"+ version_idx +".html") as f:
        html = f.read()
    return html

@app.route('/donate.html')
def donate_page():
    version = request.args.get('from')
    visit_dict[version] += 1
    app.logger.critical(f'home_visits = {home_visits}')
    app.logger.critical(f'visit_dict = {visit_dict}')
    app.logger.critical(f'version_idx = {version_idx}')
    with open('donate.html') as f:
        html = f.read()
    return html

#### generate the index.html files
files = [f for f in os.listdir('.') if 
         (os.path.isfile(f) and f[-4:]=='html')]
for idx in version_idxs:
    with open("index"+ idx +".html", 'w') as f:
        text = f"""<html>
        <h1>Welcome to my webpage (version={idx})</h1>
        <body><p>Directory</p><ul> """
        for file in files:
            if 'index' not in file:
                text += "<li><a href=" + '/' + file + f'?from={idx}' ">" + file[:-5] + "</a></li>"           
        text += "</ul> \n </body> \n </html>"
        f.write(text)
    
if __name__ == '__main__':
    app.run(host="0.0.0.0")


