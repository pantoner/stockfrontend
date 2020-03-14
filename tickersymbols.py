import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime
import config
yf.pdr_override() # <== that's all it takes :-)

def formatdate(year,month,day):
	thisdate = str(str(year) +'-'+str(month)+'-'+str(day))
	return thisdate


def getdata(symbol):
	todaydate = datetime.today().strftime('%Y-%m-%d')
	thisstartdate = formatdate(config.startyear,config.startmonth,config.startday)
	thisenddate = formatdate(config.endyear,config.endmonth,config.endday)
	data = pdr.get_data_yahoo(symbol, start=thisstartdate, end= thisenddate)
	print(data)
    #stockprices = data[::-1] #reverses the data by rows
    #closelist = stockprices.Close.values.tolist()
    #highlist = stockprices.High.values.tolist()
    #lowlist = stockprices.Low.values.tolist()
    #print(closelist,highlist,lowlist)

def getallsymbols2():
	symbolraw = pd.read_fwf('nasdaqlisted.txt')
	config.sentinal = 0
	n = 0
	symbollist = []
	while n < len(symbolraw):
		onerow = pd.DataFrame(symbolraw).values[n]
		symbollist.append(onerow[0].split("|", 1)[0])
		n+=1	
	for symbol in symbollist:
		if config.sentinal == 0:
			getdata(symbol)
			print(symbol)
		else:
			print(config.sentinal)
			break

def stopthread():
	config.sentinal = 1

