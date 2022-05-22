from functools import reduce
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from fuzzywuzzy import fuzz,process,StringMatcher

class movie_recommandation:
    def __init__(self,df,emotion=None):
        df=df.fillna(' ')
        df=df.drop_duplicates(subset='id')
        self.df = df.loc[:,['adult', 'budget', 'genres', 'homepage',
           'id', 'imdb_id', 'original_language', 'original_title', 'overview',
           'popularity', 'poster_path', 'production_companies',
           'production_countries', 'release_date', 'revenue', 'runtime',
           'spoken_languages', 'status', 'tagline', 'title', 'vote_average',
           'vote_count', 'cast', 'crew', 'keyword_based', 'content_based','lang']]
        self.emotion_data = {'fear':'comedy','disguit':"musical","angry":"family",
                   "sad":"drama","suprise":"crime","happy":"thriller"}
        self.emotion = emotion
  
    def string_process(self,x):
        x = str(x).lower().replace(" ",'')
        return x

    def get_data(self):
        return self.df

    def get_close_by_name(self,x,limit=5):
        x = self.string_process(x)
        k=process.extract(x,self.df.title.str.lower().str.replace(' ',''),limit=limit)
        k1=list(map(lambda x: x[0],k))
        data=reduce(pd.DataFrame.append, map(lambda i: self.df[self.df.title.str.lower().str.replace(' ','') == i], k1))
        if self.emotion is not None and self.emotion in self.emotion_data.keys(): data =data.loc[data['genres'].str.lower().str.contains(self.emotion_data[self.emotion])]
        data=data.drop_duplicates(subset="id")
        return data

    def get_movie_detail(self,id):
        df = self.df.loc[self.df['id']==id]
        return df.iloc[0].to_json()

    def get_recommandation(self,x=None,content=True,keyword=False,limit=10):
        #Selecting Dataframe based on emotion for suggestion 
        if self.emotion is not None and self.emotion in self.emotion_data.keys(): emo_df = self.get_data_of_emotion()
        else: emo_df = self.df
        
          #if emotion is none gives recommandation based on past data or given title match default content based
        if self.emotion is None: 
            if x is not None: movie_name = self.string_process(x)
            else: movie_name = 'super'
            return self.recommandation(df=emo_df,x=movie_name,content=content,keyword=keyword,limit=limit)
        name = 0
        if self.emotion is not None:
            if x is not None:
                closet = self.get_close_by_name(x,limit=limit)
                if closet.shape[0]>0: name = closet.iloc[0].title   
                else: name = 0
            else:
                x = 'super'
                closet = self.get_close_by_name(x,limit=limit)
                if closet.shape[0]>0: name = closet.iloc[0].title
                else: name = 0


            if name!=0:
                idx=emo_df[emo_df.title.str.contains(name)].index[0]
                cid = CountVectorizer(min_df=5,ngram_range=(1,5),stop_words="english")
                if content==True:cid_matrix_content_based_1 = cid.fit_transform(emo_df['content_based'])
                if keyword==True:cid_matrix_content_based_1 = cid.fit_transform(emo_df['keyword_based'])
                cos_similarity_content_based_1 = cosine_similarity(cid_matrix_content_based_1,cid_matrix_content_based_1)

                l=[i[0] for i in sorted(list(enumerate(cos_similarity_content_based_1[idx])),key=lambda x:x[1],reverse=True)]
                if emo_df.shape[0]<limit:limit = emo_df.shape[0]
                return emo_df.iloc[l].iloc[:limit],name

            else:
                if emo_df.shape[0]<limit:limit = emo_df.shape[0]
                return emo_df.iloc[:limit],name

    def get_data_of_emotion(self):
        try:
            emotion_sug = str(self.emotion_data[self.emotion]).lower()
            emo_df = self.df[self.df['genres'].str.lower().str.contains(emotion_sug)]
        except:
            emo_df = self.df
        emo_df.index = np.arange(0,emo_df.shape[0])
        return emo_df
          

    def recommandation(self,df,x,content=False,keyword=False,limit=10):
            df = df[df['status'].str.contains("Released")].sort_values(by='release_date',ascending=False).head(2000)
            df.index = np.arange(0,df.shape[0])
            name = self.get_close_by_name(x,limit=1).title.values[0] 
            if name in df.title.tolist(): idx = df[df.title == name].index[0]
            else : idx=df[df.title.str.lower().str.replace(' ','').str.contains(self.string_process(x))].index[0]
            cid = CountVectorizer(min_df=2,ngram_range=(1,2),stop_words="english")
            if content==True:cid_matrix_content_based_1 = cid.fit_transform(df['content_based'])
            if keyword==True:cid_matrix_content_based_1 = cid.fit_transform(df['keyword_based'])
            cos_similarity_content_based_1 = cosine_similarity(cid_matrix_content_based_1,cid_matrix_content_based_1)
            l=[i[0] for i in sorted(list(enumerate(cos_similarity_content_based_1[idx])),key=lambda x:x[1],reverse=True)]
            if df.shape[0]<limit:limit = df.shape[0]
            return df.iloc[l].iloc[:limit],name
        




