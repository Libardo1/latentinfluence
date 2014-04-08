import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import seaborn as sns
from dateutil import parser
import math
import itertools
from collections import Counter

######## SET UP DATA COLLECTION 

inflectionbiz=[('business id',  'date of inflection','average stars at inflection', 'rolling mean of score', 'total average score')]
influencers=[]
allreviews=[]

############### SET VARIABLES
 
start = 0 # INDEX OF BIZ TO START FROM
n=500 # HOW MANY
finish = start+n
meanwindow = 7 # SET TO 7 TO CATCH WEEKLY SEASONALITY
varwindow = 20 # REVIEWS SEEM TO HIT FINAL AVERAGE SCORE AROUND 15-20 REVIEWS
users = 15 # HOW MANY USERS TO COLLECT AT INFLECTION

######################### LOAD DATA

review = pickle.load(open('../pickles/review.pkl'))
biz = pickle.load(open('../pickles/business.pkl'))
review['date'] = pd.to_datetime(review['date'])
biz = biz.sort(columns="review_count", ascending=False)
businessids = [ i for i in biz['business_id'][start:finish]]

for idx, bizid in enumerate(businessids):
    currentstar=[]
    runningavg=[]
    temp = review[review['business_id'] == bizid]
    temp = temp.sort(columns='date')
    for star in temp['stars']:
        currentstar.append(star)
        runningavg.append(np.mean(currentstar))
    allreviews.append([currentstar, runningavg])
    
######## GET ROLLING DATA ###    
    
    roll = pd.rolling_mean(pd.Series(temp['stars'].values, index=temp['date']), meanwindow)
    rollvar = pd.rolling_var(roll, varwindow)
    rollvar.sort(ascending=False)
    asdf = temp[temp['date'] <= rollvar.index[0]]
    influencers.append([i for i in asdf['user_id'].values[:users]])
    inflectionbiz.append(    (asdf['business_id'].iloc[1],\
                              
                              rollvar.index[0],\
                              np.mean([i for i in asdf['stars']]),\
                              pd.rolling_mean(pd.Series(asdf.stars.values, index=asdf.date), 7)[-1],\
                              biz[biz['business_id'] == asdf['business_id'].iloc[1]]['stars'].values[0] 
                              ))
influencers = [item for sublist in influencers for item in sublist]