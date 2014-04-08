import pickle
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
import pymc as pm
import math
import pdb
 
review = pickle.load(open('../pickles/review.pkl'))
review['date'] = pd.to_datetime(review['date'])
biz = pickle.load(open('../pickles/business.pkl'))
biz = biz.sort(columns="review_count", ascending=False)
 
print biz[:3]
 
########### SET VARIABLES HERE #############
 
n=100 # restaurant samples
 
start = 0 # index of restaurant to start at
finish = n+start
users = 20 #how many do you want around inflection point?
user0 = int(math.ceil(users*1/2))  # users to collect BEFORE inflection
user1 = int(math.floor(users*1/2))  # users to collevt AFTER inflection
mcsamples = 5000
burn = 2000
skip = 1
loop = 0
 
########### END VARIABLES
 
############ INITIALIZE DATA COLLECTING LISTS
tempidxes=[]
businesses=[]
influencers=[] # collects all influencers
inflectionbiz=[('business_id', 'inflection_id', 'total_weeks_sampled', 'year-week', 'when samples taken')] # collects inflection points
count = 0 #count how many samples pass
tsk = 0 # number of taus to skip
 
########### start looping for pymcmc
 
businessids = [ i for i in biz['business_id'][start:finish]]
print 'no. of businesses =', n, '\nuser count =', users, '\ntrials =', mcsamples, '\nburn =', burn
for idx, bizid in enumerate(businessids[start:finish]):
    temp = review[review['business_id'] == bizid]
    temp = temp.sort(columns='date', ascending=True)
    temp['wy'] = temp['date'].apply(lambda x: x.strftime("%Y-%W"))
    asdf = temp.groupby(by='wy').count()
    timetemp = pd.Series(asdf.stars.values, index=asdf.index)
 
########### start pymcmc code here, thanks to @cmrn_dp !
 
    count_data = asdf.totalnotes.values # count data keeps track of the number of reviews per day
    n_count_data = len(asdf) # n_count_date is just a limit of how many days to keep track of
    
    alpha = 1.0 / count_data.mean()  # Recall count_data is the
                                   # variable that holds our txt counts
    lambda_1 = pm.Exponential("lambda_1", alpha)
    lambda_2 = pm.Exponential("lambda_2", alpha)
    
    tau = pm.DiscreteUniform("tau", lower=0, upper=n_count_data)
    @pm.deterministic
    def lambda_(tau=tau, lambda_1=lambda_1, lambda_2=lambda_2):
        out = np.zeros(n_count_data)
        out[:tau] = lambda_1  # lambda before tau is lambda1
        out[tau:] = lambda_2  # lambda after (and including) tau is lambda2
        return out
    observation = pm.Poisson("obs", lambda_, value=count_data, observed=True)
    model = pm.Model([observation, lambda_1, lambda_2, tau])
    
    mcmc = pm.MCMC(model);
    mcmc.sample(mcsamples, burn, skip); # set samples, burn, and how many to skip - ie 1 is "collect every other tau"
    lambda_1_samples = mcmc.trace('lambda_1')[:];
    lambda_2_samples = mcmc.trace('lambda_2')[:];
    tau_samples = mcmc.trace('tau')[:]; # cut off point for tau
    
########### end pymcmc
########### start ending dataset:
    
    tempidx = Counter(tau_samples).most_common(1)[0][0] # what is the most common tau?
    # if tempidx == len(asdf):
 
    #     tempidx=tempidx-1
    #print tempidx, len(asdf)
    if len(Counter(tau_samples)) == 1:
        tempidx = 0
    else:
        i=1
        while tempidx < 3 or tempidx == len(asdf):
            counter = 0
            i += 1
            tempidx = Counter(tau_samples).most_common(i)[i-1][0]
            counter += 1
            if counter > 8:
                tempidx = 0
        if tempidx == 0:
            pass
    if tempidx==0:
        influencers.append(   ['no inflection found for business %s' % bizid ])
    else:
        a = temp[temp['wy'] <= asdf.index[tempidx]]
        a = a.sort(columns='wy', ascending=True)#[-user0:] #dates are descending. you want the last 10
        b = temp[temp['wy'] > asdf.index[tempidx]]
        b = b.sort(columns='wy', ascending=True)#[:user1] #dates are descending. you want the first 5
        businesses.append(a['business_id'][:1].values[0])
        influencers.append(    [i for i in a[-user0:]['user_id'].values]+[j for j in b[:user1]['user_id'].values]     )
        inflectionbiz.append([ a['business_id'][:1].values[0], tempidx, len(asdf), asdf.index[tempidx] ])
        count += 1
        loop += 1
        if loop % 100 == 0:
            print "\n", loop, "done"
c = [item for sublist in influencers for item in sublist]