from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, send_file
from flask import json
from flask_cors import CORS
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline

from sklearn.externals import joblib
import numpy as np
import random
import pandas as pd
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)
CORS(app)

def normalize_text(text):
    norm_text = text.lower()
    # Replace breaks with spaces
    norm_text = norm_text.replace('<br />', ' ')
    # Pad punctuation with spaces on both sides
    norm_text = norm_text.strip()
    # try find digits and DATES (new)
    norm_text = re.sub(r"\d\d\.\d\d\.\d\d\d\d", "ДАТА", norm_text)
    
    norm_text = re.sub(r"приложени[еюи]\s\d+", " ПРИЛОЖЕНИЕ", norm_text)
    
    norm_text = re.sub(r"\s[nN№]\s?\d+", " НОМЕР", norm_text)
    norm_text = re.sub(r"\s\d+(\s)?", " ЦИФРЫ ", norm_text)
    
    norm_text = re.sub(r"\w\.\w\.(\s)?\w+(\s)?", " ФИО ", norm_text)
    
    ## clearing under_ROW
    norm_text = re.sub('[_]+', 'ГОР_ЧЕРТА', norm_text)
    norm_text = re.sub('[|]+', 'ВЕР_ЧЕРТА', norm_text) 
    norm_text = re.sub('[│]+', 'ВЕР_ЧЕРТА', norm_text)
    norm_text = re.sub('│', 'ВЕР_ЧЕРТА', norm_text)
    norm_text = re.sub(r"(\<\*\>)", 'КАВЫЧ_ЗВЕЗД', norm_text)
    # clearing start numeration
    norm_text = re.sub(r"([\"«»])", "", norm_text)
    norm_text = re.sub(r"(^\d+\.\d+(\.)?(\d+\.)?\s?)", "", norm_text)
    norm_text = re.sub(r"(^\d+\)\s)", "", norm_text)
    norm_text = re.sub(r"(^\d+\.\s+)", "", norm_text)
    norm_text = re.sub(r"(^\w\)\s)", "", norm_text)
    norm_text = re.sub(r"(^\-\s?)", "", norm_text)
    
    
    
    norm_text = re.sub(r"([\.\[\]\"\,\,\%\(\)!\?;:])", "", norm_text)
    
    norm_text = re.sub('\/\s', ' ', norm_text)  
    norm_text = re.sub('\s№\s', ' ', norm_text)    
    norm_text = re.sub('\s[nN]\s', ' ', norm_text)
    #norm_text = re.sub('[_]+', '', norm_text)
    
    norm_text = re.sub('[\s+]', ' ', norm_text)
    norm_text = norm_text.strip()
    return norm_text


model = joblib.load('modelPR_271019.pkl')
count_vect = joblib.load('c_vectPR_271019.pkl')


with open('cl_reportPR_271019.txt', 'r') as file:
    cl_report=file.read()

with open('conf_matrix_Model_to_service_271019.txt', 'r') as file:
    conf_matrix =file.read()

@app.route('/confusion_matrix')
def confusion_matrix():
        return conf_matrix

@app.route('/classification_report')
def classification_report():
        return cl_report


@app.route('/')
def hello_world():
    print("go! go! go!")
    return "<h1>test post service by json on ds_post {id:[ids], text: [texts]</h1>" 

@app.route('/badrequest400')
def bad_request():
    return abort(400)


@app.route('/ds_post', methods=['POST'])
def add_message():
    try:
        content = request.get_json()
        data = pd.DataFrame(content)

        data['text'] = data['text'].apply(normalize_text)
        X = count_vect.transform(data['text'])
        
        data['class'] = model.predict(X)
        data['probability'] = np.around(np.max(model.predict_proba(X), axis=1), decimals=3)
        
        response = app.response_class(response='{"id":'+data.id.to_json(orient='records')+ ',"class":' + str(list(data['class'].values))+ \
            ',"probability":'+ str(list(data['probability'].values))+'}', 
        status=200, 
        mimetype='application/json')
        
    
    except:
        return redirect(url_for('bad_request'))
    return response




app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))
