import sys
import json
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget
from subprocess import Popen

pr = 'esas.ui'  # əsas UI
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.mywindow = QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.OK1.clicked.connect(self.OK1)
        self.ui.OK2.clicked.connect(self.OK2)
        self.ui.OK3.clicked.connect(self.OK3)
        self.ui.OK5.clicked.connect(self.OK5)
        self.ui.OK9.clicked.connect(self.OK9)
        self.ui.OK4.clicked.connect(self.logout)  # logout düyməsi

        self.ui.L.setVisible(False)
        self.ui.P.setVisible(False)
        self.ui.PP.setVisible(False)

        try:
            with open("session.json", "r", encoding="utf-8") as f:
                user_info = json.load(f)
                full_name = f"{user_info['first_name']} {user_info['last_name']}"
                role = user_info['role']

                self.ui.L2.setText(full_name)
                self.ui.L3.setText(role)
        except Exception as e:
            print("İstifadəçi məlumatı oxunmadı:", e)
            self.ui.L2.setText("Bilinməyən istifadəçi")
            self.ui.L3.setText("N/A")

    def logout(self):
        # session.json faylını sil
        if os.path.exists("session.json"):
            os.remove("session.json")
        # Cari pəncərəni bağla
        self.close()
        # Login pəncərəsini aç (login.py-ni işə sal)
        Popen(["python", "Login.py"])

    def OK1(self):
        from subprocess import call
        call(["python", "lab21.py"])

    def OK3(self):
        from subprocess import call
        call(["python", "kal.py"])

    def OK2(self):
        from subprocess import call
        call(["python", "kassa1.py"])

    def OK5(self):
        from subprocess import call
        call(["python", "addedWork.py"])


    def OK9(self):
        from subprocess import call
        call(["python", "shopPro.py"])



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())




# import ctypes
# from math import *
# import sys
# import webbrowser
# import subprocess
# from PyQt5.QtWidgets import (
#     QWidget, QTableWidget, QApplication, QTableWidgetItem, QHBoxLayout)
# from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
# from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView
# from PyQt5 import uic
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtCore import QSize, Qt
# import json
# pr = 'esas.ui'
# Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)


# class mywindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(mywindow, self).__init__()
#         self.mywindow = QWidget()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         self.ui.OK1.clicked.connect(self.OK1)
#         self.ui.OK2.clicked.connect(self.OK2)
#         self.ui.OK3.clicked.connect(self.OK3)
#         self.ui.OK4.clicked.connect(self.close)
#         self.ui.L.setVisible(False)
#         self.ui.P.setVisible(False)
#         self.ui.PP.setVisible(False)

#     def OK1(self):
#         from subprocess import call
#         call(["python", "lab21.py"])

#     def OK3(self):
#         from subprocess import call
#         call(["python", "kal.py"])

#     def OK2(self):
#         from subprocess import call
#         call(["python", "kassa1.py"])
   

        


# if __name__ == '__main__':
#     appl = QApplication(sys.argv)
# win = mywindow()
# win.show()
# sys.exit(appl.exec())
