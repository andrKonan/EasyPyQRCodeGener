import sys
import io

import qrcode

from PyQt5 import QtCore, QtGui, QtWidgets


class WindowSize():
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def get_qsize(self):
        return QtCore.QSize(self.x, self.y)


def make_slider(
        orientation="h", slider_range=(0, 100), single_step=1,
        page_step=5, slider_position=0, tick_position=-1, tick_interval=-1):
    tick_pos_minmax = {
        "nt": QtWidgets.QSlider.NoTicks,
        "tbs": QtWidgets.QSlider.TicksBothSides
    }
    if isinstance(orientation, str):
        orientation = orientation.lower()
    if orientation in ["h", "horizontal", "-"]:
        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    elif orientation in ["v", "vertical", "|"]:
        slider = QtWidgets.QSlider(QtCore.Qt.Vertical)
    elif not orientation == QtCore.Qt.Horizontal or QtCore.Qt.Vertical:
        return -1
    slider.setRange(slider_range[0], slider_range[1])
    slider.setSingleStep(single_step)
    slider.setPageStep(page_step)
    slider.setSliderPosition(slider_position)
    if tick_pos_minmax["nt"] <= tick_position <= tick_pos_minmax["tbs"]:
        slider.setTickPosition(tick_position)
    if tick_interval > 0:
        slider.setTickInterval(tick_interval)
    return slider


class MainWindow(QtWidgets.QWidget):
    def __init__(self, **kwargs):
        super().__init__()

        self.setWindowTitle('QR code generator')
        self.minimum_size = WindowSize(320, 440)
        self.resize(self.minimum_size.x, self.minimum_size.y)
        self.setMinimumSize(self.minimum_size.get_qsize())

        try:
            kwargs.get("")
        except AttributeError:
            sys.exit(-1)

        self.textInputObjName = kwargs.get(
            "textInputObjName", "textInput"
        )
        self.qrObjName = kwargs.get(
            "qrObjName", "QRImage"
        )

        self.errCorrectionSliderObjName = kwargs.get(
            "errCorrectionSliderObjName", "errCorrectionSlider"
        )

        self.errCorrectionStateObjName = kwargs.get(
            "errCorrectionStateObjName", "errCorrectionLabel"
        )

        self.boxSizeSliderObjName = kwargs.get(
            "boxSizeSliderObjName", "boxSizeSlider"
        )

        self.boxSizeStateObjName = kwargs.get(
            "boxSizeStateObjName", "boxSizeLabel"
        )

        self.borderSizeSliderObjName = kwargs.get(
            "borderSizeSliderObjName", "borderSizeSlider"
        )

        self.borderSizeStateObjName = kwargs.get(
            "borderSizeStateObjName", "borderSizeState"
        )

        self.init_ui()

    def init_ui(self):
        grid = QtWidgets.QGridLayout(self)
        grid.setSpacing(5)

        qr_text_input = QtWidgets.QLineEdit()
        qr_text_input.textChanged.connect(self.update_settings_and_qr)
        qr_text_input.setObjectName(self.textInputObjName)

        qr_image = QtWidgets.QLabel()
        qr_image.setScaledContents(True)
        qr_image.setObjectName(self.qrObjName)

        qr_error_correction_slider = make_slider(
            orientation="h",
            slider_range=(0, 3),
            slider_position=1,
            tick_position=QtWidgets.QSlider.TicksBothSides,
            tick_interval=1
        )
        qr_error_correction_slider.valueChanged.connect(
            self.update_settings_and_qr
        )
        qr_error_correction_slider.setObjectName(
            self.errCorrectionSliderObjName
        )

        qr_error_correction_state_label = QtWidgets.QLabel()
        qr_error_correction_state_label.setObjectName(
            self.errCorrectionStateObjName
        )

        qr_error_correction_level_label = QtWidgets.QLabel(
            "Error correction level"
        )

        box_size_slider = make_slider(
            orientation="h",
            slider_range=(1, 50),
            single_step=5,
            page_step=15,
            slider_position=10,
            tick_position=QtWidgets.QSlider.TicksBothSides,
            tick_interval=5
        )
        box_size_slider.valueChanged.connect(
            self.update_settings_and_qr
        )
        box_size_slider.setObjectName(
            self.boxSizeSliderObjName
        )

        box_size_state_label = QtWidgets.QLabel()
        box_size_state_label.setObjectName(
            self.boxSizeStateObjName
        )

        box_size_label = QtWidgets.QLabel(
            "Image resolution"
        )

        self.border_size_state_multiplier = 2

        border_size_slider = make_slider(
            orientation="h",
            slider_range=(0, 4),
            single_step=2 // self.border_size_state_multiplier,
            page_step=2 // self.border_size_state_multiplier,
            slider_position=4 // self.border_size_state_multiplier,
            tick_position=QtWidgets.QSlider.TicksBothSides,
            tick_interval=2 // self.border_size_state_multiplier
        )
        border_size_slider.valueChanged.connect(
            self.update_settings_and_qr
        )
        border_size_slider.setObjectName(
            self.borderSizeSliderObjName
        )

        border_size_state_label = QtWidgets.QLabel()
        border_size_state_label.setObjectName(
            self.borderSizeStateObjName
        )

        border_size_label = QtWidgets.QLabel(
            "Border size"
        )

        column = 0
        grid.addWidget(
            qr_text_input, column, 0, 1, -1
        )
        column += 1
        grid.addWidget(
            qr_error_correction_level_label, column, 0, 1, 2
        )
        grid.addWidget(
            qr_error_correction_slider, column, 3
        )
        grid.addWidget(
            qr_error_correction_state_label, column, 4
        )
        column += 1
        grid.addWidget(
            box_size_label, column, 0, 1, 2
        )
        grid.addWidget(
            box_size_slider, column, 3
        )
        grid.addWidget(
            box_size_state_label, column, 4
        )
        column += 1
        grid.addWidget(
            border_size_label, column, 0, 1, 2
        )
        grid.addWidget(
            border_size_slider, column, 3
        )
        grid.addWidget(
            border_size_state_label, column, 4
        )
        column += 1
        grid.addWidget(
            qr_image, column, 0, 4, -1
        )

        self.setLayout(grid)
        self.show()

        self.update_settings_and_qr()

    def get_error_correction_level(self, value, return_object="number"):
        if return_object == "number":
            return {
                0: qrcode.constants.ERROR_CORRECT_L,
                1: qrcode.constants.ERROR_CORRECT_M,
                2: qrcode.constants.ERROR_CORRECT_Q,
                3: qrcode.constants.ERROR_CORRECT_H
            }.get(value, qrcode.constants.ERROR_CORRECT_M)
        if return_object == "char":
            return {
                qrcode.constants.ERROR_CORRECT_L: "L",
                qrcode.constants.ERROR_CORRECT_M: "M",
                qrcode.constants.ERROR_CORRECT_Q: "Q",
                qrcode.constants.ERROR_CORRECT_H: "H"
            }.get(self.get_error_correction_level(value), "M")

    def update_settings_and_qr(self, *args, **kwargs):
        self.findChildren(
            QtWidgets.QLabel,
            self.errCorrectionStateObjName
        )[0].setText(
            self.get_error_correction_level(
                self.findChildren(
                    QtWidgets.QSlider,
                    self.errCorrectionSliderObjName
                )[0].sliderPosition(),
                return_object="char"
            )
        )

        self.findChildren(
            QtWidgets.QLabel,
            self.boxSizeStateObjName
        )[0].setText(
            str(
                self.findChildren(
                    QtWidgets.QSlider,
                    self.boxSizeSliderObjName
                )[0].sliderPosition()
            )
        )

        self.findChildren(
            QtWidgets.QLabel,
            self.borderSizeStateObjName
        )[0].setText(
            str(
                self.findChildren(
                    QtWidgets.QSlider,
                    self.borderSizeSliderObjName
                )[0].sliderPosition() * self.border_size_state_multiplier
            )
        )

        self.generate_qr()

    def generate_qr(self, text=""):
        if text == "":
            text = self.findChildren(
                QtWidgets.QLineEdit,
                self.textInputObjName
            )[0].text()

        error_correction_level = self.get_error_correction_level(
            self.findChildren(
                QtWidgets.QSlider,
                self.errCorrectionSliderObjName
            )[0].sliderPosition()
        )

        box_size = self.findChildren(
            QtWidgets.QSlider,
            self.boxSizeSliderObjName
        )[0].sliderPosition()

        border_size = self.findChildren(
            QtWidgets.QSlider,
            self.borderSizeSliderObjName
        )[0].sliderPosition() * self.border_size_state_multiplier
        with io.BytesIO() as virtual_file:
            qrcode.make(
                text,
                error_correction=error_correction_level,
                box_size=box_size,
                border=border_size
            ).save(
                virtual_file,
                format="png"
            )
            virtual_file.seek(0)
            img = virtual_file.read()
            img = QtGui.QPixmap.fromImage(QtGui.QImage.fromData(img))
        label = self.findChildren(QtWidgets.QLabel, self.qrObjName)[0]
        label.setPixmap(img)


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()

app.exec_()
