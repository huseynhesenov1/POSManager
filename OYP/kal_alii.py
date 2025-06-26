import sys
import ctypes
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QApplication, QTableWidgetItem, QHBoxLayout)
from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QSize, Qt
pr = 'kal_ali.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.mywindow = QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.P1.clicked.connect(self.bir)
        # self.ui.P2.clicked.connect(self.iki)
        # self.ui.P3.clicked.connect(self.uc)
        # self.ui.P4.clicked.connect(self.dort)
        # self.ui.P5.clicked.connect(self.bes)
        # self.ui.P6.clicked.connect(self.alti)
        # self.ui.P7.clicked.connect(self.yeddi)
        # self.ui.P8.clicked.connect(self.sekkiz)
        # self.ui.P9.clicked.connect(self.doqquz)
        # self.ui.P0.clicked.connect(self.sifir)
        # (1 yazanda istenilen qeder yaza bilsin meselen 11)(biri istediyim xanaya yaza bilim////)(silmeni,massagebox)

    def bir(self):
        self.ui.LE1.setText(str(1))


if __name__ == '__main__':
    appl = QApplication(sys.argv)
win = mywindow()
win.show()
sys.exit(appl.exec())
