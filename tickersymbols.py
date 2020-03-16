import pandas as pd
import sqlite3
import umsgpack
import json
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime
import webbrowser
import config
yf.pdr_override() # <== that's all it takes :-)

html_string = '''
				<html>
				  <head><title>HTML Pandas Dataframe with CSS</title></head>
				  <link rel="stylesheet" type="text/css" href="df_style.css"/>
				  <body>
					{table}
				  </body>
				</html>.
				'''
path = config.rawstockdatapath

def formatdate(year,month,day):
	thisdate = str(str(year) +'-'+str(month)+'-'+str(day))
	return thisdate

def loaddata(dbname,tablename,df):
	print(dbname , tablename)
	conn = sqlite3.connect(dbname)
	df.to_sql(tablename, conn, if_exists='append')
	print('data has been entered into {}'.format(DB_NAME))

def getdata(symbol):
	todaydate = datetime.today().strftime('%Y-%m-%d')
	thisstartdate = formatdate(config.startyear,config.startmonth,config.startday)
	thisenddate = formatdate(config.endyear,config.endmonth,config.endday)
	data = pdr.get_data_yahoo(symbol, start=thisstartdate, end= thisenddate)
	stockprices = data[::-1] #reverses the data by rows
	openlist = stockprices.Open.values.tolist()
	closelist = stockprices.Close.values.tolist()
	highlist = stockprices.High.values.tolist()
	lowlist = stockprices.Low.values.tolist()
	volumelist = stockprices.Volume.values.tolist()
	thisdict = {"symbol":symbol,"startdate":thisstartdate,"enddate":thisenddate, "openlist":openlist,\
	"closelist":closelist,"highlist":highlist,"lowlist":lowlist ,"volumelist":volumelist};thisjson = json.dumps(thisdict)
	with open('{}/{}.msgpack'.format(path,symbol), 'wb') as outfile:
		umsgpack.pack(thisjson, outfile)
	print("{} loaded to mspack file".format(symbol))

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
	#conn = sqlite3.connect('stocks','cloud')
	#data.to_sql('stocks', conn, if_exists="replace")
	#print('data has been entered into {}'.format('stocks'))
	#loaddata(config.dbname,config.tablename,data)   
	#stockprices = data[::-1] #reverses the data by rows
	#closelist = stockprices.Close.values.tolist()
	#highlist = stockprices.High.values.tolist()
	#lowlist = stockprices.Low.values.tolist()
 
	#print(closelist,highlist,lowlist)

# html_string = '''
# 				<html>
# 				  <head><title>HTML Pandas Dataframe with CSS</title></head>
# 				  <link rel="stylesheet" type="text/css" href="df_style.css"/>
# 				  <body>
# 					{table}
# 				  </body>
# 				</html>.
# 				'''
def viewanydf(df,html_string):
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
	df = pd.read_sql_query("select Distinct Date from cloud",conn)
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

def stopthread():
	config.sentinal = 1
	viewdatabase(html_string,"sstocks.db")

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



