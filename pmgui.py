# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pmg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_popupmsgform(object):
    def setupUi(self, popupmsgform):
        popupmsgform.setObjectName("popupmsgform")
        popupmsgform.resize(348, 96)
        self.horizontalLayout = QtWidgets.QHBoxLayout(popupmsgform)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(popupmsgform)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label.setStyleSheet("QLabel{color: #eee;}")
        self.horizontalLayout.addWidget(self.label)

        self.retranslateUi(popupmsgform)
        QtCore.QMetaObject.connectSlotsByName(popupmsgform)

    def retranslateUi(self, popupmsgform):
        _translate = QtCore.QCoreApplication.translate
        popupmsgform.setWindowTitle(_translate("popupmsgform", "Message"))
        self.label.setText(_translate("popupmsgform", "TextLabel"))

