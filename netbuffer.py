#!/usr/bin/python3

"""Автор Роганов Геннадий
email: roganovg@mail.ru
подробности в readme.txt"""

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, \
    QAction, QMenu, QMainWindow, QSizePolicy, QMessageBox, QFileDialog
from PyQt5.QtCore import QSettings, Qt, QThread, QMimeData, QUrl
from PyQt5.QtGui import QIcon, QGuiApplication, QPixmap
import sys
import os
from os.path import join
from pathlib import Path
from server import StreamServer, DataHeader, Sender, SenderFile
from gui import Ui_MainForm
from popup import PopupWidget
from messagepopup import MessagePopup
from connections import ConnectionsDialog
from config import APP_DIR, CACHE_DIR
from settings import Settings, SettingsDialog
from lang import Lang


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(None)
        self.active_action = None
        self.tray = None
        self.sender = None
        self.thread = None
        self.lang = Lang()
        self.ui = Ui_MainForm()
        self.ui.setupUi(self, self.lang)
        self.appdir = APP_DIR
        os.chdir(self.appdir)
        if not os.path.isdir(CACHE_DIR):
            os.mkdir(CACHE_DIR)
        else:
            for fn in os.listdir(CACHE_DIR):
                fn = os.path.join(CACHE_DIR, fn)
                try:
                    if os.path.isfile(fn):
                        os.remove(fn)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (fn, e))
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.serv = None
        self.initTray()
        self.app = parent
        self.mustClose = False
        self.hdr = None
        self.active_action.setChecked(True)
        self.ui.bSend.clicked.connect(self.sendFromClipboard)
        self.ui.bSendFile.clicked.connect(self.sendFromFile)
        self.ui.bCancel.clicked.connect(self.cancelsend)
        self.ui.bAddrEdit.clicked.connect(self.addredit)
        self.sets = Settings(self.lang)
        sets = QSettings(QSettings.IniFormat, QSettings.UserScope, join('RoganovSoft', 'NetClipBoard'), "config")
        itemscount = sets.beginReadArray("items")
        self.connections = []
        for i in range(itemscount):
            sets.setArrayIndex(i)
            ip = sets.value('ip', '')
            port = int(sets.value("port", 5305))
            name = sets.value('name', '')
            if len(ip) > 2:
                self.connections.append({'ip': ip, 'port': port, 'name': name})
                self.ui.cbIp.addItem(name + ' [' + ip + ']')
        sets.endArray()
        self.ui.cbIp.setCurrentIndex(int(sets.value('CurrentIndex', -1)))
        self.ui.cbIp.activated.connect(self.cbitemchanged)
        self.setAcceptDrops(True)
        self.startserver(True)

    def startserver(self, start):
        if start:
            thread = QThread()
            self.serv = StreamServer(thread, self.sets)
            self.serv.onFinish.connect(self.threadFinish)
            self.serv.onRead.connect(self.doRead)
            self.serv.moveToThread(thread)
            thread.started.connect(self.serv.run)
            thread.start()
        else:
            if self.serv != None:
                self.serv.keep_running = False

    def activeActionClick(self):
        self.startserver(self.active_action.isChecked())

    def threadFinish(self, err):
        self.serv = None
        self.active_action.setChecked(False)
        if self.mustClose:
            self.doQuit()
        else:
            if (len(err) > 0):
                QMessageBox.information(self, self.lang.tr('error'), err)

    def doRead(self, hdr):
        if hdr.addr[0] in self.sets.whitelist:
            if hdr.filetype == 1 or hdr.filetype == 2:
                if self.sets.auto_copy_to_clipboard:
                    if hdr.filetype == 2:
                        cb = QGuiApplication.clipboard()
                        with open(os.path.join(CACHE_DIR, hdr.filename), 'r', encoding='utf-8') as f:
                            cb.setText(f.read())
                        msg = MessagePopup(self.lang.tr('textcopied'))
                        msg.show()
                    else:
                        cb = QGuiApplication.clipboard()
                        pix = QPixmap(os.path.join(CACHE_DIR, hdr.filename))
                        cb.setPixmap(pix)
                        msg = MessagePopup(self.lang.tr('imagecopied'))
                        msg.show()
                    return
            elif self.sets.auto_copy_file_to_clipboard:
                cb = QGuiApplication.clipboard()
                mime = QMimeData()
                fn = 'file://' + os.path.join(CACHE_DIR, hdr.filename)
                if os.name == 'nt':
                    fn = 'file:///' + os.path.join(CACHE_DIR, hdr.filename)
                    mime.setUrls([QUrl(fn)])
                else:
                    gnomeFormat = f"copy\n{fn}".encode('utf-8')
                    mime.setData("x-special/gnome-copied-files", gnomeFormat)
                cb.setMimeData(mime)
                msg = MessagePopup(self.lang.tr('filecopied'))
                msg.show()
                return
        popup = PopupWidget(hdr, self.sets, self.lang)
        popup.show()

    def cbitemchanged(self):
        set = QSettings(QSettings.IniFormat, QSettings.UserScope, join('RoganovSoft', 'NetClipBoard'), "config")
        set.setValue('CurrentIndex', self.ui.cbIp.currentIndex())

    def doQuit(self):
        if self.serv is not None:
            self.mustClose = True
            self.startserver(False)
            # self.serv.stop()
        else:
            sets = QSettings(QSettings.IniFormat, QSettings.UserScope, join('RoganovSoft', 'NetClipBoard'), "config")
            sets.setValue('CurrentIndex', self.ui.cbIp.currentIndex())
            self.app.quit()

    def closeEvent(self, event):
        print('close event')

    def clipboardcheck(self):
        cb = QGuiApplication.clipboard()
        md = cb.mimeData()
        if self.hdr is None:
            self.hdr = DataHeader(None)
        self.hdr.filetype = 0
        res = False
        if md.hasImage():
            self.hdr.filetype = 1
            self.hdr.filename = 'image.png'
            self.ui.label1.setText(self.lang.tr('imageinclipboard'))
            self.ui.lClipboard.setScaledContents(True)
            self.ui.lClipboard.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.ui.lClipboard.setPixmap(cb.pixmap())
            res = True
        elif md.hasUrls():
            self.hdr.filetype = 3
            fn = cb.text()
            if fn[:8] == 'file:///': fn = fn[8:]
            self.hdr.filename = fn
            self.ui.label1.setText(self.lang.tr('fileinclipboard'))
            self.ui.lClipboard.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            self.ui.lClipboard.setText(fn)
            res = True
        elif md.hasText():
            self.hdr.filetype = 2
            self.hdr.filename = 'document.txt'
            self.ui.label1.setText(self.lang.tr('textinclipboard'))

            self.ui.lClipboard.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
            self.ui.lClipboard.setText(cb.text())
            res = True
        else:
            self.ui.label1.setText(self.lang.tr('emptyclipboard'))
            self.ui.lClipboard.setText('')
        return res

    def doSend(self):
        self.clipboardcheck()
        self.show()

    def sendclipboard(self):
        if self.clipboardcheck():
            self.sendFromClipboard()
        else:
            self.show()

    def senddata(self, hdr, data, ip, port):
        """ отправляем потоком QThread
            почему не threading.Thread: потому что при ошибке необходимо
            запустить уведомление, а оно из потока не может быть запущено
            поэтому решаем проблему pyqtSignal """
        self.thread = QThread()
        self.sender = Sender(hdr, data, (ip, port), self.thread, self.sets.ssl)
        self.sender.moveToThread(self.thread)
        self.sender.onError.connect(self.sendError)
        self.thread.started.connect(self.sender.run)
        self.thread.start()

    def getMimeData(self, cb, md):
        f = 'PNG'
        formats = md.formats()
        if ('image/png' in formats) or ('application/x-qt-image' in formats):
            self.hdr.filename = 'image.png'
        else:
            self.hdr.filename = 'image.jpg'
            f = 'JPEG'
        ba = QtCore.QByteArray()
        buff = QtCore.QBuffer(ba)
        buff.open(QtCore.QIODevice.WriteOnly)
        md.imageData().save(buff, f)
        return ba.data()

    def sendFile(self, ip, port):
        self.thread = QThread()
        self.sender = SenderFile(self.hdr, (ip, port), self.thread, self.sets.ssl)
        self.sender.moveToThread(self.thread)
        self.sender.onError.connect(self.sendError)
        self.thread.started.connect(self.sender.run)
        self.thread.start()

    def sendFromFile(self):
        if self.hdr is None:
            print('sendFromFile: hdr = None')
            return
        i = self.ui.cbIp.currentIndex()
        if i < 0:
            print('can not send a data becouse destination ip not selected')
            return
        ip = self.connections[i]['ip']
        port = self.connections[i]['port']
        if len(ip) < 3:
            print('sendFromFile: length of ip < 3')
            return
        fn, _ = QFileDialog.getOpenFileName(self, self.lang.tr('open'), str(Path.home()))
        self.hdr.filename = fn
        self.sendFile(ip, port)
        self.hide()

    def sendFromClipboard(self):
        i = self.ui.cbIp.currentIndex()
        if i < 0:
            msg = MessagePopup(self.lang.tr('noipaddress'))
            msg.show()
            return
        ip = self.connections[i]['ip']
        port = self.connections[i]['port']
        if self.hdr is None:
            print('sendFromFile: hdr = None')
            return
        if len(ip) < 3:
            print('sendFromFile: length of ip < 3')
            return
        cb = QGuiApplication.clipboard()
        md = cb.mimeData()
        data = None
        if self.hdr.filetype == 2:
            data = cb.text().encode('utf-8')
        elif self.hdr.filetype == 1:
            if not md.hasImage():
                print('sendFromClipboard: meta data has no image')
                return
            data = self.getMimeData(cb, md)
        elif self.hdr.filetype == 3:
            if '\n' in self.hdr.filename:
                self.sendError(self.lang.tr('multiplefileerror'))
            else:
                self.sendFile(ip, port)
            self.hide()
            return
        else:
            print('sendFromClipboard: hdr.filetype unsupported')
            return

        if data is None:
            print('sendFromClipboard: data to send = None, hdr.filetype=', self.hdr.filetype)
            return
        self.hdr.filesize = len(data)
        self.senddata(self.hdr, data, ip, port)
        self.hide()

    def sendError(self, msg):
        print(msg)
        msg = MessagePopup(msg)
        msg.show()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls: e.accept()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls: e.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            if self.hdr is None: return
            i = self.ui.cbIp.currentIndex()
            if i < 0:
                print('can not send a data becouse destination ip not selected')
                return
            ip = self.connections[i]['ip']
            port = self.connections[i]['port']
            event.setDropAction(Qt.CopyAction)
            event.accept()
            url = event.mimeData().urls()[0]
            fn = str(url.toLocalFile())
            self.hdr.filename = fn
            self.sendFile(ip, port)
            self.hide()

    def cancelsend(self):
        self.hide()
        cb = QGuiApplication.clipboard()
        md = cb.mimeData()
        if len(md.formats()) == 0: return

    def showsettings(self):
        dlg = SettingsDialog(self.sets, self.lang)
        if dlg.exec():
            self.sets.save()

    def initTray(self):
        self.tray = QSystemTrayIcon(self)
        icon = QIcon(":/cb.png")
        self.tray.setIcon(icon)
        self.tray.setToolTip("NetBuffer")
        self.setWindowIcon(icon)

        self.active_action = QAction(self.lang.tr("receivedata"), self)
        self.active_action.setCheckable(True)
        self.active_action.triggered.connect(self.activeActionClick)

        showmain_action = QAction(self.lang.tr("send"), self)
        showmain_action.triggered.connect(self.doSend)

        setting_action = QAction(self.lang.tr('settings'), self)
        setting_action.triggered.connect(self.showsettings)

        quit_action = QAction(self.lang.tr("exit"), self)
        quit_action.triggered.connect(self.doQuit)

        traymenu = QMenu()
        traymenu.addAction(self.active_action)
        traymenu.addAction(showmain_action)
        traymenu.addAction(setting_action)
        traymenu.addAction(quit_action)
        self.tray.setContextMenu(traymenu)
        self.tray.activated.connect(self.trayActivated)
        self.tray.show()

    def trayActivated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.sendclipboard()

    def addredit(self):
        dlg = ConnectionsDialog(self.connections, self.lang, self)
        if dlg.exec() == 1:
            self.connections = dlg.getConnections()
            self.ui.cbIp.clear()
            sets = QSettings(QSettings.IniFormat, QSettings.UserScope, join('RoganovSoft', 'NetClipBoard'), "config")
            sets.beginWriteArray("items")
            for i, con in enumerate(self.connections):
                if len(con['ip']) > 3:
                    sets.setArrayIndex(i)
                    sets.setValue('name', con['name'])
                    sets.setValue('ip', con['ip'])
                    sets.setValue('port', con['port'])
                    self.ui.cbIp.addItem(con['name'] + ' [' + con['ip'] + ']')

            sets.endArray()
            sets.sync()


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    appdir = os.path.dirname(os.path.realpath(__file__))
    fn = os.path.join(appdir, 'dark.qss')
    if os.path.isfile(fn):
        with open(fn, 'r') as f:
            darktheme = f.read()
        app.setStyleSheet(darktheme)
    main = MainWindow(app)
    # main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
