import ctypes
from math import *
import sys
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QApplication, QTableWidgetItem, QHBoxLayout)
from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QSize, Qt
pr = 'kalkulyator.ui'
Ui_MainWindow, QtBaseClass =uic.loadUiType(pr)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.mywindow = QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.PB1.clicked.connect(self.Plus)
        self.ui.PB2.clicked.connect(self.Minus)
        self.ui.PB3.clicked.connect(self.Vurma)
        self.ui.PB4.clicked.connect(self.Bolma)
        self.ui.PB6.clicked.connect(self.quvvat)
        self.ui.PB7.clicked.connect(self.clear)
       
        self.ui.OK5.setVisible(False)
        self.ui.LE4.setVisible(False)
        self.ui.OK5.clicked.connect(self.sil)

    def sil(self):
        self.ui.OK5.setVisible(False)
        self.ui.LE4.setVisible(False)
    def clear(self):
        self.ui.LE1.setText(" ")
        self.ui.LE2.setText(" ")
        self.ui.LE3.setText(" ")
    def Plus(self):
        a = float(self.ui.LE1.text())
        b = float(self.ui.LE2.text())
        c = a+b
        self.ui.LE3.setText(str(c))

    def Minus(self):
        a = float(self.ui.LE1.text())
        b = float(self.ui.LE2.text())
        c = a-b
        self.ui.LE3.setText(str(c))

    def Vurma(self):
        a = float(self.ui.LE1.text())
        b = float(self.ui.LE2.text())
        c = a*b
        self.ui.LE3.setText(str(c))

    def Bolma(self):
        a = float(self.ui.LE1.text())
        b = float(self.ui.LE2.text())
        if b==0:
            ctypes.windll.user32.MessageBoxW(0,"Sifra bolmek olmaz!", "Diqqat !",16)
            self.ui.LE4.setVisible(True)
            self.ui.OK5.show()
            h="Sifira bolmek olmaz..!"
            self.ui.LE4.setText(h)
        else:
            c = a/b
            self.ui.LE3.setText(str(c))
        

    def quvvat(self):
        a = float(self.ui.LE1.text())
        b = float(self.ui.LE2.text())
        c = a**b
        self.ui.LE3.setText(str(c))
    


if __name__ == '__main__':
    appl = QApplication(sys.argv)
win = mywindow()
win.show()
sys.exit(appl.exec())
