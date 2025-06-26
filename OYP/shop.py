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
pr = 'shop.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.mywindow = QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.PB.clicked.connect(self.Send)

    def Send(self):
        barkod = self.ui.LE.text()
        say = self.ui.sp.value()

        # MySQL bağlantısı
        conn = mariadb.connect(
            user='root',
            password='123456',  # əgər şifrən varsa buraya yaz
            host='localhost',
            database='mpd'
        )
        cursor = conn.cursor()

        # Barkoda uyğun məhsulu seç, sütun adlarını uyğunlaşdır
        cursor.execute("""
            SELECT `Malin adi` AS ad, Qiymeti AS qiymet, Miqdari AS say 
            FROM table1 
            WHERE Barkod = %s
        """, (barkod,))
        result = cursor.fetchone()

        if result:
            ad, qiymet, movcud_say = result

            if say > movcud_say:
                QMessageBox.warning(self, "Xəta", "Yetərli qədər məhsul yoxdur.")
                return

            yeni_say = movcud_say - say
            cem = qiymet * say

            # Sayını bazada yenilə
            cursor.execute("UPDATE table1 SET Miqdari = %s WHERE Barkod = %s", (yeni_say, barkod))
            conn.commit()

            # Label-ləri yenilə
            self.ui.l1.setText(ad)
            self.ui.l2.setText(str(say))
            self.ui.l3.setText(f"{qiymet:.2f} AZN")
            self.ui.l4.setText(f"{cem:.2f} AZN")
        else:
            QMessageBox.warning(self, "Xəta", "Bu barkod tapılmadı.")

        cursor.close()
        conn.close()




if __name__ == '__main__':
    appl = QApplication(sys.argv)
win = mywindow()
win.show()
sys.exit(appl.exec())
