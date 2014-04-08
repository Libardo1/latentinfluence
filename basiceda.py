import pickle
import pandas as pd
#import seaborn as sns
import json
import matplotlib as plt

elite = pickle.load(open('pickles/elites.pkl'))
notes = pickle.load(open('pickles/over100notes.pkl'))
ufc = pickle.load(open('pickles/ufc.pkl'))
popular = pickle.load(open('pickles/over100.pkl'))
reviews = pickle.load(open('pickles/review.pkl'))
biz = pickle.load(open('pickles/business.pkl'))
users = pickle.load(open('pickles/users.pkl'))
popular400 = popular[popular['fcount'] >= 400]

plt = figsize(18,8)
plt = xlim(0.8,5.2)
popular400['average_stars'][1:].plot(kind='kde', label='Over 400 friends')
elite['average_stars'].plot(kind='kde', label='yelp elites')
ufc['average_stars'].plot(kind='kde', label='reviews marked as useful/funny/cool')
notes['average_stars'].plot(kind='kde', label="most amount of 'notes' on yelp")
users['average_stars'].plot(kind='kde', lw=3, label='overall average stars').legend(fontsize=13, loc="upper left")


plt = xlim(0.8,5.2)
plt = figsize(18,8)

elite['average_stars'].plot(kind='kde', label="yelp elite review distribution")
ufc['average_stars'].plot(kind='kde', label="distribution of scores with 'helpful' review ")
sns.distplot(biz['stars'])#.plot(kind='kde')


plt = figsize(6,8)
plt = ylim(0.8,5.2)
sns.boxplot([elite['average_stars'], notes['average_stars'], biz['stars'], \
             users[users['review_count']>3]['average_stars']])\
            .legend(['elites', '100+ notes', 'business averages', 'more than 3 reviews'],\
                    loc='best', fontsize=14)

reviews['stars'].hist(bins = 5)

