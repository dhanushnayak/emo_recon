import imp
import logging
from urllib import response
from flask.helpers import make_response
from flask import Flask,request
from flask.templating import render_template
import pandas as pd
import os
from flask_autoindex import AutoIndex
from flask import Blueprint

from flask_limiter.util import get_remote_address

from Api_document import document

from flask import current_app

from Emotion_Detection import emo

app = Flask(__name__)
app.register_blueprint(document)

files_index = AutoIndex(app, os.path.curdir , add_url_rules=False)



@app.route('/files')
@app.route('/files/<path:path>')
def autoindex(path='.'):
    return files_index.render_autoindex(path)

@app.route("/",methods=['GET','POST'])
def index():
    return "Movie_API"


@app.route('/emotion',methods=['GET','POST'])
def emotion_detection():
    #return emo.get_data()
    
    return render_template('main.html')


if __name__=='__main__':
    app.run(debug=True)