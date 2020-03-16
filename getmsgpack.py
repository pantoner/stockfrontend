import umsgpack
import tickersymbols
import config




def getmsgpackdata(symbollist,path):
	for symbol in symbollist:
		with open('{}/{}.msgpack'.format(path,symbol), 'rb') as data_file:
		    data_loaded = umsgpack.unpack(data_file,raw=False)
		    print(data_loaded)


symbollist = tickersymbols.getonlysymbols()
getmsgpackdata(symbollist,config.rawstockdatapath)