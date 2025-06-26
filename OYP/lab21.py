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
import mysql.connector as mariadb
import ctypes
import datetime
pr = 'mainn.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.mywindow = QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.calendarWidget.hide()
        self.ui.PB.clicked.connect(self.A)
        self.ui.PB1.clicked.connect(self.add)
        self.ui.PDF.clicked.connect(self.Pdf)
        #self.ui.delete2.clicked.connect(self.delete)
        self.ui.SUM.clicked.connect(self.toplama)
        self.ui.calendarWidget.clicked.connect(self.B)
        self.ui.tableWidget.setColumnWidth(2, 270)
        self.ui.tableWidget.setColumnWidth(5, 161)
        self.ui.pushButton_4.clicked.connect(self.excel)


    def add(self):
        from subprocess import call
        call(["python", "create.py"])
    
    def toplama(self):
         a=self.ui.tableWidget.rowCount()    # Setirlerin sayi
         cem1=cem2=cem3=0
         for k in range(a):
              item=self.ui.tableWidget.item(k,5)
              try:           meb=float(item.text())
              except:    meb=0

              item=self.ui.tableWidget.item(k,6)
              try:           edv=float(item.text())
              except:    edv=0

              item=self.ui.tableWidget.item(k,7)
              try:           umumi=float(item.text())
              except:    umumi=0 

              cem1=cem1+meb
              cem2=cem2+edv
              cem3=cem3+umumi
         self.ui.SUMLE1.setText(str(round(cem1,2)))
         self.ui.SUMLE2.setText(str(round(cem2,2)))
         self.ui.SUMLE3.setText(str(round(cem3,2)))

         
                    
    def Pdf(self):
        import fpdf
        import os
        ws=('ID','Kod  ','Malin adi ',' Qiymet ','Miqdar',' Mebleg   ','EDV ',' CEMI ','Tarix')
        from fpdf import FPDF
        spacing=1
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.set_font("Arial", size=9)
        pdf.add_page()
        col_width = pdf.w / 15
        row_height = pdf.font_size
        a=self.ui.tableWidget.rowCount()
        columns=self.ui.tableWidget.columnCount()
       
        for i in range(9):
                item=ws[i]
                pdf.cell(col_width, row_height*spacing,txt=item, border=1)
        pdf.ln(row_height*spacing)
    
        for k in range(a):
            for i in range(9):
                item=self.ui.tableWidget.item(k, i)
                try: 
                         item=item.text()
                except:
                         item=' '
                pdf.cell(col_width, row_height*spacing,txt=item, border=1)
            pdf.ln(row_height*spacing)
        file = "C:\\Users\\ACER\\Desktop\\OYP\\Satis.pdf"
        print(2)
        pdf.output(file)
        print(3)
        ctypes.windll.user32.MessageBoxW(0,"Netice Satis adli PDF faylinda saxlanildi", "Diqqat !",0)
        os.startfile(file)
        
    def A(self):
        self.ui.calendarWidget.show()

    def B(self):
        self.ui.calendarWidget.hide()
        m = self.ui.calendarWidget.selectedDate().month()
        y = self.ui.calendarWidget.selectedDate().year()
        d = self.ui.calendarWidget.selectedDate().day()
        dat = datetime.date(y, m, d)
        connection = mariadb.connect(
            host='localhost', user='root', password='123456', db='mpd')
        cursor = connection.cursor()
        sql0 = "Select count(*) from table1 where tarix=%s"
        inputdata = (dat,)
        cursor.execute(sql0, inputdata)
        data = cursor.fetchone()
        say = int(data[0])
        print(data)
        if say != 0:
            sql1 = 'Select * from table1 where tarix=%s'
            inputdata = (dat,)
            cursor.execute(sql1, inputdata)
            data = cursor.fetchall()
            connection.close()
            cursor.close()
            self.ui.LCD1.display(d)
            self.ui.LCD2.display(m)
            self.ui.LCD3.display(y)
            a = len(data)
            b = len(data[0])
            self.ui.tableWidget.setRowCount(a)
            for i in range(a):
                for j in range(b):
                    if j == 1:
                        item = QTableWidgetItem(data[i][j])
                    else:
                        item = QTableWidgetItem(str(data[i][j]))
                    self.ui.tableWidget.setItem(i, j, item)
            self.ui.tableWidget.update()
        else:
            ctypes.windll.user32.MessageBoxW(
                0, "Bu tarixde satish olmayib", "Diqqat !", 16)


    def excel(self):
        import os
        import xlwt
        import getpass
        usr = getpass.getuser()

        font0 = xlwt.Font()
        font0.name = 'Arial'
        font0.size = 12
        font0.colour_index = 2
        font0.bold = True

        style0 = xlwt.XFStyle()
        style0.font = font0

        wb = xlwt.Workbook()
        ws = wb.add_sheet('Market')

        headers = ['ID', 'Barkod', 'Malın adı', 'Qiyməti',
                   'Miqdarı', 'Məbləği', 'Ədv', 'Ümumi Məbləğ', 'Tarix']

        for col_num, header in enumerate(headers, 1):
            ws.write(1, col_num, header, style0)

        rows = self.ui.tableWidget.rowCount()
        columns = self.ui.tableWidget.columnCount()

        for i in range(rows):
            for j in range(columns):
                item = self.ui.tableWidget.item(i, j)
                if item is not None:
                    item_text = item.text()
                    try:
                        item_value = float(item_text)
                        ws.write(i + 2, j + 1, item_value)
                    except ValueError:
                        ws.write(i + 2, j + 1, item_text)

        file_path = "C:\\Users\\ACER\\Desktop\\OYP\\Satis.xls"
        wb.save(file_path)

        ctypes.windll.user32.MessageBoxW(
            0, "Netice Satis adlı Excel faylında saxlanıldı", "Diqqət!", 0)
        os.startfile(file_path)

   

if __name__ == '__main__':
    appl = QApplication(sys.argv)
win = mywindow()
win.show()
sys.exit(appl.exec())
