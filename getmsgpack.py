import umsgpack
import tickersymbols
import config
import json
from datetime import datetime
import time
import pandas as pd
import config
import tickersymbols
import yfinance as yf
import webbrowser
import indicatorformulas

def viewanydf(df,html_string):  #send dataframe of one signal here to see it in a browser
	with open('myhtml2.html', 'w') as f:
		f.write(html_string.format(table=df.to_html(classes='mystyle')))
	webbrowser.open('myhtml2.html')

def convertime(opentimenp):
	opentimestr = str(opentimenp)
	thistime1 = int(opentimestr[:10])
	thisdate1 = time.strftime("%d %B, %Y", time.localtime(thistime1))
	return thisdate1

def getmsgpack(symbol,path):  #pulls the message pack that you want 3
	with open('{}/{}.msgpack'.format(path,symbol), 'rb') as data_file:
		datamsgpk = umsgpack.unpack(data_file,raw=False)
		datajson = json.loads(datamsgpk)
	return datajson

def readmsgpack(symbol,path):  #reads the message pack after pulling getmsgpack 2
	datajson = getmsgpack(symbol,path)
	symbol = datajson["symbol"]
	openlist = datajson["openlist"]
	closelist = datajson["closelist"]
	highlist = datajson["highlist"]
	lowlist = datajson["lowlist"]
	volumelist = datajson["volumelist"]
	datelist = datajson["datelist"]
	day1results = datajson["day1results"]
	day2close = datajson["day2close"]
	day3open = datajson["day3open"]
	return (symbol,openlist,closelist,highlist,lowlist,volumelist,datelist,day1results,day2close,day3open)

#symbollist = tickersymbols.getonlysymbols()
path = config.rawstockdatapath = "C:/Users/VH189DW/Documents/twoyearsdata" #= "C:/Users/VH189DW/Documents/weeklydata" #C:/Users/VH189DW/Documents/twoyearsdata



def msgpacktodf(symbol,path): # for symbol in symbollist with break at the end 1
	d = readmsgpack(symbol,path)
	eachdict = {"date":d[6],"openlist":d[1],"closelist":d[2],"highlist":d[3],"lowlist":d[4],"volumelist":d[5],\
	"day1results":d[7],"day2close":d[8],"day3open":d[9]}
	eachdf = pd.DataFrame(eachdict)
	print(eachdf)
	eachdf = eachdf.sort_values(by="date",ascending=False)
	eachdf['symbol'] = symbol
	eachdf['date'] = eachdf.date.apply(convertime)
	viewanydf(eachdf,config.html_string)
	return eachdf

	


def getdata_tsqllite(symbol): # not being used
	todaydate = datetime.today().strftime('%Y-%m-%d')
	thisstartdate = formatdate(config.startyear,config.startmonth,config.startday)
	thisenddate = formatdate(config.endyear,config.endmonth,config.endday)
	data = pdr.get_data_yahoo(symbol, start=thisstartdate, end= thisenddate)
	data['Symbol'] = symbol
	#columns = ['Date','Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
	data = data.reset_index()
	#str is that the index is the symbol, change index to something else.
	data['Date'] = pd.DatetimeIndex(data.Date).to_native_types()
	#data = data.astype(str)
	#add here the 
# ts = 1552262400
# dates = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d')
# print(dates)
#for symbol in symbollist:

def createresults(symboldf): # for symbol in symbollist with break at the end 1
	symbolobj = yf.Ticker(symbol)
	symboldf = symbolobj.history(period="max", interval = '1wk')
	symboldf = symboldf.sort_values(by="Date",ascending=False)
	symboldf['day1results'] = symboldf.Close/symboldf.Open
	symboldf['day2close'] = symboldf.Close.shift(1)/symboldf.Close
	symboldf['day3open'] = symboldf.Close.shift(2)/symboldf.Close
	print(symboldf)
	#return symboldf

	

def getonlysymbols(): #this creates the symbollist from nasdaq
	symbolraw = pd.read_fwf('nasdaqlisted.txt')
	config.sentinal = 0
	n = 0
	symbollist = []
	while n < len(symbolraw):
		onerow = pd.DataFrame(symbolraw).values[n]
		symbollist.append(onerow[0].split("|", 1)[0])
		n+=1
	return symbollist


# symbollist = getonlysymbols()
# for symbol in symbollist:
# 	#createresults(symbol)
# 	break

# symbollist = getonlysymbols()
# for symbol in symbollist:
# 	msgpacktodf(symbol,path)
# 	break

######For each symbol, then for each row run the getcloudformula
def thislistflip(thelist):
	newlist = thelist#[::-1]
	return newlist


def getcloudall(symbol,path): #pulls before df
	thislist = readmsgpack(symbol,path)
	closelist = thislistflip(thislist[2])[::-1]
	highlist = thislistflip(thislist[3])[::-1]
	lowlist = thislistflip(thislist[4])[::-1]
	datelist = thislistflip(thislist[6])[::-1]
	n=0
	while n < (len(thislist[2])-77):
		indicatorformulas.getcloud(closelist,highlist,lowlist,datelist,symbol)
		closelist.pop(0);highlist.pop(0);lowlist.pop(0);datelist.pop(0)
		n+=1


# from joblib import Parallel, delayed
# import multiprocessing
# import os
#import time

# symbollist = getonlysymbols()
# for symbol in symbollist:
# 	try:
# 		getcloudall(symbol,path)
# 	except FileNotFoundError:
# 		print('file not found error {}'.format(symbol))
# 		continue
# 	except OSError: 
# 		print('OS error {}'.format(symbol))
# 		break
#this needs multithreading. -----
# must decide where to store results
#then must make something to store the results for later ml evaluation - 	

#getcloudall()

# def getcloudallmulti(symbol): #pulls before df
# 	thislist = readmsgpack(symbol,config.rawstockdatapath)
# 	closelist = thislistflip(thislist[2])[::-1]
# 	highlist = thislistflip(thislist[3])[::-1]
# 	lowlist = thislistflip(thislist[4])[::-1]
# 	datelist = thislistflip(thislist[6])[::-1]
# 	n=0
# 	while n < (len(thislist[2])-77):
# 		indicatorformulas.getcloud(closelist,highlist,lowlist,datelist,symbol)
# 		closelist.pop(0);highlist.pop(0);lowlist.pop(0);datelist.pop(0)
# 		n+=1

# def runmulticore(symbollist):
# 	num_cores = multiprocessing.cpu_count()
# 	t0 = time.time()
# 	results = Parallel(n_jobs=num_cores,verbose=5)(delayed(getcloudallmulti)(symbol) for symbol in symbollist)
# 	t1 = time.time()
# 	totaltime = t1-10
# 	print(totaltime)

# symbollist = getonlysymbols()
# runmulticore(symbollist)
# # open resource Monitor in the computer to see how well using CPU
# spawn command
# mQ send to other computers
# build a computer  -

