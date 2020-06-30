# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PlotGui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(866, 870)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 821, 121))
        self.pushButton.setObjectName("pushButton")
        self.widget = matplotlibWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(40, 170, 791, 661))
        self.widget.setObjectName("widget")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Push to Plot"))

from test.matplotlibWidgetFile import matplotlibWidget
