import sys
from PyQt5.QtWidgets import (QWidget, QTableWidget,QApplication, QTableWidgetItem, QHBoxLayout)
from PyQt5 import QtWidgets,QtGui,QtCore,QtSql
from PyQt5.QtWidgets import QMainWindow, QApplication,QTableView
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QSize, Qt
from cmd import Ui_MainWindow
class mywindow(QtWidgets.QMainWindow): 
    def __init__(self):
          super(mywindow, self).__init__()
          self.mywindow = QWidget()
          self.ui = Ui_MainWindow()
          self.ui.setupUi(self)
          self.ui.calendarWidget.hide()
          self.ui.pushButton_10.clicked.connect(self.aa)
          
    def aa(self):
        self.ui.calendarWidget.show()
    
        

      








if __name__ == '__main__':
    appl=QApplication(sys.argv)
win = mywindow()
win.show()
sys.exit(appl.exec())
