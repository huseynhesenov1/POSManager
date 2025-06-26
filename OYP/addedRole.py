import sys
import mysql.connector
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QWidget, QMainWindow, QApplication

pr = 'addedRole.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.mywindow = QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Gonder düyməsini tap və event bağla
        self.ui.gonder.clicked.connect(self.add_role)

    def add_role(self):
        role_name = self.ui.l1.text().strip()

        if not role_name:
            QMessageBox.warning(self, "Boş daxil etmə", "Zəhmət olmasa rol adını daxil edin.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456",  # Öz MySQL şifrən
                database="mpd"      # Öz database adın
            )
            cursor = conn.cursor()

            # Rolun olub olmadığını yoxla
            cursor.execute("SELECT id FROM roles WHERE role_name = %s", (role_name,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Təkrar", "Bu rol artıq mövcuddur.")
            else:
                cursor.execute("INSERT INTO roles (role_name) VALUES (%s)", (role_name,))
                conn.commit()
                QMessageBox.information(self, "Uğurlu", f"{role_name} rolu əlavə olundu.")
                self.ui.l1.clear()

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Xəta", f"Rol əlavə olunmadı:\n{e}")

if __name__ == '__main__':
    appl = QApplication(sys.argv)
    win = mywindow()
    win.show()
    sys.exit(appl.exec())
