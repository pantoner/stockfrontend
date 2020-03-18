import umsgpack
import tickersymbols
import config
import json
from datetime import datetime
import time
import pandas as pd
import config
import tickersymbols

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
	return (symbol,openlist,closelist,highlist,lowlist,volumelist,datelist)

#symbollist = tickersymbols.getonlysymbols()
path = config.rawstockdatapath #= #"C:/Users/VH189DW/Documents/weeklydata"

def msgpacktodf(symbol,path): # for symbol in symbollist with break at the end 1
	d = readmsgpack(symbol,path)
	eachdict = {"date":d[6],"openlist":d[1],"closelist":d[2],"highlist":d[3],"lowlist":d[4],"volumelist":d[5]}
	eachdf = pd.DataFrame(eachdict)
	eachdf['symbol'] = symbol
	eachdf['date'] = eachdf.date.apply(convertime)
	tickersymbols.viewanydf(eachdf,config.html_string)
	


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

