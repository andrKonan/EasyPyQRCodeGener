import sys, io

import qrcode

from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QIcon, QPixmap

from PIL import Image

class MainWindow(QWidget):
    def __init__(self, pathToImage = "qr.png"):
        super().__init__()

        self.setWindowTitle('QR code generator')

        self.resize(320, 240)
        self.setMinimumSize(QSize(320, 240))

        self.pathToImage = pathToImage
        self.initUI()

    def initUI(self):
        grid = QGridLayout(self)
        grid.setSpacing(5)

        qrTextInput = QLineEdit()
        qrTextInput.textChanged.connect(self.generateQR)
        qrImage = QLabel()
        qrImage.setPixmap(QPixmap(self.pathToImage))
        qrImage.setScaledContents(True)

        grid.addWidget(qrTextInput, 0, 0)
        grid.addWidget(qrImage, 1, 0)

        self.setLayout(grid)

        self.show()

    def generateQR(self, text):
        qrcode.make(text).save(self.pathToImage)

        label = self.findChildren(QLabel)[0]
        label.setPixmap(QPixmap(self.pathToImage))

app = QApplication(sys.argv)

window = MainWindow()

app.exec_()