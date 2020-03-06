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
version_idx = version_idxs[0]
visit_dict = {key: 0 for key in version_idxs} # counts donate page visits
home_visits = 0

# def donate_count(page_fn):
#     visit_dict = {key: 0 for key in version_idxs} # counts donate page visits
#     home_visits = 0
#     def wrapper(page):
#         if page == 'donate.html':
#             visit_dict[version_idx] += 1
#         return page_fn
#     return wrapper

def home_version(home_fn):
    visit_dict = {key: 0 for key in version_idxs}    
    def wrapper():
        pass
        
#### set up a flask app
app = Flask(__name__)

@app.route('/')
def home(): # switches btwn A,B until 10 visits. DOESN'T UPDATE global home_visits. use a wrapper to do the counting and store the final idx result, so that idx will simply be returned after this. OR. 
# make this webpage inside a class, then home_visits is a property we can set update inside the function. 
    global version_idx
    global home_visits
    if home_visits <= 10:
        if home_visits == 10:
            version_idx = sorted([(idx,visit_dict[idx]) for idx in visit_dict],key=lambda x: 5-int(x[1]))[0][0]
        version_idx = version_idxs[home_visits % 2]
        home_visits += 1
    with open("index"+ version_idx +".html") as f:
        html = f.read()
    return html

# @donate_count
# @app.route('/<html_page>')
# def page(html_page):
#     if html_page == 'browse.html':
#         with open('main.csv') as f:
#             df = pd.read_csv(f)
#         return df[-1000:].to_html() 
#     with open(html_page) as f:
#         html = f.read()
#             # if there are other resources for this page, load those too
#     return html

@app.route('/donate.html')
def donate_page():
    version = request.args.get('from')
    visit_dict[version] += 1
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


