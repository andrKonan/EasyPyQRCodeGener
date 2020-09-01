import sys, os, io

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

    def closeEvent(self, event):
        if not os.path.exists(self.pathToImage):
            try:
                os.remove(self.pathToImage)
            except OSError:
                self.generateQR("")

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
        with io.BytesIO() as f:
            im = qrcode.make(text)
            im.save(f, format='png')
            f.seek(0)
            img = f.read()
            img = QtGui.QPixmap.fromImage(QtGui.QImage.fromData(img))
        label = self.findChildren(QtWidgets.QLabel)[0]
        label.setPixmap(img)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()

app.exec_()