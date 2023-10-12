# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets
from mylabel import MyLabel


class Ui_MainForm(object):
    def setupUi(self, MainForm, lang):
        MainForm.setObjectName("MainForm")
        MainForm.resize(395, 346)
        MainForm.setMaximumSize(QtCore.QSize(500, 400))
        MainForm.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainForm)
        self.centralwidget.setObjectName("centralwidget")
        # self.centralwidget.setStyleSheet('QWidget#centralwidget {background: #222; font-color: #eee;}')
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        MainForm.setCentralWidget(self.centralwidget)

        self.lInfo = QtWidgets.QLabel(self.centralwidget)
        self.lInfo.setText("")
        self.lInfo.setMinimumSize(QtCore.QSize(0, 20))
        self.lInfo.setWordWrap(True)
        self.lInfo.setObjectName("lInfo")
        self.verticalLayout.addWidget(self.lInfo)

        self.ipwidget = QtWidgets.QWidget(self.centralwidget)
        self.ipwidget.setMinimumSize(QtCore.QSize(0, 30))
        self.ipwidget.setObjectName("ipwidget")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.ipwidget)
        self.horizontalLayout_2.setContentsMargins(0, 1, 0, 1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setSpacing(2)

        self.label2 = QtWidgets.QLabel(self.ipwidget)
        self.label2.setObjectName("label2")
        self.horizontalLayout_2.addWidget(self.label2)

        # self.eip = QtWidgets.QLineEdit(self.ipwidget)
        # self.eip.setObjectName("eip")
        self.cbIp = QtWidgets.QComboBox(self.ipwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbIp.sizePolicy().hasHeightForWidth())
        self.cbIp.setSizePolicy(sizePolicy)
        self.cbIp.setMaxVisibleItems(8)
        self.cbIp.setMaxCount(100)
        self.cbIp.setObjectName("cbIp")
        self.horizontalLayout_2.addWidget(self.cbIp)
        # self.horizontalLayout_2.addWidget(self.eip)
        self.bAddrEdit = QtWidgets.QToolButton(self.ipwidget)
        self.bAddrEdit.setMinimumSize(QtCore.QSize(32, 32))
        self.bAddrEdit.setMaximumSize(QtCore.QSize(32, 32))
        self.bAddrEdit.setIconSize(QtCore.QSize(24, 24))
        self.bAddrEdit.setObjectName("bAddrEdit")
        self.horizontalLayout_2.addWidget(self.bAddrEdit)

        self.verticalLayout.addWidget(self.ipwidget)

        self.cbwidget = QtWidgets.QWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.cbwidget.sizePolicy().hasHeightForWidth())
        self.cbwidget.setSizePolicy(sizePolicy)
        self.cbwidget.setObjectName("cbwidget")

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.cbwidget)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setSpacing(1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label1 = QtWidgets.QLabel(self.cbwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label1.sizePolicy().hasHeightForWidth())
        self.label1.setSizePolicy(sizePolicy)
        self.label1.setMinimumSize(QtCore.QSize(0, 26))
        self.label1.setObjectName("label1")
        self.label1.setMaximumSize(QtCore.QSize(16777215, 26))
        self.verticalLayout_2.addWidget(self.label1)

        self.lClipboard = MyLabel(self.cbwidget)
        self.lClipboard.setWordWrap(True)

        self.lClipboard.setStyleSheet("QLabel{color: #eee;\n"
                                      "    border-style: outset;\n"
                                      "    border-width: 1px;\n"
                                      "    border-color: #1b1b1b;\n"
                                      "}")
        self.lClipboard.setText("")
        self.lClipboard.setObjectName("lClipboard")
        self.verticalLayout_2.addWidget(self.lClipboard)
        self.bSend = QtWidgets.QPushButton(self.cbwidget)
        self.bSend.setObjectName("bSend")
        self.verticalLayout_2.addWidget(self.bSend)
        self.verticalLayout.addWidget(self.cbwidget)
        self.bwidget = QtWidgets.QWidget(self.centralwidget)
        self.bwidget.setMinimumSize(QtCore.QSize(0, 40))
        self.bwidget.setObjectName("bwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.bwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bSendFile = QtWidgets.QPushButton(self.bwidget)
        self.bSendFile.setObjectName("bSendFile")
        self.horizontalLayout.addWidget(self.bSendFile)
        self.bCancel = QtWidgets.QPushButton(self.bwidget)
        self.bCancel.setObjectName("bCancel")
        self.horizontalLayout.addWidget(self.bCancel)
        self.verticalLayout.addWidget(self.bwidget)

        self.retranslateUi(MainForm, lang)
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm, lang):
        MainForm.setWindowTitle(lang.tr("netbuffer"))
        self.lInfo.setText(lang.tr("dragandsend"))
        self.label2.setText(lang.tr("hostname"))
        self.label1.setText(lang.tr("onclipboardnow"))
        self.bSend.setText(lang.tr("sendfromclipboard"))
        self.bSendFile.setText(lang.tr("sendfile"))
        self.bCancel.setText(lang.tr("cancel"))
        self.bAddrEdit.setText("...")
