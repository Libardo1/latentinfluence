

window = 7 # assumption being reviews come in 7 day cycles
window2 = 20 # 20 review window seems to converge on overall ending average score

amys = amys.sort(column="date", ascending=True) # assumes you load in amy's data as 'amys'
numberlist = []
runningavg = []
for i in amys['stars']:
    numberlist.append(i*1.0)
    runningavg.append(np.mean(numberlist))
#keeps a list of every score as well as a list of the runnign overall average

plt.figure(figsize=(18,12))
plt.subplot(2,1,1)
# sets up the plots 2 vertical, 1 horizontal, position 1:

pd.Series(amys.stars.values, index=amys.date).plot(lw=2, alpha=.2, label="Star Ratings X Review Date")
#turns the data into a time series indexed by the date.

axvline(pd.to_datetime('05/10/2013'), lw=3, c='red', label="Air Date of Kitchen Nightmares", zorder=5, alpha=0.75)
#draws a vertical line on the air date of Kitchen Nightmares

plt.plot(amys.date, runningavg, lw=2, color='green', zorder=2, label="Moving Average of All Reviews")
#plots moving average

plt.fig = xlim(date2num(datetime.datetime(2010,1,1,1,1)), date2num(datetime.datetime(2014,2,14,1,1))) 
#sets xlim of the first chart

plt.subplot(2,1,2)
rollvar = pd.rolling_var(roll, window2)
#creates rolling variance with a window size 20

rollvar.plot(c='orange', lw=2)
plt.fig = xlim(date2num(datetime.datetime(2010,1,1,1,1)), date2num(datetime.datetime(2014,2,14,1,1))) 
