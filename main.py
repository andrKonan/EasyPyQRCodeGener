import sys, os, io

import qrcode

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit

class windowSize():
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def getQSize(self):
        return QtCore.QSize(self.x, self.y)

def makeSlider(orientation = "h", range = (0, 100), singleStep = 1, pageStep = 5, sliderPosition = 0, tickPosition = -1, tickInterval = -1):
    if isinstance(orientation, str):
        orientation = orientation.lower()
    if orientation in ["h", "horizontal", "-"]:
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    elif orientation in ["v", "vertical", "|"]:
        slider = QtWidgets.QSlider(QtCore.Qt.Vertical)
    elif not orientation == QtCore.Qt.Horizontal or QtCore.Qt.Vertical:
        return -1
    slider.setRange(range[0], range[1])
    slider.setSingleStep(singleStep)
    slider.setPageStep(pageStep)
    slider.setSliderPosition(sliderPosition)
    if QtWidgets.QSlider.NoTicks <= tickPosition <= QtWidgets.QSlider.TicksBothSides:
        slider.setTickPosition(tickPosition)
    if tickInterval > 0:
        slider.setTickInterval(tickInterval)
    return slider

class MainWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()

        self.setWindowTitle('QR code generator')
        self.minSize = windowSize(320, 440)
        self.resize(self.minSize.x, self.minSize.y)
        self.setMinimumSize(self.minSize.getQSize())

        try:
            kwargs.get("")
        except AttributeError:
            sys.exit(-1)

        self.textInputObjName = kwargs.get("textInputObjName", "textInput")
        self.qrObjName = kwargs.get("qrObjName", "QRImage")
        self.errCorrectionSliderObjName = kwargs.get("errCorrectionSliderObjName", "errCorrectionSlider")
        self.errCorrectionStateObjName = kwargs.get("errCorrectionStateObjName", "errCorrectionLabel")
        self.boxSizeSliderObjName = kwargs.get("boxSizeSliderObjName", "boxSizeSlider")
        self.boxSizeStateObjName = kwargs.get("boxSizeStateObjName", "boxSizeLabel")
        self.borderSizeSliderObjName = kwargs.get("borderSizeSliderObjName", "borderSizeSlider")
        self.borderSizeStateObjName = kwargs.get("borderSizeStateObjName", "borderSizeState")

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

        qrErrCorrectionSlider = makeSlider(orientation = "h", range = (0, 3), sliderPosition = 1, tickPosition = QtWidgets.QSlider.TicksBothSides, tickInterval = 1)
        qrErrCorrectionSlider.valueChanged.connect(self.updateSettings)
        qrErrCorrectionSlider.setObjectName(self.errCorrectionSliderObjName)

        qrErrCorrectionStateLabel = QtWidgets.QLabel()
        qrErrCorrectionStateLabel.setObjectName(self.errCorrectionStateObjName)

        qrErrCorrectionLabel = QtWidgets.QLabel("Error correction level")


        boxSizeSlider = makeSlider(orientation = "h", range = (1, 50), singleStep = 5, pageStep = 15, sliderPosition = 10, tickPosition = QtWidgets.QSlider.TicksBothSides, tickInterval = 5)
        boxSizeSlider.valueChanged.connect(self.updateSettings)
        boxSizeSlider.setObjectName(self.boxSizeSliderObjName)

        boxSizeStateLabel = QtWidgets.QLabel()
        boxSizeStateLabel.setObjectName(self.boxSizeStateObjName)

        boxSizeLabel = QtWidgets.QLabel("Image resolution")


        self.borderSizeStateMultiplier = 2

        borderSizeSlider = makeSlider(orientation = "h", range = (0, 4), singleStep = 2 // self.borderSizeStateMultiplier, pageStep = 2 // self.borderSizeStateMultiplier, sliderPosition = 4 // self.borderSizeStateMultiplier, tickPosition = QtWidgets.QSlider.TicksBothSides, tickInterval = 2 // self.borderSizeStateMultiplier)
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
        self.findChildren(QtWidgets.QLabel, self.borderSizeStateObjName)[0].setText(str(self.findChildren(QtWidgets.QSlider, self.borderSizeSliderObjName)[0].sliderPosition() * self.borderSizeStateMultiplier))
        self.generateQR()

    def generateQR(self, text = ""):
        if text == "":
            text = self.findChildren(QtWidgets.QLineEdit, self.textInputObjName)[0].text()

        errCorrection = self.getErrorCorrection(self.findChildren(QtWidgets.QSlider, self.errCorrectionSliderObjName)[0].sliderPosition())
        boxSize = self.findChildren(QtWidgets.QSlider, self.boxSizeSliderObjName)[0].sliderPosition()
        borderSize = self.findChildren(QtWidgets.QSlider, self.borderSizeSliderObjName)[0].sliderPosition() * self.borderSizeStateMultiplier
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