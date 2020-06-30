# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_DialogWithButtonsRight.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog3(object):
    def setupUi(self, Dialog3):
        Dialog3.setObjectName("Dialog3")
        Dialog3.resize(602, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog3)
        self.buttonBox.setGeometry(QtCore.QRect(290, 20, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.pushButton = QtWidgets.QPushButton(Dialog3)
        self.pushButton.setGeometry(QtCore.QRect(20, 160, 351, 46))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog3)
        self.buttonBox.accepted.connect(Dialog3.accept)
        self.buttonBox.rejected.connect(Dialog3.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog3)

    def retranslateUi(self, Dialog3):
        _translate = QtCore.QCoreApplication.translate
        Dialog3.setWindowTitle(_translate("Dialog3", "Dialog"))
        self.pushButton.setText(_translate("Dialog3", "test_DialogWithButtonsRight"))

