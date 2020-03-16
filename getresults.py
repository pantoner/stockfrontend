import pandas as pd
import sqlite3
from pandas_datareader import data as pdr
import yfinance as yf
from datetime import datetime
import webbrowser
import config
import warnings
warnings.simplefilter(action='ignore')

database = 'sstocks.db'

symbolraw = pd.read_fwf('nasdaqlisted.txt')
n = 0
symbollist = []
while n < len(symbolraw):
    onerow = pd.DataFrame(symbolraw).values[n]
    symbollist.append(onerow[0].split("|", 1)[0])
    n+=1
print(symbollist)

def viewdatabase(database):
	conn = sqlite3.connect(database)
	conn.text_factory = bytes
	df = pd.read_sql_query("select * from cloud",conn)
	return df
day1openlist=[]
day1closelist=[]
day2openlist=[]
day2closelist=[]
day3openlist=[]

df = viewdatabase(database)
notdf = pd.to_datetime(df.Date.str.decode("utf-8"))
dfdates = pd.DataFrame(notdf)
#dfdates = dfdates.columns = ['Date2']
df2 = pd.merge(df,dfdates,how ='left',left_index=True,right_index=True)
df2 = df2.sort_values(by='Date_y',ascending = False)
symbollist
for symbol in symbollist:
	df2['Symbol'] = df2['Symbol'].str.decode("utf-8")
	thisdf = df2[df2['Symbol'] == symbol]
	thisdf['Day2willB'] = thisdf.Date_y.shift(1)
	thisdf['Day3willB'] = thisdf.Date_y.shift(2)
	thisdf.rename(columns = {'Date_y':'Day1is'}, inplace = True)
	thisdf = thisdf.reset_index()
	print(thisdf)
	# for index in thisdf.index[::-1]:
	# 	print(index)
		# print(type(int(index)))
		# day1openlist.append(thisdf.Open[index])
		# day1closelist.append(thisdf.Close[index])
		# day2openlist.append(thisdf.Open[index+1])
		# day2closelist.append(thisdf.Close[index+1])
		# try:
		# 	 day3openlist.append(thisdf.Open[index+2])
		# except:
		# 	print(day3openlist)
		# 	break
#print(dfdates)
#print(dfdates.sort_values(by='Date',ascending = False))

