import sys, os, io

import qrcode

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit

class MainWindow(QtWidgets.QWidget):
    def __init__(self, textInputObjName = "textInput", qrObjName = "QRImage", errCorrectionSliderObjName = "errCorrectionSlider", errCorrectionLabelObjName = "errCorrectionLabel"):
        super().__init__()

        self.setWindowTitle('QR code generator')

        self.resize(320, 320)
        self.setMinimumSize(QtCore.QSize(320, 320))

        self.textInputObjName = textInputObjName
        self.qrObjName = qrObjName
        self.errCorrectionSliderObjName = errCorrectionSliderObjName
        self.errCorrectionLabelObjName = errCorrectionLabelObjName

        self.initUI()

    def initUI(self):
        grid = QtWidgets.QGridLayout(self)
        grid.setSpacing(5)

        qrTextInput = QtWidgets.QLineEdit()
        qrTextInput.textChanged.connect(self.generateQR)
        qrTextInput.setObjectName(self.textInputObjName)

        qrImage = QtWidgets.QLabel()
        qrImage.setScaledContents(True)
        qrImage.setObjectName(self.qrObjName)

        qrErrCorrectionSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        qrErrCorrectionSlider.setRange(0, 3)
        qrErrCorrectionSlider.setPageStep(1)
        #qrErrCorrectionSlider.setValue(0)
        qrErrCorrectionSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        qrErrCorrectionSlider.setTickInterval(1)
        qrErrCorrectionSlider.sliderMoved.connect(self.updateSettings)
        qrErrCorrectionSlider.setObjectName(self.errCorrectionSliderObjName)

        qrErrCorrectionStateLabel = QtWidgets.QLabel()
        qrErrCorrectionStateLabel.setObjectName(self.errCorrectionLabelObjName)

        grid.addWidget(qrTextInput, 0, 0, 1, -1)
        grid.addWidget(qrErrCorrectionSlider, 1, 0)
        grid.addWidget(qrErrCorrectionStateLabel, 1, 1)
        grid.addWidget(qrImage, 2, 0, 2, 2)

        self.setLayout(grid)
        self.show()

        self.generateQR("")

    @staticmethod
    def getErrorCorrection(value, type = "number"):
        if type == "number":
            return {
                0: qrcode.constants.ERROR_CORRECT_L,
                1: qrcode.constants.ERROR_CORRECT_M,
                2: qrcode.constants.ERROR_CORRECT_Q,
                3: qrcode.constants.ERROR_CORRECT_H
            }.get(value, qrcode.constants.ERROR_CORRECT_M)
        if type == "char":
            return {
                qrcode.constants.ERROR_CORRECT_L: "L",
                qrcode.constants.ERROR_CORRECT_M: "M",
                qrcode.constants.ERROR_CORRECT_Q: "Q",
                qrcode.constants.ERROR_CORRECT_H: "H"
            }.get(value, "M")

    def updateSettings(self, *args, **kwargs):
        print(self.findChildren(QtWidgets.QSlider, self.errCorrectionSliderObjName)[0].value())
        self.findChildren(QtWidgets.QLabel, self.errCorrectionLabelObjName)[0].setText(self.getErrorCorrection(self.findChildren(QtWidgets.QSlider, self.errCorrectionSliderObjName)[0].value(), type = "char"))
        self.generateQR()

    def generateQR(self, text = ""):
        if text == "":
            text = self.findChildren(QtWidgets.QLineEdit, self.textInputObjName)[0].text()

        errCorrection = self.getErrorCorrection(self.findChildren(QtWidgets.QSlider, self.errCorrectionSliderObjName)[0].value())

        with io.BytesIO() as f:
            im = qrcode.make(text, error_correction=errCorrection).save(f, format="png")
            f.seek(0)
            img = f.read()
            img = QtGui.QPixmap.fromImage(QtGui.QImage.fromData(img))
        label = self.findChildren(QtWidgets.QLabel, self.qrObjName)[0]
        label.setPixmap(img)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()

app.exec_()