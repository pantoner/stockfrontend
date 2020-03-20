
import pandas as pd
import config
import indicatorformulas
import getmsgpack

path = config.rawstockdatapath = "C:/Users/VH189DW/Documents/twoyearsdata" 

def thislistflip(thelist):
	newlist = thelist#[::-1]
	return newlist


# def getonlysymbols(): #this creates the symbollist from nasdaq
# 	symbolraw = pd.read_fwf('nasdaqlisted.txt')
# 	config.sentinal = 0
# 	n = 0
# 	symbollist = []
# 	while n < len(symbolraw):
# 		onerow = pd.DataFrame(symbolraw).values[n]
# 		symbollist.append(onerow[0].split("|", 1)[0])
# 		n+=1
# 	return symbollist


def getcloudall(symbol,path): #pulls before df
	thislist = getmsgpack.readmsgpack(symbol,path)
	closelist = thislistflip(thislist[2])[::-1]
	highlist = thislistflip(thislist[3])[::-1]
	lowlist = thislistflip(thislist[4])[::-1]
	datelist = thislistflip(thislist[6])[::-1]
	n=0
	while n < (len(thislist[2])-77):
		indicatorformulas.getcloud(closelist,highlist,lowlist,datelist,symbol)
		closelist.pop(0);highlist.pop(0);lowlist.pop(0);datelist.pop(0)
		n+=1


symbollist = getmsgpack.getonlysymbols()
for symbol in symbollist:
	try:
		getcloudall(symbol,path)
	except FileNotFoundError:
		print('file not found error {}'.format(symbol))
		continue
	except OSError: 
		print('OS error {}'.format(symbol))
		break

# dashboarddata = pickle.load( open( "dashboard.p", "rb" ) )
# print(dashboarddata)
# winprice = dashboarddata['takewin']
# loseprice = dashboarddata['stoploss']

# if os.path.exists("ohlcvdir.p"):
#     directory = pickle.load( open( "ohlcvdir.p", "rb" ) ) #source
#     path = directory['ohlcvdir']
# else:
#     exit()


# def getbucketname():
#     if os.path.exists("bucketname.p"):
#         bucket = pickle.load( open( "bucketname.p", "rb" ) ) #source
#         bucketname = bucket['bucketname']
#     else:
#         print('no bucket defined')
#         exit()
#     return bucketname

#         hmtwsl = dict({'howmany': howmany, 'takewin': takewin, 'stoploss': stoploss})
#         pickle.dump( hmtwsl, open( "hmtwsl.p", "wb" ) )

#  if os.path.exists("directory.p"):
#             os.remove("directory.p")
#         if fileName:
#             directory = dict({'dir': fileName})
#             pickle.dump(directory, open( "directory.p", "wb" ) )
#             print(fileName)
#             self.lineEdit_dir.setText(fileName)