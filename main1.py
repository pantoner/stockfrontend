# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(9, 9, 611, 351))
        self.tabWidget.setObjectName("tabWidget")
        self.Download = QtWidgets.QWidget()
        self.Download.setObjectName("Download")
        self.pushButtonWeekly = QtWidgets.QPushButton(self.Download)
        self.pushButtonWeekly.setGeometry(QtCore.QRect(40, 120, 56, 17))
        self.pushButtonWeekly.setDefault(False)
        self.pushButtonWeekly.setObjectName("pushButtonWeekly")
        self.pushButtonDaily = QtWidgets.QPushButton(self.Download)
        self.pushButtonDaily.setGeometry(QtCore.QRect(120, 120, 56, 17))
        self.pushButtonDaily.setObjectName("pushButtonDaily")
        self.pushButtonTickers = QtWidgets.QPushButton(self.Download)
        self.pushButtonTickers.setGeometry(QtCore.QRect(180, 20, 56, 17))
        self.pushButtonTickers.setObjectName("pushButtonTickers")
        self.tabWidget.addTab(self.Download, "")
        self.Indicators = QtWidgets.QWidget()
        self.Indicators.setObjectName("Indicators")
        self.tabWidget.addTab(self.Indicators, "")
        self.Algo = QtWidgets.QWidget()
        self.Algo.setObjectName("Algo")
        self.tabWidget.addTab(self.Algo, "")
        self.Apply = QtWidgets.QWidget()
        self.Apply.setObjectName("Apply")
        self.tabWidget.addTab(self.Apply, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.pushButtonTickers.clicked.connect(MainWindow.getallsymbols)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButtonTickers, self.pushButtonWeekly)
        MainWindow.setTabOrder(self.pushButtonWeekly, self.pushButtonDaily)
        MainWindow.setTabOrder(self.pushButtonDaily, self.tabWidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonWeekly.setText(_translate("MainWindow", "Weekly"))
        self.pushButtonDaily.setText(_translate("MainWindow", "Dailly"))
        self.pushButtonTickers.setText(_translate("MainWindow", "Get Tickers"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Download), _translate("MainWindow", "Download"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Indicators), _translate("MainWindow", "Indicators"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Algo), _translate("MainWindow", "Algo"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Apply), _translate("MainWindow", "Apply"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

