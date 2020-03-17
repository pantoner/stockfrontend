import umsgpack
import tickersymbols
import config
import json

def getmsgpack(symbol,path):
	with open('{}/{}.msgpack'.format(path,symbol), 'rb') as data_file:
		datamsgpk = umsgpack.unpack(data_file,raw=False)
		datajson = json.loads(datamsgpk)
	return datajson

def readmsgpack(symbol):
	datajson = getmsgpack(symbol,path)
	symbol = datajson["symbol"]
	openlist = datajson["openlist"]
	closelist = datajson["closelist"]
	lowlist = datajson["highlist"]
	volumelist = datajson["volumelist"]
	datelist = datajson["datelist"]
	print(symbol)
	return (symbol,openlist,closelist,lowlist,volumelist,datelist)

symbollist = tickersymbols.getonlysymbols()
path = config.rawstockdatapath = "C:/Users/VH189DW/Documents/weeklydata"

for symbol in symbollist:
	try:
		eachattribute = readmsgpack(symbol)
		break
	except:
		continue


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