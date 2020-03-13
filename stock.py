import pandas as pd
from datetime import datetime
from pandas_datareader import data as pdr
import yfinance as yf
import indicators
import sqlite3
import rolling

symbolraw = pd.read_fwf('C://Python37//nasdaqlisted.txt')
n = 0
symbollist = []
while n < len(symbolraw):
    onerow = pd.DataFrame(symbolraw).values[n]
    symbollist.append(onerow[0].split("|", 1)[0])
    n+=1
print(symbollist)

yf.pdr_override() # <== that's all it takes :-)
todaydate = datetime.today().strftime('%Y-%m-%d')

todaydate = datetime.today().strftime('%Y-%m-%d')

# thiscloud

def gettotals(symbol,popyes):
    data = pdr.get_data_yahoo(symbol, start="2019-10-01", end= todaydate)
    stockprices = data[::-1] #reverses the data by rows
    closelist = stockprices.Close.values.tolist()
    highlist = stockprices.High.values.tolist()
    lowlist = stockprices.Low.values.tolist()
    if popyes == 'yes':
        nextclose = closelist[0]
        closelist.pop(0)
        highlist.pop(0)
        lowlist.pop(0)
    h_max9 = rolling.Max(highlist, 9)
    high9 = list(h_max9)
    h_max9 = rolling.Max(highlist, 9)
    l_min9 = rolling.Min(lowlist, 9)
    high9 = list(h_max9)
    low9 = list(l_min9)
    high9+low9
    tenkan_sen = [(x + y)/2 for x, y in zip(high9,low9)]
    h_max26 = rolling.Max(highlist, 26)
    l_min26 = rolling.Min(lowlist, 26)
    high26 = list(h_max26)
    low26 = list(l_min26)
    high26+low26
    kijun_sen = [(x + y)/2 for x, y in zip(high26,low26)]
    sa = [(x + y)/2 for x, y in zip(kijun_sen,tenkan_sen)]
    clouda = (sa[26] - closelist[0])/closelist[0]
    kijun_sen2 = (kijun_sen[0] - closelist[0])/closelist[0]
    tenkan_sen2 = (tenkan_sen[0] - closelist[0])/closelist[0]
   
    h_max52 = rolling.Max(highlist, 52)
    l_min52 = rolling.Min(lowlist, 52)
    high52 = list(h_max52)
    low52 = list(l_min52)
    sb = [(x + y)/2 for x, y in zip(high52,low52)]
    cloudb = (sb[26] - closelist[0])/closelist[0]
    
    df = pd.DataFrame(highlist,columns=['High'])
    pd.DataFrame(lowlist,columns=['Low'])
    pd.DataFrame(closelist,columns=['Close'])
    df = pd.concat([pd.DataFrame(lowlist,columns=['Low']).reset_index(drop=True),df.reset_index(drop=True)], axis=1)
    df = pd.concat([pd.DataFrame(closelist,columns=['Close']).reset_index(drop=True),df.reset_index(drop=True)], axis=1)
    n=21
    dfbb = df.iloc[::-1]
    bb = indicators.bollinger_bands(dfbb, n)
    Bollingerpercb = bb.iloc[-1].Bollingerpercb
    Bollingerpercb
    rsi = indicators.relative_strength_index(df, n)
    RSI = rsi.iloc[-1].RSI
    print(clouda,Bollingerpercb,RSI)
    outcomedict = {'todaydate':todaydate, 'symbol':symbol,'sacloud':clouda,'sbcloud':cloudb,'kijun_sen':kijun_sen2,'tenkan_sen2':tenkan_sen2,'Bollingerpercb':Bollingerpercb,'RSI':RSI,'nextclose':nextclose/closelist[0]}
    print(outcomedict)
    return outcomedict

outcomelist = []   
for symbol in symbollist:
    try:
        outcomedict = gettotals(symbol,'yes')
        outcomelist.append(outcomedict)      
    except IndexError:
        continue
    except:
        continue
print(outcomelist)

outcome = pd.DataFrame(outcomelist)
DB_NAME = 'sstocks.db'
conn = sqlite3.connect(DB_NAME)
outcome.to_sql('cloud', conn, if_exists='append')
print('data has been entered into database')