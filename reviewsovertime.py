import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
# import seaborn as sns # optional


## data has been taken from yelp's dataset challenge
## http://www.yelp.com/dataset_challenge
## and have been sorted/pickled for ease

review = pickle.load(open('pickles/review.pkl'))
biz = pickle.load(open('pickles/business.pkl'))

review['date'] = pd.to_datetime(review['date'])
## change datatype to datetime
## probably should have done this in the pickle

businessids = [ i for i in biz['business_id']] 
# not necessary, but made it easier to retrieve the business_ids 
# i wanted in different sample sizes and subsets

plt.fig = figsize(24,20)
plt.fig = ylim(.8,5.2) #set ylimit, yelp stars go from 1-5 stars ± 0.2 for visual buffer

for idx, bizid in enumerate(businessids[:500]):
    if idx < 100: # for top 100
        plt.subplot(2,1,1)
        currentstar=[]
        runningavg=[]
        temp = review[review['business_id'] == bizid]
        temp = temp.sort(column='date')
        for star in temp['stars']:
            currentstar.append(star)
            runningavg.append(average(currentstar))
        plot(pd.to_datetime(temp['date']), runningavg, c='red', lw=3, alpha=.25)

    if idx > 400: # for last 100
        plt.subplot(2,1,2)
        currentstar=[]
        runningavg=[]
        temp = review[review['business_id'] == bizid]
        temp = temp.sort(column='date')
        for star in temp['stars']:
            currentstar.append(star)
            runningavg.append(average(currentstar))
        plot(pd.to_datetime(temp['date']), runningavg, c='blue' , lw=3, alpha=.25)