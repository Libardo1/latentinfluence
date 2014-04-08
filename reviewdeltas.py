import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns # optional 

## data has been taken from yelp's dataset challenge
## http://www.yelp.com/dataset_challenge
## and have been sorted/pickled for ease of use


biz = pickle.load(open("pickles/business.pkl"))
review = pickle.load(open("pickles/review.pkl"))
review['date'] = pd.to_datetime(review['date'])
review = review.sort(column="date")

# selecting data subset
n = 500 # number of businesses 
biz = biz.sort(column="review_count", ascending=False) # selecting most reviewed businesses
topbiz=biz['business_id'] # grabbing only the business ids for easier processing
topbizpd = [] # making a master list of reviews x businesses
for business in topbiz[:n]:
    reviews = review[review['business_id'] == business]
    topbizpd.append(reviews.sort(column="date", ascending=True))


def deltascores(businesses, scores):
    simu = []
    for i in range(scores):
        for reviewset in topbizpd[:businesses]:
            delta = [] # this is the delta of the score
            numberlist = []
            runningavg = []
            for review in reviewset['stars']:
                numberlist.append(review)
                runningavg.append(mean(numberlist)) # keep track of average scores
            a = runningavg[-1] # mean score
            b = average(runningavg[:i]) # average of mean score to n-places
        simu.append([i, a-b])
    simuscores = pd.DataFrame(simu)
    simuscores.plot(x=0, y=1, figsize=(18,10))

deltascores(500, 50)