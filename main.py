import sys
from math import sin, asin, cos, pi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QColorDialog
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt


# K - коэффициент поворота, 0 <= k <= 1
# N - количество углов
# M - количество многоугольников


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(485, 408)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 55, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 20, 55, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(250, 20, 55, 16))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 20, 51, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 20, 51, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(280, 20, 51, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(370, 20, 93, 28))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 485, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Не квадрат-объектив"))
        self.label.setText(_translate("MainWindow", "K = "))
        self.label_2.setText(_translate("MainWindow", "N = "))
        self.label_3.setText(_translate("MainWindow", "M = "))
        self.pushButton.setText(_translate("MainWindow", "Рисовать"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.pushButton.clicked.connect(self.press)
        self.lineEdit.textEdited.connect(self.action)
        self.lineEdit_2.textEdited.connect(self.action)
        self.lineEdit_3.textEdited.connect(self.action)

        self.color = Qt.black
        self.draw_start = False
        self.x_c = self.width() // 2
        self.x_y = self.height() // 2
        self.r = 150

    def paintEvent(self, e):
        super().paintEvent(e)
        if not self.draw_start:
            return
        qp = QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):
        try:
            m = int(self.lineEdit_3.text())
            k = float(self.lineEdit.text())
            fi = 0
            r = self.r
            for _ in range(m):
                points = []
                n = int(self.lineEdit_2.text())
                for i in range(0, n):
                    x = self.x_c + r * cos(fi + 2 * pi * i / n)
                    y = self.x_y + r * sin(fi + 2 * pi * i / n)
                    points.append((x, y))
                side = 2 * r * sin(pi / n)
                n_side = side * (1 - k)
                alp = ((180 - (360 / n)) / 2) * pi / 180
                r = (r ** 2 + n_side ** 2 - 2 * r * n_side * cos(alp)) ** 0.5
                fi += asin((n_side * sin(alp)) / r)

                pen = QPen(self.color, 1, Qt.SolidLine)
                qp.setPen(pen)
                for i in range(0, len(points) - 1):
                    qp.drawLine(*points[i], *points[i + 1])
                qp.drawLine(*points[-1], *points[0])
        except ValueError:
            return

    def press(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color
        self.draw_start = True
        self.update()

    def action(self):
        self.draw_start = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
