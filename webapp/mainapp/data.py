
from django import http
import requests as r 
import pandas as pd



SEARCH_URL = 'http://127.0.0.1:5000/api/movie/search_by_name/'
CONTENT_URL = 'http://127.0.0.1:5000/api/movie/get_content_recommandation/'
KEYWORD_URL = 'http://127.0.0.1:5000/api/movie/get_keyword_recommandation/'
DATASET = 'http://127.0.0.1:5000/api/movie/dataset/'
DATA = 'http://127.0.0.1:5000/api/movie/data/'
EMO = 'http://127.0.0.1:5000/api/movie/emo/'
IMAGE = 'http://127.0.0.1:5000/api/image/'


def get_images(emo='neutral'):
    global IMAGE
    params = {'emotion':emo}
    try:
        data = r.post(IMAGE,json=params,verify=False).json()
        return data
    except:
        return None


def get_data(method='name',data=None,limit=100):
    global SEARCH_URL
    global CONTENT_URL
    global KEYWORD_URL
    url = 0
    if data is not None:
        params = data
        if method == 'name': url = SEARCH_URL
        if method == 'content': url = CONTENT_URL
        if method == 'keyword': url = KEYWORD_URL
        data = r.post(url,json=params,verify=False).json()
        movie_table = pd.read_json(data['table'])
        movie_table = movie_table[movie_table['adult']==False]
        return movie_table
    else: return data


def dataset():
    global DATASET
    data = r.get(DATASET,verify=False).json()
    movie_table = pd.read_json(data['table'])
    return movie_table
    

def movie_detail(id):
    global DATA
    param = {'id':id}
    data = r.get(DATA,json=param,verify=False).json()
    return data


def get_emotion():
    global EMO
    try:
        data = r.get(EMO,verify=False).json()
        return data['emotion']
    except:
        return None
