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

pr = 'kassa.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(pr)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.mywindow = QWidget()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.PB1.clicked.connect(self.manat)
        self.ui.PB2.clicked.connect(self.qepik)
        self.ui.PB3.clicked.connect(self.hesabla)
        self.ui.PB300.clicked.connect(self.close)

    def manat(self):
        a = float(self.ui.LE1.text())
        b = float(self.ui.LE2.text())
        c = float(self.ui.LE3.text())
        d = float(self.ui.LE4.text())
        e = float(self.ui.LE5.text())
        f = float(self.ui.LE6.text())
        g = float(self.ui.LE7.text())     
        h = float(self.ui.LE8.text())     
        x = a*1
        self.ui.L1.setText(str(x))
        y = b*5
        self.ui.L2.setText(str(y))
        z = c*10
        self.ui.L3.setText(str(z))
        m = d*20
        self.ui.L4.setText(str(m))
        n = e*50
        self.ui.L5.setText(str(n))
        q = f*100
        self.ui.L6.setText(str(q))
        t = g*200
        self.ui.L7.setText(str(t))
        s = h*500
        self.ui.L8.setText(str(s))
        j = x+y+z+m+n+q+t+s
        self.ui.L100.setText(str(j))

    def qepik(self):
        aa = float(self.ui.LE9.text())
        bb = float(self.ui.LE10.text())
        cc = float(self.ui.LE11.text())
        dd = float(self.ui.LE12.text())
        ee = float(self.ui.LE13.text())
        ff = float(self.ui.LE14.text())
        xx = aa*0.01
        self.ui.L9.setText(str(xx))
        yy = bb*0.03
        self.ui.L10.setText(str(yy))
        zz = cc*0.05
        self.ui.L11.setText(str(zz))
        mm = dd*0.1
        self.ui.L12.setText(str(mm))
        nn = ee*0.2
        self.ui.L13.setText(str(nn))
        qq = ff*0.5
        self.ui.L14.setText(str(qq))

        jj = xx+yy+zz+mm+nn+qq
        self.ui.L200.setText(str(jj))

    def hesabla(self):
        aaa = float(self.ui.LE15.text())
        bbb = float(self.ui.LE16.text())
        ccc = float(self.ui.LE17.text())
        ddd = float(self.ui.LE18.text())
        eee = float(self.ui.LE19.text())
        a = float(self.ui.LE1.text())
        b = float(self.ui.LE2.text())
        c = float(self.ui.LE3.text())
        d = float(self.ui.LE4.text())
        e = float(self.ui.LE5.text())
        f = float(self.ui.LE6.text())
        g = float(self.ui.LE7.text())
        h = float(self.ui.LE8.text())
        aa = float(self.ui.LE9.text())
        bb = float(self.ui.LE10.text())
        cc = float(self.ui.LE11.text())
        dd = float(self.ui.LE12.text())
        ee = float(self.ui.LE13.text())
        ff = float(self.ui.LE14.text())
        hhh = eee-aaa-bbb-ccc-ddd-float(a)-float(b)*5-float(c)*10-float(d)*20-float(e)*50-float(f)*100-float(g)*200-float(h)*500-float(aa)*0.01-float(bb)*0.03-float(cc)*0.05-float(dd)*0.1-float(ee)*0.2-float(ff)*0.5
        abcd=round(hhh,2)
        self.ui.L800.setText(str(abcd))


if __name__ == '__main__':
    appl = QApplication(sys.argv)
win = mywindow()
win.show()
sys.exit(appl.exec())
