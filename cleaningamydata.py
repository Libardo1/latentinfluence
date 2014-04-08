import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
#import seaborn as sns
import bs4 as bs4
#from matplotlib.backends.backend_pdf import PdfPages

lst = [str(i)+".html" for i in range(1,7)]
#files were saved from yelp as 1.html, 2.html, 3.html....

alltext = []

for filename in lst:
    soup = bs4.BeautifulSoup(open(filename), "html.parser")
    reviewtext = soup.findAll('p', {"class":"review_comment ieSucks"})
    text = [ i.text for i in reviewtext ]
    for i in text:
        alltext.append(i)

alldates=[]
for filename in lst:
    soup = bs4.BeautifulSoup(open(filename), "html.parser")    
    date = soup.findAll('meta', {"itemprop":"datePublished"})
    dates = [(i.text).replace("\n Updated review\n\n", "") for i in date]
    for i in dates:
        alldates.append(pd.to_datetime(i))

allfriends=[]
for filename in lst:
    soup = bs4.BeautifulSoup(open(filename), "html.parser")   
    friends = soup.findAll("li",{"class":"friend-count"})
    friendc = [ i.text for i in friends ]
    for i in friendc:
        allfriends.append(int(i.split(" ")[1]))

def parseufc(ufc):
    for i in range(len(ufc)):
        temp = []
        string = ufc[i].text.replace("\n", "")
    #     string = string.replace("\n", "")
        string = string.replace('Useful', "")
        string = string.replace('Funny', "")
        string = string.replace('Cool',"")
        # "this is X"
        string = string.split(" ")
        string.pop(0)
        for i in string:
            try: 
                temp.append(int(i))
            except:
                temp.append(0)
        u.append(temp[0])
        f.append(temp[1])
        c.append(temp[2])

u=[]
f=[]
c=[]
for filename in lst:
    soup = bs4.BeautifulSoup(open(filename), "html.parser")  
    ufc = soup.findAll('ul', {"class":"big-ufc"})
    if filename=='1.html':
        ufc.pop(22)
    if filename=='2.html':
        ufc.pop(4)
    if filename=='3.html':        
        ufc.pop(15)
        ufc.pop(15)
        ufc.pop(15)
        ufc.pop(15)
    if filename=='4.html':        
        ufc.pop(4)
        ufc.pop(8)
        ufc.pop(9)
        ufc.pop(27)        
        ufc.pop(32)
        ufc.pop(37)
    if filename=='5.html':
        ufc.pop(21)
    if filename=='6.html':
        ufc.pop(2)
        ufc.pop(-1)
    parseufc(ufc)


allnames=[]
for filename in lst:
    soup = bs4.BeautifulSoup(open(filename), "html.parser")
    asdf = (soup.find_all(itemprop="author"))
    namelist=[asdf[i].text[:30].strip() for i in (range(len(asdf)))]
    names = [ (i[0]+" "+i[1][0]+".") for i in [x.split(" ") for x in namelist]]
    for i in names:
        allnames.append(str(i))

allstars=[]
for filename in lst:
    soup = bs4.BeautifulSoup(open(filename), "html.parser")
    stars = soup.findAll('meta', {"itemprop":"ratingValue"})
    stars.pop(0)
    print len(stars), "page: ", filename
    for i in range(len(stars)):
        allstars.append(float(str(stars[i])[15:18]))
    
userids=[]
for filename in lst:
    soup = bs4.BeautifulSoup(open(filename), "html.parser")
    asdf = (soup.find_all(itemprop="author"))
    for i in asdf:
        x = str(i).split('a href="http://www.yelp.com/user_details?userid=')
        userids.append(x[1][:22])



amys['text'] = alltext
amys['stars'] = allstars
amys['name'] = allnames
amys['useful'] = u
amys['funny'] = f
amys['cool'] = c
amys['user_id'] = userids