from curses.ascii import HT
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound

import mainapp.data as data_re
from mainapp.Emotion_Detection import emo
import pandas as pd
import json
# Create your views here.

emotion = None

params = {
  "movie_name":'super',
      "emotion":emotion,
      "limit":100,
}


def image_suggestion(request):
    global emotion
    try:
      if emotion is None:
        img = data_re.get_images()
        
      else: 
        img  = data_re.get_images(emotion)
        
      return render(request,'images.html',{"emotion":img['emotion'],"img":img['images'][:10]})
    except:
      return render(request,'404.html')


def index(request):
  try:
    global emotion
    global params
    
    if request.method == 'POST':
      cat = request.POST.get('search',None)
      movie = request.POST.get("movies",None)
      params['movie_name']=movie
      head_table = data_re.get_data(cat,params).head(20)
      keyword_table = data_re.get_data('keyword',params).head(20)
      content_table = data_re.get_data('content',params).head(20)
      return render(request,"index-2.html",{"data_table":head_table,"keyword_table":keyword_table,'content_table':content_table,'name':params['movie_name'],'emotion':params['emotion']})

    head_table = data_re.get_data('name',params).head(20)
    keyword_table = data_re.get_data('keyword',params).head(20)
    content_table = data_re.get_data('content',params).head(20)
    

    return render(request,"index-2.html",{"data_table":head_table,"keyword_table":keyword_table,'content_table':content_table,'name':params['movie_name'],'emotion':params['emotion']})
  except:
    params['movie_name'] = 'super'
    return render(request,'404.html')
    


def movie_detail(request,movie):
  try:
    movie = data_re.movie_detail(int(movie))['table']
    movie=json.loads(movie)
    cast = [j for i,j in enumerate(movie['cast'].split('as')) if i%2!=0]
    crew = movie['crew'].split('by')
    global emotion
    params = {'movie_name':movie['title'],'limit':5,'emotion':emotion}
    #key_table = data_re.get_data('keyword',params)
    con_table = data_re.get_data('content',params)
    if request.method == 'POST':
      cat = request.POST.get('search',None)
      movie = request.POST.get("movies",None)
      params['movie_name']=movie
      head_table = data_re.get_data(cat,params).head(20)
      keyword_table = data_re.get_data('keyword',params).head(20)
      content_table = data_re.get_data('content',params).head(20)
      return render(request,"index-2.html",{"data_table":head_table,"keyword_table":keyword_table,'content_table':content_table,'name':params['movie_name'],'emotion':params['emotion']})

    return render(request,"moviesingle.html",{"data":movie,'cast':cast,'crew':crew,"con_table":con_table,})
  except: 
    params['movie_name'] = 'super'
    return render(request,'404.html')



def movie_list(request,movie,method='content'):
  try:
    global emotion
    global params
    params['movie_name']=movie
    if request.method == 'POST':
        cat = request.POST.get('search',None)
        movie = request.POST.get("movies",None)
        params['movie_name']=movie
        head_table = data_re.get_data(cat,params).head(20)
        keyword_table = data_re.get_data('keyword',params).head(20)
        content_table = data_re.get_data('content',params).head(20)
        return render(request,"index-2.html",{"data_table":head_table,"keyword_table":keyword_table,'content_table':content_table,'name':params['movie_name'],'emotion':params['emotion']})

    #params ={'movie_name':movie,'limit':100,'emotiolobal emotion
    params ={'movie_name':movie,'limit':100,'emotion':emotion}
    if method=='content': table = data_re.get_data('content',params)
    if method=='keyword': table = data_re.get_data('keyword',params)
    return render(request,'moviegridfw.html',{"table":table,'method_data':method})
  except: 
    params['movie_name'] = 'super'
    return render(request,'404.html')

def get_emotion_image(request):
  try:
      global emotion
      emotionobj = emo.EMO_DATA()
      emotion = emotionobj.get_data()["dominant_emotion"]
      print(emotion)
      if emotion is None:
        img = data_re.get_images()
        
      else: 
        img  = data_re.get_images(emotion)
        
      return render(request,'images.html',{"emotion":img['emotion'],"img":img['images'][:10]})

  except:
    return render(request,'404.html')


def get_emotion_movie(request):
  try:
    global emotion
    global params
    if request.method == 'POST':
      cat = request.POST.get('search',None)
      movie = request.POST.get("movies",None)
      params['movie_name']=movie
      head_table = data_re.get_data(cat,params).head(20)
      keyword_table = data_re.get_data('keyword',params).head(20)
      content_table = data_re.get_data('content',params).head(20)
      return render(request,"index-2.html",{"data_table":head_table,"keyword_table":keyword_table,'content_table':content_table,'name':params['movie_name'],'emotion':params['emotion']})

    emotionobj = emo.EMO_DATA()
    emotion = emotionobj.get_data()["dominant_emotion"]

    
    params['emotion']=emotion
    
 
    head_table = data_re.get_data('name',params).head(20)
    keyword_table = data_re.get_data('keyword',params).head(20)
    content_table = data_re.get_data('content',params).head(20)
    

    return render(request,"index-2.html",{"data_table":head_table,"keyword_table":keyword_table,'content_table':content_table,'name':params['movie_name'],'emotion':params['emotion']})
  except: 
    params['movie_name'] = 'super'
    return render(request,'404.html')