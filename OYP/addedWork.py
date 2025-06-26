import sys
import mysql.connector
import bcrypt
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QWidget, QMainWindow, QApplication

pr = 'addedWork.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.mywindow = QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # LineEdit-lər və ComboBox
        self.l1 = self.ui.l1  # ad
        self.l2 = self.ui.l2  # soyad
        self.l3 = self.ui.l3  # username
        self.l4 = self.ui.l4  # password
        self.cb = self.ui.cb  # comboBox

        # Gonder düyməsini tap (objectName 'gonder' olmalıdır)
        self.gonder = self.ui.gonder
        self.gonder.clicked.connect(self.save_user)

        self.load_roles()

    def load_roles(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",  # <-- buraya MySQL şifrən
                database="mpd"               # <-- buraya DB adın
            )
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, role_name FROM roles")
            roles = cursor.fetchall()
            self.cb.clear()
            for role in roles:
                self.cb.addItem(role['role_name'], role['id'])
            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Xəta", f"Rol siyahısı yüklənmədi:\n{e}")

    def save_user(self):
        first_name = self.l1.text()
        last_name = self.l2.text()
        username = self.l3.text()
        password = self.l4.text()
        role_id = self.cb.currentData()

        if not all([first_name, last_name, username, password]):
            QMessageBox.warning(self, "Boş sahə", "Zəhmət olmasa bütün xanaları doldurun.")
            return

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",
                database="mpd"
            )
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (first_name, last_name, username, password_hash, role_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (first_name, last_name, username, password_hash, role_id))
            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, "Uğurlu", "İstifadəçi əlavə olundu!")

            # LineEdit-ləri təmizlə
            self.l1.clear()
            self.l2.clear()
            self.l3.clear()
            self.l4.clear()

        except Exception as e:
            QMessageBox.critical(self, "Xəta", f"İstifadəçi əlavə olunmadı:\n{e}")

if __name__ == '__main__':
    appl = QApplication(sys.argv)
    win = mywindow()
    win.show()
    sys.exit(appl.exec())
