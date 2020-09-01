import sys, os, io

import qrcode

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit

class MainWindow(QtWidgets.QWidget):
    def __init__(self, textInputObjName = "textInput", qrObjName = "QRImage", errCorrectionSliderObjName = "errCorrectionSlider", errCorrectionStateObjName = "errCorrectionLabel", boxSizeSliderObjName = "boxSizeSlider", boxSizeStateObjName = "boxSizeLabel", borderSizeSliderObjName = "borderSizeSlider", borderSizeStateObjName = "borderSizeState"):
        super().__init__()

        self.setWindowTitle('QR code generator')

        self.resize(320, 380)
        self.setMinimumSize(QtCore.QSize(320, 380))

        self.textInputObjName = textInputObjName
        self.qrObjName = qrObjName
        self.errCorrectionSliderObjName = errCorrectionSliderObjName
        self.errCorrectionStateObjName = errCorrectionStateObjName
        self.boxSizeSliderObjName = boxSizeSliderObjName
        self.boxSizeStateObjName = boxSizeStateObjName
        self.borderSizeSliderObjName = borderSizeSliderObjName
        self.borderSizeStateObjName = borderSizeStateObjName

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
        qrErrCorrectionSlider.setSliderPosition(1)
        qrErrCorrectionSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        qrErrCorrectionSlider.setTickInterval(1)
        qrErrCorrectionSlider.valueChanged.connect(self.updateSettings)
        qrErrCorrectionSlider.setObjectName(self.errCorrectionSliderObjName)

        qrErrCorrectionStateLabel = QtWidgets.QLabel()
        qrErrCorrectionStateLabel.setObjectName(self.errCorrectionStateObjName)

        qrErrCorrectionLabel = QtWidgets.QLabel("Error correction level")


        boxSizeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        boxSizeSlider.setRange(2, 50)
        boxSizeSlider.setSingleStep(5)
        boxSizeSlider.setPageStep(10)
        boxSizeSlider.setSliderPosition(10)
        boxSizeSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        boxSizeSlider.setTickInterval(5)
        boxSizeSlider.valueChanged.connect(self.updateSettings)
        boxSizeSlider.setObjectName(self.boxSizeSliderObjName)

        boxSizeStateLabel = QtWidgets.QLabel()
        boxSizeStateLabel.setObjectName(self.boxSizeStateObjName)

        boxSizeLabel = QtWidgets.QLabel("Image resolution")


        borderSizeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        borderSizeSlider.setRange(0, 8)
        borderSizeSlider.setSingleStep(2)
        borderSizeSlider.setPageStep(4)
        borderSizeSlider.setSliderPosition(4)
        borderSizeSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        borderSizeSlider.setTickInterval(4)
        borderSizeSlider.valueChanged.connect(self.updateSettings)
        borderSizeSlider.setObjectName(self.borderSizeSliderObjName)

        borderSizeStateLabel = QtWidgets.QLabel()
        borderSizeStateLabel.setObjectName(self.borderSizeStateObjName)

        borderSizeLabel = QtWidgets.QLabel("Border size")

        column = 0
        grid.addWidget(qrTextInput, column, 0, 1, -1)
        column += 1
        grid.addWidget(qrErrCorrectionLabel, column, 0, 1, 2)
        grid.addWidget(qrErrCorrectionSlider, column, 3)
        grid.addWidget(qrErrCorrectionStateLabel, column, 4)
        column += 1
        grid.addWidget(boxSizeLabel, column, 0, 1, 2)
        grid.addWidget(boxSizeSlider, column, 3)
        grid.addWidget(boxSizeStateLabel, column, 4)
        column += 1
        grid.addWidget(borderSizeLabel, column, 0, 1, 2)
        grid.addWidget(borderSizeSlider, column, 3)
        grid.addWidget(borderSizeStateLabel, column, 4)
        column += 1
        grid.addWidget(qrImage, column, 0, 4, -1)

        self.setLayout(grid)
        self.show()

        self.updateSettings()

    def getErrorCorrection(self, value, type = "number"):
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
            }.get(self.getErrorCorrection(value), "M")

    def updateSettings(self, *args, **kwargs):
        self.findChildren(QtWidgets.QLabel, self.errCorrectionStateObjName)[0].setText(self.getErrorCorrection(self.findChildren(QtWidgets.QSlider, self.errCorrectionSliderObjName)[0].sliderPosition(), type = "char"))
        self.findChildren(QtWidgets.QLabel, self.boxSizeStateObjName)[0].setText(str(self.findChildren(QtWidgets.QSlider, self.boxSizeSliderObjName)[0].sliderPosition()))
        self.findChildren(QtWidgets.QLabel, self.borderSizeStateObjName)[0].setText(str(self.findChildren(QtWidgets.QSlider, self.borderSizeSliderObjName)[0].sliderPosition()))
        self.generateQR()

    def generateQR(self, text = ""):
        if text == "":
            text = self.findChildren(QtWidgets.QLineEdit, self.textInputObjName)[0].text()

        errCorrection = self.getErrorCorrection(self.findChildren(QtWidgets.QSlider, self.errCorrectionSliderObjName)[0].sliderPosition())
        boxSize = self.findChildren(QtWidgets.QSlider, self.boxSizeSliderObjName)[0].sliderPosition()
        borderSize = self.findChildren(QtWidgets.QSlider, self.borderSizeSliderObjName)[0].sliderPosition()
        with io.BytesIO() as f:
            im = qrcode.make(text, error_correction=errCorrection, box_size=boxSize, border=borderSize).save(f, format="png")
            f.seek(0)
            img = f.read()
            img = QtGui.QPixmap.fromImage(QtGui.QImage.fromData(img))
        label = self.findChildren(QtWidgets.QLabel, self.qrObjName)[0]
        label.setPixmap(img)

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()

app.exec_()