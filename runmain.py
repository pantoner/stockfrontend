import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import QMessageBox
from main6 import Ui_MainWindow
import pandas as pd
import pickle
from datetime import datetime
import tickersymbols
import config

pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
#ftp.nasdaqtrader.com/symboldirectory
class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)
		self.show()
		self.dailydownloadthread = DailyDownLoadThread()
		self.weeklydownloadthread = WeeklyDownLoadThread()
		config.startyear = self.dateEditStart.date().year();config.startmonth = self.dateEditStart.date().month();config.startday = self.dateEditStart.date().day()
		config.endyear = self.dateEditEnd.date().year();config.endmonth = self.dateEditEnd.date().month();config.endday = self.dateEditEnd.date().day()
		self.checkBoxToday.stateChanged.connect(self.CalendarHide)


	def getallsymbols(self):
		config.startyear = self.dateEditStart.date().year();config.startmonth = self.dateEditStart.date().month();config.startday = self.dateEditStart.date().day()
		config.endyear = self.dateEditEnd.date().year();config.endmonth = self.dateEditEnd.date().month();config.endday = self.dateEditEnd.date().day()
		if self.radioButtonDaily.isChecked():
			config.rawstockdatapath = "C:/Users/VH189DW/Documents/twoyearsdata/"
			self.pushButtonStop.setEnabled(True)
			self.pushButtonTickers.setEnabled(False)
			self.dailydownloadthread.start()
		if self.radioButtonWeekly.isChecked():
			config.rawstockdatapath = "C:/Users/VH189DW/Documents/weeklydata"
			self.dateEditStart.setEnabled(False)
			self.dateEditEnd.setEnabled(False)
			self.checkBoxToday.setEnabled(False)
			self.pushButtonStop.setEnabled(True)
			self.pushButtonTickers.setEnabled(False)
			self.weeklydownloadthread.start()


	def stopdailydownload(self):  #stops daily or weekly data
		QMessageBox.about(self, "See Data", "Press to Wait for Data!")
		self.pushButtonStop.setEnabled(False)
		self.pushButtonTickers.setEnabled(True)
		self.dateEditStart.setEnabled(True)
		self.dateEditEnd.setEnabled(True)
		self.checkBoxToday.setEnabled(True)
		self.dailydownloadthread.stopdailydownload()
		

	def CalendarHide(self, state):
		if self.checkBoxToday.isChecked(): 
			self.dateEditEnd.setEnabled(False)
			config.endyear = datetime.today().strftime('%Y')
			config.endmonth = datetime.today().strftime('%m')
			config.endday = datetime.today().strftime('%d')
		else: 
			self.dateEditEnd.setEnabled(True)

	def browseforstockdir(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		fileName = os.path.dirname(fileName)
		if os.path.exists("stocksdir.p"):
			os.remove("stocksdir.p")
		if fileName:
			directory = dict({'stocksdir': fileName})
			pickle.dump(directory, open( "stocksdir.p", "wb" ) )
			print(fileName)
			config.rawstockdatapath = filename
			self.lineEditStockDir.setText(fileName)

class DailyDownLoadThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)       

	def run(self):
		tickersymbols.getallsymbols2()

	def stopdailydownload(self):
		tickersymbols.stopthread()

class WeeklyDownLoadThread(QThread):
	signal = pyqtSignal('PyQt_PyObject')
	def __init__(self):
		QThread.__init__(self)       

	def run(self):
		tickersymbols.getallsymbolsweekly()

	def stopdailydownload(self):
		tickersymbols.stopthread()

#https://stackoverflow.com/questions/10636024/python-pandas-gui-for-viewing-a-dataframe-or-matrix
if __name__ == '__main__':
  app = QApplication([])
  w = MainWindow()
  app.exec_()