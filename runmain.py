from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from main1 import Ui_MainWindow
import pandas as pd
import tickersymbols

pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
#ftp.nasdaqtrader.com/symboldirectory
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()
        self.dailydownloadthread = DailyDownLoadThread()
       
    def getallsymbols(self):
    	self.dailydownloadthread.start()

class DailyDownLoadThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')
    def __init__(self):
        QThread.__init__(self)       

    def run(self):
    	tickersymbols.getallsymbols2()

#https://stackoverflow.com/questions/10636024/python-pandas-gui-for-viewing-a-dataframe-or-matrix
if __name__ == '__main__':
  app = QApplication([])
  w = MainWindow()
  app.exec_()