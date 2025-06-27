import sys
import json
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget
from subprocess import Popen
import mysql.connector
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QApplication, QTableWidgetItem)
from decimal import Decimal
from PyQt5.QtGui import QColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QColor
from datetime import datetime



pr = 'refund.ui'  
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)

class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            self.mywindow = QWidget()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.ui.table.setColumnCount(5)
            self.ui.send.clicked.connect(self.GetirGeriQaytarma)
            self.ui.refund.clicked.connect(self.GeriQaytar)
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



        def GeriQaytar(self):
            fiscal_id = self.ui.LE.text().strip()

            if not fiscal_id:
                QMessageBox.warning(self, "Xəta", "Fiskal ID daxil edilməyib.")
                return

            conn = mysql.connector.connect(
                user='root', password='123456', host='localhost', database='mpd')
            cursor = conn.cursor()

            try:
                # ➤ 1. fiscal_id-dən sale_id-ni tap
                cursor.execute("SELECT id FROM sales WHERE fiscal_id = %s", (fiscal_id,))
                sale_result = cursor.fetchone()
                if not sale_result:
                    QMessageBox.warning(self, "Xəta", "Satış tapılmadı.")
                    return

                sale_id = sale_result[0]

                # ➤ 2. Seçilmiş satırları dövr et
                selected_rows = self.ui.table.selectionModel().selectedRows()
                if not selected_rows:
                    QMessageBox.information(self, "Diqqət", "Zəhmət olmasa geri qaytarmaq üçün məhsul(lar) seçin.")
                    return

                for selected in selected_rows:
                    row = selected.row()

                    ad = self.ui.table.item(row, 1).text()
                    say = Decimal(self.ui.table.item(row, 2).text())

                    # ➤ 3. table1-də bu məhsulun Miqdari-sini artır
                    cursor.execute("SELECT Miqdari FROM table1 WHERE `Malin adi` = %s", (ad,))
                    movcud_result = cursor.fetchone()

                    if movcud_result:
                        movcud_say = movcud_result[0]  # Decimal
                        yeni_say = movcud_say + say

                        cursor.execute("UPDATE table1 SET Miqdari = %s WHERE `Malin adi` = %s", (yeni_say, ad))

                        # ➤ 4. sale_items-də is_refunded = TRUE et
                        cursor.execute("""
                            UPDATE sale_items
                            SET is_refunded = TRUE
                            WHERE sale_id = %s AND product_name = %s
                        """, (sale_id, ad))

                        # ➤ 5. Geri qaytarılan sətirləri qırmızı rənglə
                        for col in range(self.ui.table.columnCount()):
                            item = self.ui.table.item(row, col)
                            if item:
                                item.setBackground(QColor(255, 102, 102))  # Açıq qırmızı
                    else:
                        QMessageBox.warning(self, "Xəta", f"{ad} məhsulu table1-də tapılmadı.")

                conn.commit()
                QMessageBox.information(self, "Uğur", "Seçilmiş məhsullar uğurla geri qaytarıldı.")
                self.GeriQaytarPDFYaz()
                # ➤ 6. Ümumi məbləği yenidən hesablamaq
                umumi_cem = Decimal("0.00")
                for i in range(self.ui.table.rowCount()):
                    item = self.ui.table.item(i, 4)
                    if item:
                        try:
                            umumi_cem += Decimal(item.text())
                        except:
                            pass  # əgər cəm boşdursa

                self.ui.labelTotal.setText(f"Ümumi məbləğ: {umumi_cem:.2f}")

            except Exception as e:
                conn.rollback()
                QMessageBox.critical(self, "Xəta", f"Geri qaytarma zamanı xəta baş verdi:\n{str(e)}")

            finally:
                cursor.close()
                conn.close()




        def GeriQaytarPDFYaz(self):
                pdfmetrics.registerFont(
                    TTFont('Arial', 'C:\\Windows\\Fonts\\arial.ttf'))
                
                tarix = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                downloads = os.path.join(os.path.expanduser("~"), "Downloads")
                if not os.path.exists(downloads):
                    os.makedirs(downloads)
                pdf_path = os.path.join(downloads, f"qaytarma_cek_{tarix}.pdf")

                c = canvas.Canvas(pdf_path, pagesize=A4)
                width, height = A4

                # Loqo (əgər varsa)
                logo_path = "C:\\Users\\ACER\\Desktop\\logo\\loqomain.png"
                if os.path.exists(logo_path):
                    logo = ImageReader(logo_path)
                    c.drawImage(logo, 50, height - 80, width=80, height=50, mask='auto')

                # Başlıq
                c.setFont("Arial", 14)
                c.drawString(200, height - 50, "QAYTARMA ÇEKİ")

                # Başlıq sütunlar
                c.setFont("Arial", 10)
                y = height - 100
                c.drawString(50, y, "Məhsul")
                c.drawString(200, y, "Say")
                c.drawString(260, y, "Qiymət")
                c.drawString(330, y, "Məbləğ")
                y -= 20

                umumi_qaytarilan = 0.0

                for row in range(self.ui.table.rowCount()):
                    # Sadəcə qırmızı arxa fona malik sətirləri seç
                    item_reng = self.ui.table.item(row, 0).background().color()
                    is_qaytarilib = (item_reng == QColor(255, 102, 102))

                    if is_qaytarilib:
                        ad = self.ui.table.item(row, 1).text()
                        say = int(self.ui.table.item(row, 2).text())
                        qiymet = float(self.ui.table.item(row, 3).text())
                        mebleg = say * qiymet
                        umumi_qaytarilan += mebleg

                        c.drawString(50, y, ad)
                        c.drawString(200, y, str(say))
                        c.drawString(260, y, f"{qiymet:.2f}")
                        c.drawString(330, y, f"{mebleg:.2f}")
                        y -= 20

                        if y < 50:
                            c.showPage()
                            y = height - 100
                            c.setFont("Arial", 10)

                c.setFont("Arial", 12)
                c.drawString(50, y - 20, f"CƏMİ QAYTARILAN MƏBLƏĞ: {umumi_qaytarilan:.2f} AZN")
                c.save()

                QMessageBox.information(self, "PDF yaradıldı",
                                        f"Qaytarma çeki PDF olaraq saxlanıldı:\n{pdf_path}")




        def GetirGeriQaytarma(self):
            fiscal_id = self.ui.LE.text().strip()

            if not fiscal_id:
                QMessageBox.warning(self, "Xəta", "Zəhmət olmasa fiskal ID daxil edin.")
                return

            conn = mysql.connector.connect(
                user='root', password='123456', host='localhost', database='mpd')
            cursor = conn.cursor()

            try:
                # ➤ 1. fiscal_id varsa, sale_id-ni tap
                cursor.execute("SELECT id FROM sales WHERE fiscal_id = %s", (fiscal_id,))
                result = cursor.fetchone()

                if not result:
                    QMessageBox.warning(self, "Xəta", "Belə bir fiskal ID tapılmadı.")
                    return

                sale_id = result[0]

                # ➤ 2. Əlaqəli sale_items məlumatlarını al
                cursor.execute("""
                    SELECT product_name, quantity, unit_price
                    FROM sale_items
                    WHERE sale_id = %s AND is_refunded = FALSE
                """, (sale_id,))
                items = cursor.fetchall()

                if not items:
                    QMessageBox.information(self, "Məlumat", "Bu satış artıq tam geri qaytarılıb və ya boşdur.")
                    return

                # ➤ 3. Table-i təmizlə
                self.ui.table.setRowCount(0)

                # ➤ 4. Yeni məlumatları table-a doldur
                for idx, (ad, say, qiymet) in enumerate(items):
                    cem = say * qiymet
                    self.ui.table.insertRow(idx)
                    self.ui.table.setItem(idx, 0, QTableWidgetItem(str(idx + 1)))      # sıra
                    self.ui.table.setItem(idx, 1, QTableWidgetItem(ad))                # məhsul adı
                    self.ui.table.setItem(idx, 2, QTableWidgetItem(str(say)))          # say
                    self.ui.table.setItem(idx, 3, QTableWidgetItem(f"{qiymet:.2f}"))   # qiymət
                    self.ui.table.setItem(idx, 4, QTableWidgetItem(f"{cem:.2f}"))      # cəm

                # ➤ 5. Ümumi cəmi yenilə
                umumi_cem = sum(q * p for (_, q, p) in items)
                self.ui.labelTotal.setText(f"Ümumi məbləğ: {umumi_cem:.2f}")

            except Exception as e:
                QMessageBox.critical(self, "Xəta", f"Xəta baş verdi:\n{str(e)}")

            finally:
                cursor.close()
                conn.close()
    










if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
