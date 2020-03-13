import pandas as pd
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime
yf.pdr_override() # <== that's all it takes :-)

def getdata(symbol):
	todaydate = datetime.today().strftime('%Y-%m-%d')
	data = pdr.get_data_yahoo(symbol, start="2019-10-01", end= todaydate)
	print(data)
    #stockprices = data[::-1] #reverses the data by rows
    #closelist = stockprices.Close.values.tolist()
    #highlist = stockprices.High.values.tolist()
    #lowlist = stockprices.Low.values.tolist()
    #print(closelist,highlist,lowlist)

def getallsymbols2():
	symbolraw = pd.read_fwf('nasdaqlisted.txt')
	n = 0
	symbollist = []
	while n < len(symbolraw):
		onerow = pd.DataFrame(symbolraw).values[n]
		symbollist.append(onerow[0].split("|", 1)[0])
		n+=1	
	for symbol in symbollist:
		getdata(symbol)
