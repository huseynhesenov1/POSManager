import ctypes
import random
from datetime import datetime
from math import *
import sys
import webbrowser
import subprocess
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QApplication, QTableWidgetItem, QHBoxLayout)
from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QSize, Qt
import mysql.connector as mariadb
pr = 'create.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.mywindow = QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.add.clicked.connect(self.add)

    
    def add(self):
        barkod = self.ui.barkod.text()
        name = self.ui.ad.text()
        qiymet = float(self.ui.qiymet.text())
        miqdar = float(self.ui.miqdar.text())
        mebleg = qiymet * miqdar
        edv = mebleg * 0.18  
        umumi_cem = mebleg + edv
        tarix = datetime.now().strftime('%Y-%m-%d')  

        try:
            connection = mariadb.connect(
                host='localhost', user='root', password='123456', db='mpd'
            )
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO table1 (Barkod, `Malin adi`, Qiymeti, Miqdari, Mebleg, EDV, `Umumi Cem`, Tarix)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (barkod, name, qiymet, miqdar, mebleg, edv, umumi_cem, tarix))

            connection.commit()
            cursor.close()
            connection.close()
            QMessageBox.information(self, "Uğurla əlavə edildi", "Məlumat bazaya əlavə olundu!")
            from subprocess import call
            call(["python", "lab21.py"])
        except mariadb.Error as err:
            QMessageBox.critical(self, "Xəta baş verdi", f"Xəta: {err}")

if __name__ == '__main__':
    appl = QApplication(sys.argv)
win = mywindow()
win.show()
sys.exit(appl.exec())
