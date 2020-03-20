from joblib import Parallel, delayed
import multiprocessing
import time
import os
import getmsgpack
import indicatorformulas
import config

def thislistflip(thelist):
	newlist = thelist#[::-1]
	return newlist

def getcloudallmulti(symbol): #pulls before df
	thislist = getmsgpack.readmsgpack(symbol,config.rawstockdatapath)
	closelist = thislistflip(thislist[2])[::-1]
	highlist = thislistflip(thislist[3])[::-1]
	lowlist = thislistflip(thislist[4])[::-1]
	datelist = thislistflip(thislist[6])[::-1]
	n=0
	while n < (len(thislist[2])-77):
		indicatorformulas.getcloud(closelist,highlist,lowlist,datelist,symbol)
		closelist.pop(0);highlist.pop(0);lowlist.pop(0);datelist.pop(0)
		n+=1

def runmulticore(symbollist):
	num_cores = multiprocessing.cpu_count()
	t0 = time.time()
	results = Parallel(n_jobs=num_cores,verbose=5)(delayed(getcloudallmulti)(symbol) for symbol in symbollist)
	t1 = time.time()
	totaltime = t1-10
	print(totaltime)

symbollist = getmsgpack.getonlysymbols()
runmulticore(symbollist)