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
pr = 'update.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.mywindow = QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.ad.hide()
        self.ui.meblegbtn.hide()
        self.ui.mebleg.hide()
        self.ui.malinadi.hide()
        self.ui.qiymeti.hide()
        self.ui.qiymet.hide()
        self.ui.change.hide()
        self.ui.call.clicked.connect(self.call)
        self.ui.change.clicked.connect(self.change)

    def call(self):
        self.ui.ad.show()
        self.ui.meblegbtn.show()
        self.ui.mebleg.show()
        self.ui.malinadi.show()
        self.ui.qiymeti.show()
        self.ui.qiymet.show()
        self.ui.change.show()

        barkod = self.ui.barkod.text()
        if not barkod:
            QMessageBox.warning(self, "Xəta", "Zəhmət olmasa barkod daxil edin.")
            return

        try:
            connection = mariadb.connect(
                host='localhost', user='root', password='123456', db='mpd'
            )
            cursor = connection.cursor()
            cursor.execute("""
                SELECT `Malin adi`, Qiymeti, Mebleg
                FROM table1
                WHERE Barkod = %s
            """, (barkod,))
            result = cursor.fetchone()

            if result:
                name, qiymet, mebleg = result
                self.ui.malinadi.setText(name)
                self.ui.qiymeti.setText(str(qiymet))
                self.ui.mebleg.setText(str(mebleg))
                self.ui.barkod.setReadOnly(True)
            else:
                QMessageBox.information(self, "Məlumat tapılmadı", "Bu barkod üçün məlumat tapılmadı.")

            cursor.close()
            connection.close()

        except mariadb.Error as err:
            QMessageBox.critical(self, "Xəta", f"Verilənlər bazası xətası:\n{err}")
    def change(self):
        barkod = self.ui.barkod.text()
        name = self.ui.malinadi.text()
        qiymet = self.ui.qiymeti.text()
        mebleg = self.ui.mebleg.text()

        if not (name and qiymet and mebleg):
            QMessageBox.warning(self, "Xəta", "Zəhmət olmasa bütün sahələri doldurun.")
            return

        try:
            connection = mariadb.connect(
                host='localhost', user='root', password='123456', db='mpd'
            )
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE table1
                SET `Malin adi` = %s,
                    Qiymeti = %s,
                    Mebleg = %s
                WHERE Barkod = %s
            """, (name, qiymet, mebleg, barkod))

            connection.commit()
            cursor.close()
            connection.close()

            QMessageBox.information(self, "Uğurla", "Məlumat uğurla yeniləndi.")
            self.ui.barkod.setReadOnly(False)

        except mariadb.Error as err:
            QMessageBox.critical(self, "Xəta", f"Verilənlər bazası xətası:\n{err}")


    
   

if __name__ == '__main__':
    appl = QApplication(sys.argv)
win = mywindow()
win.show()
sys.exit(appl.exec())
