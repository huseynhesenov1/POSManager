import sys
import ctypes
import mysql.connector
import bcrypt
import json
from subprocess import Popen
from PyQt5 import QtWidgets, uic

pr = 'hoci.ui'  # Login form UI
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.LE2.setEchoMode(2)  # Password mask
        self.ui.OK.clicked.connect(self.try_login)

    def try_login(self):
        username = self.ui.LE1.text().strip()
        password = self.ui.LE2.text().strip()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="mpd"
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT u.first_name, u.last_name, u.username, u.password_hash, r.role_name
                FROM users u
                JOIN roles r ON u.role_id = r.id
                WHERE u.username = %s
            """, (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"DB Xətası: {e}", "Diqqət!", 0)
            return

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            user_info = {
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "role": user["role_name"]
            }
            with open("session.json", "w", encoding="utf-8") as f:
                json.dump(user_info, f)

            ctypes.windll.user32.MessageBoxW(0, "Sisteme xoş gəldiniz!", "Uğurlu giriş", 0)
            self.ui.LE1.setText("")
            self.ui.LE2.setText("")
            Popen(["python", "esas.py"])
        else:
            ctypes.windll.user32.MessageBoxW(0, "Username və ya Parol yanlışdır!", "Diqqət!", 0)
            self.ui.LE1.setText("")
            self.ui.LE2.setText("")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())




# import sys
# import ctypes
# from PyQt5.QtWidgets import (
#     QWidget, QTableWidget, QApplication, QTableWidgetItem, QHBoxLayout)
# from PyQt5 import QtWidgets, QtGui, QtCore, QtSql
# from PyQt5.QtWidgets import QMainWindow, QApplication, QTableView
# from PyQt5 import uic
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtCore import QSize, Qt
# pr = 'hoci.ui'
# Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)


# class mywindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super(mywindow, self).__init__()
#         self.mywindow = QWidget()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         self.ui.LE2.setEchoMode(2)
#         self.ui.OK.clicked.connect(self.OK)

#     def OK(self):
#         file = open("parol2.txt", "r")
#         a = file.read(6)
#         b = file.read()
#         file.close()
#         chek = 0
#         login1 = a.strip()
#         parol1 = b.strip()
#         login = self.ui.LE1.text()
#         parol = self.ui.LE2.text()
#         if login == login1 and parol == parol1:
#             chek = 1
#         if chek == 1:
#             ctypes.windll.user32.MessageBoxW(
#                 0, "Sisteme xoş geldiniz !", "Diqqet !", 0)
#             from subprocess import call
#             call(["python", "esas.py"])
#         else:
#             ctypes.windll.user32.MessageBoxW(
#                 0, "Username ve ya Parol yanlisdir !", "Diqqat !", 0)
#         self.ui.LE1.setText("")
#         self.ui.LE2.setText("")
#         #guvenli cixis etdikde ve parol sevh yazildiqda le1 le2 nin icicni silir
        


# if __name__ == '__main__':
#     appl = QApplication(sys.argv)
# win = mywindow()
# win.show()
# sys.exit(appl.exec())
