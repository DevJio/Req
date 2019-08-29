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

app = Flask(__name__)
CORS(app)

model = joblib.load('modelPR_290819.pkl')
count_vect = joblib.load('c_vect_main_PR_all.pkl')
class_map = {0: 8, 1: 16, 2: 18, 3: 34, 4: 5, 5: 37, 6: 3}

with open('cl_reportPR290819.txt', 'r') as file:
    cl_report=file.read()

with open('conf_matrix_consol_to_service_290819.txt', 'r') as file:
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
    
        X = count_vect.transform(data['text'])
        
        data['class'] = model.predict(X)
        data['class'] = data['class'].map(class_map)
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
