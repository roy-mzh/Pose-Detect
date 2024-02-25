import os
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class warning_UI(QDialog):
    def __init__(self):
        super(warning_UI, self).__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        # palette = QPalette()
        # palette.setBrush(QPalette.Background, QBrush(QPixmap("./bg.png")))
        # self.setPalette(palette)

        # self.setWindowOpacity(0.7)
        # self.showFullScreen()


    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        desktop = QApplication.desktop()
        brush = QBrush(Qt.SolidPattern)
        painter.setBrush(brush)
        painter.setBrush(QColor(255, 255, 255, 200))  # 给画家设置笔刷
        painter.drawRect(0, 0, desktop.width(), desktop.height())

        brush = QBrush(Qt.SolidPattern)
        painter.setBrush(brush)
        painter.setBrush(QColor(0, 0, 0, 255))  # 给画家设置笔刷
        painter.drawRoundedRect(desktop.width()/2-500, desktop.height()/2-300, 1000, 600, 60, 60)
        # painter.drawRect(desktop.width()/2-500, desktop.height()/2-300, 1000, 600)
        painter.end()



    def setupUi(self, sitting_warning):
        sitting_warning.setObjectName("sitting_warning")
        desktop = QApplication.desktop()
        sitting_warning.move(0, 0)
        sitting_warning.resize(desktop.width(), desktop.height())
        sitting_warning.setMinimumSize(QtCore.QSize(desktop.width(), desktop.height()))
        sitting_warning.setMaximumSize(QtCore.QSize(desktop.width(), desktop.height()))




        self.label = QtWidgets.QLabel(sitting_warning)

        self.label.setGeometry(QtCore.QRect(desktop.width() / 2 - 960/2, desktop.height() / 2 - 90/2-100, 960, 90))
        self.label.setStyleSheet("QLabel{\n"
                                 "    color:rgb(255,255,255);\n"
                                 "    font: 20pt \"微软雅黑\";\n"
                                 "    background-color:rgb(0, 0, 0, 0);\n"
                                 "}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")


        self.label_2 = QtWidgets.QLabel(sitting_warning)
        self.label_2.setGeometry(QtCore.QRect(desktop.width() / 2 - 960/2, desktop.height() / 2 - 90/2+100, 960, 90))
        self.label_2.setStyleSheet("QLabel{\n"
                                   "    color:rgb(255,255,255);\n"
                                   "    font: 20pt \"微软雅黑\";\n"
                                   "    background-color:rgb(0, 0, 0, 0);\n"
                                   "}")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(sitting_warning)
        QtCore.QMetaObject.connectSlotsByName(sitting_warning)

    def retranslateUi(self, sitting_warning):
        _translate = QtCore.QCoreApplication.translate
        sitting_warning.setWindowTitle(_translate("sitting_warning", "Form"))
        self.label.setText(_translate("sitting_warning", "Please adjust your sitting position"))
        self.label_2.setText(_translate("sitting_warning", "Currently in a locked screen"))


class Masker(QThread, QDialog):
    """
        Func:
            Using the 'mask' file to pass the signal, if the signal is True, we mask everything; otherwise, we take the mask away.
    """

    def __init__(self):
        super().__init__()

        self.mask = [1, 1]
        self.flag = True

        # Create the main window
        self.window = warning_UI()

        # self.window.setWindowOpacity(0.7)
        # self.window.setAttribute(Qt.WA_NoSystemBackground, True)
        self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.window.showFullScreen()
        self.window.showMinimized()


        # blur = QGraphicsBlurEffect()
        # blur.setBlurRadius(100)
        # blur.setBlurHints(QGraphicsBlurEffect.QualityHint)
        # self.window.setGraphicsEffect(blur)

    def blurry(self):
        if self.flag:
            if self.mask[0] and self.mask[0] != self.mask[1]:
                self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Stay over any other apps
                self.window.showMaximized()

                self.mask[1] = self.mask[0]

            elif ~self.mask[0] and self.mask[0] != self.mask[1]:
                self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.Widget)  # Stay under any other apps

                self.window.showMinimized()

                self.mask[1] = self.mask[0]

            if not os.path.exists("mask"):
                with open("mask", "w") as f:
                    f.write("F")

            with open("mask", "r") as f:
                tmp = f.read()
                if tmp == "T":
                    self.mask[0] = 1
                elif tmp == "F":
                    self.mask[0] = 0

    def kill_all(self):
        """
            Func:
                Deciding whether kill all the process
        """
        if self.flag:
            if not os.path.exists("flag"):
                with open("flag", "w") as f:
                    f.write("T")

            with open("flag", "r") as f:
                tmp = f.read()
                if tmp == "F":
                    self.flag = False
        else:
            sys.exit(0)

    def start(self):
        self.timer1 = QTimer(self)
        self.timer2 = QTimer(self)
        self.timer1.timeout.connect(self.blurry)
        self.timer2.timeout.connect(self.kill_all)
        self.timer1.start(100)
        self.timer2.start(100)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    m = Masker()
    m.start()
    sys.exit(app.exec_())
