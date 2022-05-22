from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='index'),
    #path('<str:name>/',views.index,name='nameurl'),
    path('data/<int:movie>',views.movie_detail, ),
    path('data/<str:movie>/<str:method>',views.movie_list,name='list'),
    path('data/emotion',views.get_emotion_movie,name='emo'),
    path('data/emotionimage',views.get_emotion_image,name='emoimage'),
    path('images',views.image_suggestion,name='image')
]
