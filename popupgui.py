from PyQt5 import QtCore, QtGui, QtWidgets
from mylabel import MyLabel

class Ui_NotifyDialog(object):
    def setupUi(self, NotifyDialog):
        NotifyDialog.setObjectName("NotifyDialog")
        NotifyDialog.resize(441, 233)
        self.horizontalLayout = QtWidgets.QHBoxLayout(NotifyDialog)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.scrollArea = QtWidgets.QScrollArea(NotifyDialog)
        self.scrollArea.setStyleSheet('QScrollArea{background: #00000000;}') 
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame);
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setStyleSheet('QWidget#scrollAreaWidgetContents {background: #00000000;}')
        #self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -540, 367, 895))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.label = MyLabel(self.scrollAreaWidgetContents) #NotifyDialog) #QtWidgets.QLabel(NotifyDialog)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label.setStyleSheet("QLabel{color: #eee;}")
        self.verticalLayout_2.addWidget(self.label)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout.addWidget(self.scrollArea)#self.label)

        self.widget = QtWidgets.QWidget(NotifyDialog)
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lInfo = QtWidgets.QLabel(self.widget)
        self.lInfo.setWordWrap(True)
        self.lInfo.setObjectName("lInfo")
        self.lInfo.setStyleSheet("QLabel{color: #eee;}")
        self.verticalLayout.addWidget(self.lInfo)
        self.bCopy = QtWidgets.QPushButton(self.widget)
        self.bCopy.setObjectName("bCopy")
        self.verticalLayout.addWidget(self.bCopy)
        self.bCopyFile = QtWidgets.QPushButton(self.widget)
        self.bCopyFile.setObjectName("bCopyFile")
        self.verticalLayout.addWidget(self.bCopyFile)
        self.bOpenFile = QtWidgets.QPushButton(self.widget)
        self.bOpenFile.setObjectName("bOpenFile")
        self.bOpenFile.setVisible(False)
        self.verticalLayout.addWidget(self.bOpenFile)
        #self.bOpen = QtWidgets.QPushButton(self.widget)
        #self.bOpen.setObjectName("bOpen")
        #self.verticalLayout.addWidget(self.bOpen)
        self.bCancel = QtWidgets.QPushButton(self.widget)
        self.bCancel.setObjectName("bCancel")
        self.verticalLayout.addWidget(self.bCancel)
        self.bSpam = QtWidgets.QPushButton(self.widget)
        self.bSpam.setObjectName("bSpam")
        self.verticalLayout.addWidget(self.bSpam)

        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(NotifyDialog)
        QtCore.QMetaObject.connectSlotsByName(NotifyDialog)

    def retranslateUi(self, NotifyDialog):
        _translate = QtCore.QCoreApplication.translate
        NotifyDialog.setWindowTitle(_translate("NotifyDialog", "Dialog"))
        self.label.setText(_translate("NotifyDialog", "TextLabel"))
        self.lInfo.setText(_translate("NotifyDialog", "Информация"))
        self.bCopy.setText(_translate("NotifyDialog", "Копировать"))
        self.bCopyFile.setText(_translate("NotifyDialog", "Сохранить файл"))
        self.bOpenFile.setText(_translate("Open file", "Открыть файл"))
        #self.bOpen.setText(_translate("NotifyDialog", "Открыть"))
        self.bCancel.setText(_translate("NotifyDialog", "Отмена"))
        self.bSpam.setText(_translate("Block this IP", "Блокировать IP"))
