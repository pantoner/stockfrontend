sentinal = 0

startyear = "2019"
startmonth = "1"
startday = "1"

endyear = ""
endmonth = ""
endday = ""

#outcome = pd.DataFrame(outcomelist)
dbname = 'sstocks.db'
tablename = 'cloud'
#outcome.to_sql(tablename, conn, if_exists='append')
#print('data has been entered into database')
rawstockdatapath = ""
dailycloud = "C:/Users/VH189DW/Documents/Indicators/Cloud"

html_string = html_string = '''
				<html>
				  <head><title>HTML Pandas Dataframe with CSS</title></head>
				  <link rel="stylesheet" type="text/css" href="df_style.css"/>
				  <body>
					{table}
				  </body>
				</html>.
				'''