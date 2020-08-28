import sys, os

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
        try:
            qrcode.make(text).save(self.pathToImage)

            label = self.findChildren(QtWidgets.QLabel)[0]
            label.setPixmap(QtGui.QPixmap(self.pathToImage))
        except OSError:
            self.permissionDenied()

    class errorPermissionDeniedMessage(QtWidgets.QWidget):
        def __init__(self, parent, pathToImage):
            super().__init__()

            self.pathToImage = pathToImage

            self.setWindowTitle('QR code generator: ERROR')
            self.setMinimumSize(QtCore.QSize(440, 100))

            self.initUI()

        def initUI(self):
            grid = QtWidgets.QGridLayout(self)
            grid.setSpacing(5)

            errorMessageLabel = QtWidgets.QLabel("Error: permissions denied. Can't write to file:\"" + self.pathToImage + "\"")
            errorMessageLabel.setAlignment(QtCore.Qt.AlignCenter)

            grid.addWidget(errorMessageLabel, 0, 0)

            self.show()

        def closeEvent(self, event):
            sys.exit(-1)

    def permissionDenied(self):
        self.errorMessage = self.errorPermissionDeniedMessage(self, self.pathToImage)
        self.errorMessage.show()

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()

app.exec_()