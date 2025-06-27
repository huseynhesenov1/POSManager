import ctypes
import random
import bcrypt
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from datetime import datetime
import sys
import os
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QApplication, QTableWidgetItem)
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import json
from subprocess import Popen
import uuid
import json
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox
import mysql.connector
from reportlab.graphics.barcode import code128
from reportlab.lib.units import mm


pr = 'shopPro.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)


class mywindow(QtWidgets.QMainWindow):
        def __init__(self):
            super(mywindow, self).__init__()
            self.mywindow = QWidget()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

            self.ui.send.clicked.connect(self.Send)
            self.ui.tamamla.clicked.connect(self.Tamamla)
            self.ui.btnSil.clicked.connect(self.verify_and_delete)
            self.ui.OK4.clicked.connect(self.logout)  # logout düyməsi
            self.ui.table.setColumnCount(5)
            self.ui.table.setHorizontalHeaderLabels([
                "Nömrə", "Ad", "Say", "Məbləğ", "Cəm"])
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


        def Send(self):
            barkod = self.ui.LE.text()
            say = self.ui.sp.value()

            conn = mysql.connector.connect(
                user='root', password='123456', host='localhost', database='mpd')
            cursor = conn.cursor()

            cursor.execute("""
                    SELECT `Malin adi` AS ad, Qiymeti AS qiymet, Miqdari AS say
                    FROM table1
                    WHERE Barkod = %s
                """, (barkod,))
            result = cursor.fetchone()

            if result:
                ad, qiymet, movcud_say = result
                cem = qiymet * say
                row = self.ui.table.rowCount()
                self.ui.table.insertRow(row)
                self.ui.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
                self.ui.table.setItem(row, 1, QTableWidgetItem(ad))
                self.ui.table.setItem(row, 2, QTableWidgetItem(str(say)))
                self.ui.table.setItem(row, 3, QTableWidgetItem(f"{qiymet:.2f}"))
                self.ui.table.setItem(row, 4, QTableWidgetItem(f"{cem:.2f}"))

                # Table-dakı ümumi cəmi hesablamaq
                umumi_cem = 0.0
                for i in range(self.ui.table.rowCount()):
                    item = self.ui.table.item(i, 4)
                    if item:
                        umumi_cem += float(item.text())

                self.ui.labelTotal.setText(f"Ümumi məbləğ: {umumi_cem:.2f}")

            else:
                QMessageBox.warning(self, "Xəta", "Bu barkod tapılmadı.")

            cursor.close()
            conn.close()



        def Tamamla(self):
            conn = mysql.connector.connect(
                user='root', password='123456', host='localhost', database='mpd')
            cursor = conn.cursor()

            try:
                # ➤ 1. Kassir adı session.json-dan götürülür
                try:
                    with open("session.json", "r", encoding="utf-8") as f:
                        user_info = json.load(f)
                        cashier_name = f"{user_info['first_name']} {user_info['last_name']}"
                except Exception:
                    cashier_name = "Bilinməyən kassir"

                # ➤ 2. Ümumi məbləği hesabla
                total_price = 0.0
                for row in range(self.ui.table.rowCount()):
                    item = self.ui.table.item(row, 4)
                    if item:
                        total_price += float(item.text())

                # ➤ 3. Unikal 10 simvolluq fiscal_id yaradılır
                fiscal_id = self.generate_unique_fiscal_id(cursor)

                # ➤ 4. sales cədvəlinə INSERT
                cursor.execute("""
                    INSERT INTO sales (fiscal_id, cashier_name, total_price)
                    VALUES (%s, %s, %s)
                """, (fiscal_id, cashier_name, total_price))

                sale_id = cursor.lastrowid

                # ➤ 5. sale_items və table1 UPDATE
                for row in range(self.ui.table.rowCount()):
                    ad = self.ui.table.item(row, 1).text()
                    satis_sayi = int(self.ui.table.item(row, 2).text())
                    qiymet = float(self.ui.table.item(row, 3).text())

                    cursor.execute("SELECT Barkod, Miqdari FROM table1 WHERE `Malin adi` = %s", (ad,))
                    result = cursor.fetchone()

                    if result:
                        barkod, movcud_say = result
                        yeni_say = movcud_say - satis_sayi

                        cursor.execute("UPDATE table1 SET Miqdari = %s WHERE Barkod = %s", (yeni_say, barkod))

                        cursor.execute("""
                            INSERT INTO sale_items (sale_id, product_id, product_name, quantity, unit_price)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (sale_id, barkod, ad, satis_sayi, qiymet))
                    else:
                        QMessageBox.warning(self, "Xəta", f"{ad} məhsulu tapılmadı və yazılmadı.")

                # ➤ 6. Dəyişiklikləri saxla
                conn.commit()

                # ➤ 7. Qəbz yaz və UI təmizlə
                self.PDFYaz(fiscal_id=fiscal_id, cashier_name=cashier_name)
                QMessageBox.information(self, "Uğur", f"Satış (Fiskal ID: {fiscal_id}) uğurla yadda saxlanıldı!")
                self.ui.table.setRowCount(0)

            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Xəta", f"Satış saxlanılarkən xəta baş verdi:\n{str(e)}")

            finally:
                cursor.close()
                conn.close()

        def generate_unique_fiscal_id(self, cursor):
            import string
            while True:
                fiscal_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                cursor.execute("SELECT COUNT(*) FROM sales WHERE fiscal_id = %s", (fiscal_id,))
                if cursor.fetchone()[0] == 0:
                    return fiscal_id

       





    


        def logout(self):
            # session.json faylını sil
            if os.path.exists("session.json"):
                os.remove("session.json")
            # Cari pəncərəni bağla
            self.close()
            # Login pəncərəsini aç (login.py-ni işə sal)
            Popen(["python", "Login.py"])


        def PDFYaz(self, fiscal_id=None, cashier_name=None):
            pdfmetrics.registerFont(
                TTFont('Arial', 'C:\\Windows\\Fonts\\arial.ttf'))
            tarix_saat = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            downloads = os.path.join(os.path.expanduser("~"), "Downloads")
            if not os.path.exists(downloads):
                os.makedirs(downloads)
            pdf_path = os.path.join(downloads, f"cek_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf")

            c = canvas.Canvas(pdf_path, pagesize=A4)
            width, height = A4

            # Logo
            logo_path = "C:\\Users\\ACER\\Desktop\\logo\\loqomain.png"
            if os.path.exists(logo_path):
                logo = ImageReader(logo_path)
                c.drawImage(logo, 50, height - 80, width=80, height=50, mask='auto')

            c.setFont("Arial", 14)
            c.drawString(200, height - 50, "ÇEK QƏBZI")

            # Tarix, saat və kassir adı
            c.setFont("Arial", 10)
            y = height - 90
            c.drawString(400, y, f"Tarix və Saat: {tarix_saat}")
            y -= 15
            if cashier_name:
                c.drawString(400, y, f"Kassir: {cashier_name}")
            else:
                c.drawString(400, y, f"Kassir: Bilinməyən")

            # Cədvəlin başlıqları
            y = height - 130
            c.drawString(50, y, "Məhsul")
            c.drawString(200, y, "Say")
            c.drawString(260, y, "Qiymət")
            c.drawString(330, y, "Məbləğ")
            y -= 20

            umumi_mebleg = 0

            for row in range(self.ui.table.rowCount()):
                ad = self.ui.table.item(row, 1).text()
                say = int(self.ui.table.item(row, 2).text())
                qiymet = float(self.ui.table.item(row, 3).text())
                mebleg = say * qiymet
                umumi_mebleg += mebleg
                c.drawString(50, y, ad)
                c.drawString(200, y, str(say))
                c.drawString(260, y, f"{qiymet:.2f}")
                c.drawString(330, y, f"{mebleg:.2f}")
                y -= 20
                if y < 120:
                    c.showPage()
                    y = height - 100
                    c.setFont("Arial", 10)

            c.setFont("Arial", 12)
            c.drawString(50, y - 20, f"CƏMİ MƏBLƏĞ: {umumi_mebleg:.2f} AZN")

            # Barkod üçün
            if fiscal_id:
                barcode = code128.Code128(fiscal_id, barHeight=20*mm, barWidth=0.5)
                barcode_x = 50
                barcode_y = 50
                barcode.drawOn(c, barcode_x, barcode_y)
                c.setFont("Arial", 8)
                c.drawString(barcode_x, barcode_y - 10, f"Fiskal ID: {fiscal_id}")

            c.save()
            QMessageBox.information(self, "PDF yaradıldı", f"Çek PDF olaraq saxlanıldı:\n{pdf_path}")








     

        def verify_and_delete(self):
            selected_row = self.ui.table.currentRow()
            if selected_row == -1:
                QMessageBox.warning(self, "Seçim yoxdur",
                                    "Silmək üçün bir sətir seçin.")
                return

            password, ok = QInputDialog.getText(
                self, "Təsdiqləmə", "Admin şifrəsini daxil edin:", QLineEdit.Password)
            if not ok or not password.strip():
                return

            if self.get_admin_verification(password.strip()):
                # Silinən sətrin ümumi məbləğini tapırıq (5-ci sütun - indeks 4)
                item = self.ui.table.item(selected_row, 4)
                if item:
                    try:
                        silinen_cem = float(item.text())
                    except ValueError:
                        silinen_cem = 0.0
                else:
                    silinen_cem = 0.0

                # Satırı sil
                self.ui.table.removeRow(selected_row)

                # Yenidən ümumi cəmi hesablaya bilərik, amma daha səmərəli:
                # Mövcud cəmi label-dan götürüb çıxırıq
                label_text = self.ui.labelTotal.text()  # məsələn: "Ümumi məbləğ: 123.45"
                try:
                    mebleg = float(label_text.split(":")[1].strip())
                except (IndexError, ValueError):
                    mebleg = 0.0

                yeni_cem = mebleg - silinen_cem
                self.ui.labelTotal.setText(f"Ümumi məbləğ: {yeni_cem:.2f}")

                QMessageBox.information(self, "Uğur", "Sətir silindi.")
            else:
                QMessageBox.warning(
                    self, "Yanlış", "Şifrə düzgün deyil və ya icazəniz yoxdur.")

                def get_admin_verification(self, input_password):
                    try:
                        conn = mysql.connector.connect(
                            host="localhost",
                            user="root",
                            password="123456",
                            database="mpd"
                        )
                        cursor = conn.cursor(dictionary=True)

                        cursor.execute("""
                                SELECT u.password_hash 
                                FROM users u
                                JOIN roles r ON u.role_id = r.id
                                WHERE r.role_name IN ('admin', 'superadmin')
                            """)

                        results = cursor.fetchall()
                        cursor.close()
                        conn.close()

                        for user in results:
                            if bcrypt.checkpw(input_password.encode('utf-8'), user["password_hash"].encode('utf-8')):
                                return True
                        return False
                    except Exception as e:
                        QMessageBox.critical(self, "DB xətası", str(e))
                        return False

        def get_admin_verification(self, input_password):
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="123456",
                    database="mpd"
                )
                cursor = conn.cursor(dictionary=True)

                cursor.execute("""
                        SELECT u.password_hash 
                        FROM users u
                        JOIN roles r ON u.role_id = r.id
                        WHERE r.role_name IN ('admin', 'superadmin')
                    """)

                results = cursor.fetchall()
                cursor.close()
                conn.close()

                for user in results:
                    if bcrypt.checkpw(input_password.encode('utf-8'), user["password_hash"].encode('utf-8')):
                        return True
                return False
            except Exception as e:
                QMessageBox.critical(self, "DB xətası", str(e))
                return False


if __name__ == '__main__':
    appl = QApplication(sys.argv)
    win = mywindow()
    win.show()
    sys.exit(appl.exec())
