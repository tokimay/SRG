from PyQt6 import QtCore as PyQt6_QtCore
from PySide6 import QtCore as PySide6_QtCore
from PySide6 import QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 434)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(PySide6_QtCore.QRect(12, 10, 581, 381))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.pic_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.pic_label.setText("")
        self.pic_label.setObjectName("pic_label")
        self.gridLayout.addWidget(self.pic_label, 0, 0, 1, 1)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(PySide6_QtCore.QRect(10, 400, 581, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_start = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout.addWidget(self.pushButton_start)
        self.pushButton_stop = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.horizontalLayout.addWidget(self.pushButton_stop)
        self.pushButton_play = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_play.setObjectName("pushButton_play")
        self.horizontalLayout.addWidget(self.pushButton_play)

        self.retranslateUi(Dialog)
        PySide6_QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = PyQt6_QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_start.setText(_translate("Dialog", "Start"))
        self.pushButton_stop.setText(_translate("Dialog", "Stop"))
        self.pushButton_play.setText(_translate("Dialog", "Play"))
