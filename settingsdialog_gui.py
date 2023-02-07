# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SettingsDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(415, 433)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.w_lists = QtWidgets.QWidget(Dialog)
        self.w_lists.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.w_lists.setObjectName("w_lists")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.w_lists)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.w_whitelist = QtWidgets.QWidget(self.w_lists)
        self.w_whitelist.setObjectName("w_whitelist")
        self.vl_witelist = QtWidgets.QVBoxLayout(self.w_whitelist)
        self.vl_witelist.setContentsMargins(0, 0, 0, 0)
        self.vl_witelist.setObjectName("vl_witelist")
        self.l_whitelist = QtWidgets.QLabel(self.w_whitelist)
        self.l_whitelist.setObjectName("l_whitelist")
        self.vl_witelist.addWidget(self.l_whitelist)
        self.e_whitelist = QtWidgets.QPlainTextEdit(self.w_whitelist)
        self.e_whitelist.setObjectName("e_whitelist")
        self.vl_witelist.addWidget(self.e_whitelist)
        self.horizontalLayout.addWidget(self.w_whitelist)
        self.w_blacklist = QtWidgets.QWidget(self.w_lists)
        self.w_blacklist.setObjectName("w_blacklist")
        self.vl_blacklist = QtWidgets.QVBoxLayout(self.w_blacklist)
        self.vl_blacklist.setContentsMargins(0, 0, 0, 0)
        self.vl_blacklist.setObjectName("vl_blacklist")
        self.l_blacklist = QtWidgets.QLabel(self.w_blacklist)
        self.l_blacklist.setObjectName("l_blacklist")
        self.vl_blacklist.addWidget(self.l_blacklist)
        self.e_blacklist = QtWidgets.QPlainTextEdit(self.w_blacklist)
        self.e_blacklist.setObjectName("e_blacklist")
        self.vl_blacklist.addWidget(self.e_blacklist)
        self.l_blacklist_info = QtWidgets.QLabel(self.w_blacklist)
        self.l_blacklist_info.setObjectName("l_blacklist_info")
        self.vl_blacklist.addWidget(self.l_blacklist_info)
        self.horizontalLayout.addWidget(self.w_blacklist)
        self.verticalLayout.addWidget(self.w_lists)
        self.cb_onlywhitelist = QtWidgets.QCheckBox(Dialog)
        self.cb_onlywhitelist.setObjectName("cb_onlywhitelist")
        self.verticalLayout.addWidget(self.cb_onlywhitelist)
        self.gb_autotoclipboard = QtWidgets.QGroupBox(Dialog)
        self.gb_autotoclipboard.setMinimumSize(QtCore.QSize(0, 96))
        self.gb_autotoclipboard.setStyleSheet("QGroupBox { \n"
"     border: 1px solid gray; \n"
"     border-radius: 6px; \n"
" } ")
        self.gb_autotoclipboard.setFlat(False)
        self.gb_autotoclipboard.setCheckable(False)
        self.gb_autotoclipboard.setObjectName("gb_autotoclipboard")
        self.cb_textimage = QtWidgets.QCheckBox(self.gb_autotoclipboard)
        self.cb_textimage.setGeometry(QtCore.QRect(20, 30, 161, 21))
        self.cb_textimage.setObjectName("cb_textimage")
        self.cb_files = QtWidgets.QCheckBox(self.gb_autotoclipboard)
        self.cb_files.setGeometry(QtCore.QRect(20, 60, 161, 21))
        self.cb_files.setObjectName("cb_files")
        self.verticalLayout.addWidget(self.gb_autotoclipboard)
        self.ssl_widget = QtWidgets.QWidget(Dialog)
        self.ssl_widget.setMinimumSize(QtCore.QSize(0, 0))
        self.ssl_widget.setObjectName("ssl_widget")
        self.ssl_widget_layout = QtWidgets.QVBoxLayout(self.ssl_widget)
        self.ssl_widget_layout.setContentsMargins(0, 0, 0, 0)
        self.ssl_widget_layout.setObjectName("ssl_widget_layout")
        self.cb_ssl = QtWidgets.QCheckBox(self.ssl_widget)
        self.cb_ssl.setObjectName("cb_ssl")
        self.ssl_widget_layout.addWidget(self.cb_ssl)
        self.ssl_widget_2 = QtWidgets.QWidget(self.ssl_widget)
        self.ssl_widget_2.setObjectName("ssl_widget_2")
        self.ssl_widget_2_layout = QtWidgets.QGridLayout(self.ssl_widget_2)
        self.ssl_widget_2_layout.setContentsMargins(0, 0, 0, 0)
        self.ssl_widget_2_layout.setHorizontalSpacing(2)
        self.ssl_widget_2_layout.setVerticalSpacing(4)
        self.ssl_widget_2_layout.setObjectName("ssl_widget_2_layout")
        self.lCert = QtWidgets.QLabel(self.ssl_widget_2)
        self.lCert.setObjectName("lCert")
        self.ssl_widget_2_layout.addWidget(self.lCert, 0, 0, 1, 1)
        self.eCert = QtWidgets.QLineEdit(self.ssl_widget_2)
        self.eCert.setObjectName("eCert")
        self.ssl_widget_2_layout.addWidget(self.eCert, 0, 1, 1, 1)
        self.bCert = QtWidgets.QPushButton(self.ssl_widget_2)
        self.bCert.setObjectName("bCert")
        self.ssl_widget_2_layout.addWidget(self.bCert, 0, 2, 1, 1)
        self.lKey = QtWidgets.QLabel(self.ssl_widget_2)
        self.lKey.setObjectName("lKey")
        self.ssl_widget_2_layout.addWidget(self.lKey, 1, 0, 1, 1)
        self.eKey = QtWidgets.QLineEdit(self.ssl_widget_2)
        self.eKey.setObjectName("eKey")
        self.ssl_widget_2_layout.addWidget(self.eKey, 1, 1, 1, 1)
        self.bCert_2 = QtWidgets.QPushButton(self.ssl_widget_2)
        self.bCert_2.setObjectName("bCert_2")
        self.ssl_widget_2_layout.addWidget(self.bCert_2, 1, 2, 1, 1)
        self.ssl_widget_layout.addWidget(self.ssl_widget_2)
        self.verticalLayout.addWidget(self.ssl_widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.l_whitelist.setText(_translate("Dialog", "Белый список IP:"))
        self.l_blacklist.setText(_translate("Dialog", "Чёрый список IP:"))
        self.l_blacklist_info.setText(_translate("Dialog", "блокирует соединения"))
        self.cb_onlywhitelist.setText(_translate("Dialog", "Разрешать соединения только из белого списка"))
        self.gb_autotoclipboard.setTitle(_translate("Dialog", "Автоперенос данных  в буфер (для белого списка)"))
        self.cb_textimage.setText(_translate("Dialog", "Текст и изображения"))
        self.cb_files.setText(_translate("Dialog", "Файлы"))
        self.cb_ssl.setText(_translate("Dialog", "Использовать SSL соединение"))
        self.lCert.setText(_translate("Dialog", "Сертификат:"))
        self.bCert.setText(_translate("Dialog", "Обзор"))
        self.lKey.setText(_translate("Dialog", "Ключ:"))
        self.bCert_2.setText(_translate("Dialog", "Обзор"))
