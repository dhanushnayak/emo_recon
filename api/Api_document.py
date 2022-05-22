from ast import keyword
from cgitb import text
from tkinter import image_names
from numpy import require
import pandas as pd
from flask import Flask,request,jsonify,Blueprint
from flask_restplus import Api,fields,reqparse,Resource
import logging

from Movie_Suggestion.suggestion import movie_recommandation
from Emotion_Detection import emo
import Pic_Suggestion.suggestion  as pic

document = Blueprint('api', __name__,url_prefix='/api')

"""
logger = logging.getLogger('api')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
file_handler = logging.FileHandler("log/api.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)"""
log = logging.getLogger('app')
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
file_handler = logging.FileHandler("log/app.log")
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

api = Api(document,version='1.0',title="Api for Movie Suggestion",description="Team Amrutha. ")
movie_data= api.namespace("movie")

image_data = api.namespace('image')

upload_parser = api.parser()
upload_parser.add_argument('emotion',required=False,type=str,help='Person emotion is helps to give recommandation based on emotion and search')
upload_parser.add_argument("movie_name",required=False,type=str,help='Search movie by name')
upload_parser.add_argument("limit",required=False,type=int,help='Number of records to retrive')
upload_parser.add_argument("content",required=False,type=bool,help='Return based on content match')
upload_parser.add_argument("keyword",required=False,type=bool,help='Return based on Keyword match')

id_parser = api.parser()
id_parser.add_argument('id',required = True, type=int,help='Id of movie')

image_parser = api.parser()
image_parser.add_argument('emotion',required=False,type=str,help='Suggest image by emotion (default - None|Neutral)')

dataset = pd.read_csv("./dataset/movie_dataset2.csv")

@movie_data.route("/search_by_name/")
@movie_data.doc(responses={ 200: 'OK', 404: 'Not able to post'})
@movie_data.expect(upload_parser)
class MovieData(Resource):
    def post(self):
        try:
            args = upload_parser.parse_args()
            name = args.get('movie_name',None)
            emotion= args.get('emotion',None)
            limit = args.get('limit',None)
            if limit is None: limit = 100
            mr = movie_recommandation(df=dataset,emotion=emotion)
            data = mr.get_close_by_name(x=name,limit=limit)
            log.info(f'search = {name}, emotion = {emotion}, limit = {limit},near_by = {data.iloc[0].title}, method = search_by_name')
            return {"parameter":{"name":name,"emotion":emotion,"limit":limit},"data":data.title.to_list(),'table':data.to_json()}
        except Exception as e:
            log.error(e.__doc__)
            pass

@movie_data.route("/get_content_recommandation/")
@movie_data.doc(responses={ 200: 'OK', 404: 'Not able to post'})
@movie_data.expect(upload_parser)
class MovieData_v2(Resource):
    def post(self):
        
            args = upload_parser.parse_args()
            name = args.get('movie_name',None)
            emotion= args.get('emotion',None)
            limit = args.get('limit',None)
            content = args.get('content',None)
            keyword = args.get("keyword",None)
            if content is None and keyword is None:
                content =  True
            if limit is None: limit = 100
            mr = movie_recommandation(df=dataset,emotion=emotion)
            data = mr.get_recommandation(x=name,limit=limit,content=True,keyword=False)
            if content==True:method ='content'
            if keyword==True:method='keyword'
            log.info(f'search = {name}, emotion = {emotion}, limit = {limit},near_by = {data[1]}, method = search_by_{method}')
            return {"parameter":{"name":name,"emotion":emotion,"content":content,"keyword":keyword,"limit":limit},"table":data[0].to_json(),"near_search":data[1]}
        


@movie_data.route("/get_keyword_recommandation/")
@movie_data.doc(responses={ 200: 'OK', 404: 'Not able to post'})
@movie_data.expect(upload_parser)
class MovieData_v3(Resource):
    def post(self):
        try:
            args = upload_parser.parse_args()
            name = args.get('movie_name',None)
            emotion= args.get('emotion',None)
            limit = args.get('limit',None)
            content = args.get('content',None)
            keyword = args.get("keyword",None)
            if content is None and keyword is None:
                keyword =  True
            if limit is None: limit = 100
            mr = movie_recommandation(df=dataset,emotion=emotion)
            data = mr.get_recommandation(x=name,limit=limit,keyword=True,content=False)
            if content==True:method ='content'
            if keyword==True:method='keyword'
            log.info(f'search = {name}, emotion = {emotion}, limit = {limit},near_by = {data[1]}, method = search_by_{method}')
            return {"parameter":{"name":name,"emotion":emotion,"content":content,"keyword":keyword,"limit":limit},"table":data[0].to_json(),"near_search":data[1]}
        except Exception as e:
            log.error(e.__doc__)
            pass


@movie_data.route("/dataset/")
@movie_data.doc(responses={ 200: 'OK', 404: 'Not able to post'})
class MovieData_v4(Resource):
    def get(self):
        try:
            data = movie_recommandation(df=dataset,emotion=None)
            df = data.get_data()
            log.info(f'data = {df.shape}')
            return {"table":df.T.to_json()}
        except Exception as e:
            log.error(e.__doc__)
            pass


@movie_data.route("/data/")
@movie_data.doc(responses={ 200: 'OK', 404: 'Not able to post'})
@movie_data.expect(id_parser)
class MovieData_v5(Resource):
    def get(self):
        try:
            data = movie_recommandation(df=dataset,emotion=None)
            args = id_parser.parse_args()
            name = int(args.get('id',None))
            df = data.get_movie_detail(id=name)
            log.info(f'id = {name},data = {df}')
            return {"id":name,"table":df}
        except Exception as e:
            log.error(e.__doc__)
            pass


@movie_data.route("/emo/")
@movie_data.doc(responses={ 200: 'OK', 404: 'Not able to post'})
class MovieData_v6(Resource):
    def get(self):
        try:
            emotion = emo.EMO_DATA()
            emotion_found = emotion.get_data()
            log.info(f'emotion = {emotion_found["dominant_emotion"]}')
            return {"emotion_frame":emotion_found['emotion'],'emotion':emotion_found["dominant_emotion"]}
            #log.info(f' = {name},data = {df}')
        except Exception as e:
            log.error(e.__doc__)
            pass

@image_data.route("/")
@image_data.doc(responses={ 200: 'OK', 404: 'Not able to post'})
@image_data.expect(image_parser)
class ImageData(Resource):
    def post(self):
        try: 
            args = image_parser.parse_args()
            emo = args.get('emotion','neutral')
            return {"emotion" :emo, "images":pic.get_images(emo)}

        except Exception as e:
            log.error(e.__doc__)
            pass