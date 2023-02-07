import os
from PyQt5 import QtCore, QtGui, QtWidgets
from settingsdialog_gui import Ui_SettingsDialog

class Settings:
    def __init__(self):
        self.load()

    def load(self):
        set = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, os.path.join('RoganovSoft', 'NetClipBoard'), "config")
        self.setpath = os.path.dirname(set.fileName())
        if os.name == 'nt':
            self.setpath = self.setpath.replace('/', '\\')
        self.serverport = int(set.value('serverport',5305))
        self.auto_copy_to_clipboard = set.value('auto_copy_to_clipboard', '1') == '1'
        self.auto_copy_file_to_clipboard = set.value('auto_copy_file_to_clipboard', '1') == '1'
        self.onlywhitelist = set.value('onlywhitelist', '1') == '1'
        self.ssl = set.value('ssl', '0') == '1'
        self.ssl_certfile = set.value('ssl_certfile','')
        self.ssl_keyfile = set.value('ssl_keyfile','')
        if self.ssl:
            if len(self.ssl_certfile) < 2 or len(self.ssl_keyfile) < 2 or not os.path.isfile(self.ssl_certfile) or not os.path.isfile(self.ssl_keyfile):
                print('Файл сертификата и/или ключа не найден, канал будет создан открытым.')
                self.ssl = False
        self.loadlists()

    def save(self):
        set = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, os.path.join('RoganovSoft', 'NetClipBoard'), "config")
        set.setValue('serverport', self.serverport)
        set.setValue('auto_copy_to_clipboard', '1' if self.auto_copy_to_clipboard else '0')
        set.setValue('auto_copy_file_to_clipboard', '1' if self.auto_copy_file_to_clipboard else '0')
        set.setValue('ssl', '1' if self.ssl else '0')
        set.setValue('ssl_certfile', self.ssl_certfile)
        set.setValue('ssl_keyfile', self.ssl_keyfile)
        self.savelists()


    def loadlists(self):
        if os.path.isfile(os.path.join(self.setpath, 'whitelist.txt')):
            with open(os.path.join(self.setpath, 'whitelist.txt')) as f:
                self.whitelist = [line.strip() for line in f]
        else:
            self.whitelist = []
        if os.path.isfile(os.path.join(self.setpath, 'blacklist.txt')):
            with open(os.path.join(self.setpath, 'blacklist.txt')) as f:
                self.blacklist = [line.strip() for line in f]
        else:
            self.blacklist = []

    def savelists(self):
        with open(os.path.join(self.setpath, 'whitelist.txt'), 'w') as f:
            for line in self.whitelist:
                f.write(line+'\n')
        with open(os.path.join(self.setpath, 'blacklist.txt'), 'w') as f:
            for line in self.blacklist:
                f.write(line+'\n')

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, sets, parent = None):
        super(SettingsDialog,self).__init__(parent)
        self.ui = Ui_SettingsDialog()
        self.ui.setupUi(self)
        self.sets = sets
        self.setsToGui()

    def setsToGui(self):
        self.ui.e_whitelist.setPlainText('\n'.join(self.sets.whitelist))
        self.ui.e_blacklist.setPlainText('\n'.join(self.sets.blacklist))
        self.ui.cb_onlywhitelist.setChecked(self.sets.onlywhitelist)
        self.ui.cb_textimage.setChecked(self.sets.auto_copy_to_clipboard)
        self.ui.cb_files.setChecked(self.sets.auto_copy_file_to_clipboard)
        self.ui.cb_ssl.setChecked(self.sets.ssl)
        self.ui.eCert.setText(self.sets.ssl_certfile)
        self.ui.eKey.setText(self.sets.ssl_keyfile)

    def guiToSets(self):
        #self.sets.whitelist = self.ui.e_whitelist.toPlainText().split('\n') #так нельзя потому, что добовляется пустая строка
        self.sets.whitelist.clear()
        self.sets.blacklist.clear()
        lst = self.ui.e_whitelist.toPlainText().split('\n')
        for l in lst:
            if len(l) > 1:
                self.sets.whitelist.append(l)
        lst = self.ui.e_blacklist.toPlainText().split('\n')
        for l in lst:
            if len(l) > 1:
                self.sets.blacklist.append(l)
        self.sets.onlywhitelist = self.ui.cb_onlywhitelist.isChecked()
        self.sets.auto_copy_to_clipboard = self.ui.cb_textimage.isChecked()
        self.sets.auto_copy_file_to_clipboard = self.ui.cb_files.isChecked()
        self.sets.ssl = self.ui.cb_ssl.isChecked()
        self.sets.ssl_certfile = self.ui.eCert.text()
        self.sets.ssl_keyfile = self.ui.eKey.text()
        if len(self.sets.ssl_certfile) < 2 or len(self.sets.ssl_keyfile) < 2 or not os.path.isfile(self.sets.ssl_certfile) or not os.path.isfile(self.sets.ssl_keyfile):
            print('Файл сертификата и/или ключа не найден, канал будет создан открытым.')
            self.sets.ssl = False

    def accept(self):
        self.guiToSets()
        super(SettingsDialog,self).accept()


