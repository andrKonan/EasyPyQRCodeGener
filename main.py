import sys

import qrcode

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit

class MainWindow(QtWidgets.QWidget):
    def __init__(self, pathToImage = "qr.png"):
        super().__init__()

        self.setWindowTitle('QR code generator')

        self.resize(320, 320)
        self.setMinimumSize(QtCore.QSize(320, 320))

        self.pathToImage = pathToImage
        self.initUI()

    def initUI(self):
        grid = QtWidgets.QGridLayout(self)
        grid.setSpacing(5)

        qrTextInput = QtWidgets.QLineEdit()
        qrTextInput.textChanged.connect(self.generateQR)
        qrImage = QtWidgets.QLabel()
        qrImage.setScaledContents(True)

        grid.addWidget(qrTextInput, 0, 0)
        grid.addWidget(qrImage, 1, 0)

        self.setLayout(grid)
        self.show()

        self.generateQR("")

    def generateQR(self, text):
        qrcode.make(text).save(self.pathToImage)

        label = self.findChildren(QtWidgets.QLabel)[0]
        label.setPixmap(QtGui.QPixmap(self.pathToImage))

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()

app.exec_()