# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_DialogWithButtonsBottom.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog2(object):
    def setupUi(self, Dialog2):
        Dialog2.setObjectName("Dialog2")
        Dialog2.resize(512, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog2)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.pushButton = QtWidgets.QPushButton(Dialog2)
        self.pushButton.setGeometry(QtCore.QRect(70, 60, 371, 46))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog2)
        self.buttonBox.accepted.connect(Dialog2.accept)
        self.buttonBox.rejected.connect(Dialog2.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog2)

    def retranslateUi(self, Dialog2):
        _translate = QtCore.QCoreApplication.translate
        Dialog2.setWindowTitle(_translate("Dialog2", "Dialog"))
        self.pushButton.setText(_translate("Dialog2", "test_DialogWithButtonsBottom"))

