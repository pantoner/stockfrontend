import pandas as pd
import sqlite3
import umsgpack
import json
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime
import webbrowser
import config
import getmsgpack
yf.pdr_override() # <== that's all it takes :-)

#path = config.rawstockdatapath

html_string  = config.html_string 

def formatdate(year,month,day):
	thisdate = str(str(year) +'-'+str(month)+'-'+str(day))
	return thisdate

def loaddata(dbname,tablename,df): # not in use for now unless going back to sqlite
	print(dbname , tablename)
	conn = sqlite3.connect(dbname)
	df.to_sql(tablename, conn, if_exists='append')
	print('data has been entered into {}'.format(DB_NAME))

def createresults(symboldf): # creates results
	symboldf = symboldf.sort_values(by="Date",ascending=False)
	symboldf['day1results'] = symboldf.Close/symboldf.Open
	symboldf['day2close'] = symboldf.Close.shift(1)/symboldf.Close
	symboldf['day3open'] = symboldf.Close.shift(2)/symboldf.Close
	return symboldf



def getdata(symbol): # this gets the daily data
	todaydate = datetime.today().strftime('%Y-%m-%d') #might not need this 
	thisstartdate = formatdate(config.startyear,config.startmonth,config.startday)
	thisenddate = formatdate(config.endyear,config.endmonth,config.endday)
	data = pdr.get_data_yahoo(symbol, start=thisstartdate, end= thisenddate)
	data = createresults(data)
	thisjson = convertpricetodict(symbol,data)
	try:
		tomsgpackpath(config.rawstockdatapath,symbol,thisjson)
	except (OSError,KeyError) as e: # trying end elegant not crash program
		return


def getweeklydata(symbol): #gets weekly data
	symbolobj = yf.Ticker(symbol)
	symboldf = symbolobj.history(period="max", interval = '1wk')
	symboldf = createresults(symboldf)
	print(symboldf)
	thisjson = convertpricetodict(symbol,symboldf)
	try:
		tomsgpackpath(config.rawstockdatapath,symbol,thisjson)
	except (OSError, KeyError) as e: # trying end elegant not crash program
		return


def convertpricetodict(symbol,data): #after pulling the data from yahoo this converts it to json for msgpack
	stockprices = data[::-1] #reverses the data by rows
	openlist = stockprices.Open.values.tolist()
	closelist = stockprices.Close.values.tolist()
	highlist = stockprices.High.values.tolist()
	lowlist = stockprices.Low.values.tolist()
	volumelist = stockprices.Volume.values.tolist()
	day1results = stockprices.day1results.values.tolist()
	day2close = stockprices.day2close.values.tolist()
	day3open = stockprices.day3open.values.tolist()
	stockprices = stockprices.reset_index();datelist = stockprices.Date.values.tolist()
	thisdict = {"symbol":symbol, "openlist":openlist,"closelist":closelist,"highlist":highlist,\
	"lowlist":lowlist ,"volumelist":volumelist,"datelist":datelist,"day1results":day1results,"day2close":day2close,"day3open":day3open};thisjson = json.dumps(thisdict)
	return thisjson
# symbol = yf.Ticker("MSFT")
# symboldf = symbol.history(period="max", interval = '1wk')

def tomsgpackpath(path,symbol,thisjson): #creates the mssage pack and stores it in path folder
	try:
		with open('{}/{}.msgpack'.format(path,symbol), 'wb') as outfile:
			umsgpack.pack(thisjson, outfile)
		print("{} loaded to mspack file".format(symbol))
	except FileNotFoundError:
		return

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

	conn = sqlite3.connect(config.dbname)
	data.to_sql(config.tablename, conn, if_exists='append')
	print('data has been entered into {}'.format(config.dbname))

# 				'''
def viewanydf(df,html_string):  #send dataframe of one signal here to see it in a browser
	with open('myhtml2.html', 'w') as f:
		f.write(html_string.format(table=df.to_html(classes='mystyle')))
	webbrowser.open('myhtml2.html')

def getminmaxdates(df):
	notdf = pd.to_datetime(df.Date.str.decode("utf-8"));df = pd.DataFrame(notdf);
	finaldict = {'Days':len(df),'Max':[df.Date.max()],'Min':df.Date.min()};df = pd.DataFrame(finaldict)
	return df

def viewdatabase(html_string,database):
	conn = sqlite3.connect(database)
	conn.text_factory = bytes
	df = pd.read_sql_query("select Distinct Date from cloud",conn) #this query goes to temp table to see data
	df = getminmaxdates(df)
	viewanydf(df,html_string) 



	#conn = sqlite3.connect("C://Python37//predictatl//stockmarket//sstocks.db") 
	#cur = conn.cursor()
	#cur.execute(" SELECT DISTINCT todaydate FROM cloud  ")
	#clouddata = cur.fetchall()
	#columns = ['todaysdate']

def getallsymbols2():  # this runs getdata or stops it based on button click from front end
	symbollist = getonlysymbols()	
	for symbol in symbollist:
		if config.sentinal == 0:
			getdata(symbol)
			print(symbol)
		else:
			print(config.sentinal)
			break

def getallsymbolsweekly(): #this runs get weekly data in a seperate thread from button click on front end
	symbollist = getonlysymbols()
	for symbol in symbollist:
		if config.sentinal == 0:
			getweeklydata(symbol)
			print(symbol)
		else:
			print(config.sentinal) #stop dailydownload from runmain.py
			break


def stopthread():
	config.sentinal = 1
	#viewdatabase(html_string,"sstocks.db")  #used when sqllite was in use
	symbol = "ACAD"
	getmsgpack.msgpacktodf(symbol,config.rawstockdatapath)

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



