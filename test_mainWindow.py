# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Projects\kiwoon36\test_mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow11(object):
    def setupUi(self, MainWindow11):
        MainWindow11.setObjectName("MainWindow11")
        MainWindow11.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow11)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMinimumSize(QtCore.QSize(0, 300))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        MainWindow11.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow11)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 38))
        self.menubar.setObjectName("menubar")
        MainWindow11.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow11)
        self.statusbar.setObjectName("statusbar")
        MainWindow11.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow11)
        # self.pushButton_2.clicked.connect(MainWindow11.kdjSlot1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow11)

    def retranslateUi(self, MainWindow11):
        _translate = QtCore.QCoreApplication.translate
        MainWindow11.setWindowTitle(_translate("MainWindow11", "MainWindow"))
        self.label.setText(_translate("MainWindow11", "TextLabel"))
        self.pushButton_2.setText(_translate("MainWindow11", "PushButton"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow11 = QtWidgets.QMainWindow()
    ui = Ui_MainWindow11()
    ui.setupUi(MainWindow11)
    MainWindow11.show()
    sys.exit(app.exec_())

