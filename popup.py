from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QSizePolicy, QFileDialog
from PyQt5.QtCore import QSize, QRect, Qt, QPropertyAnimation, QTimer, QObject, pyqtProperty
from PyQt5.QtGui import QPainter, QBrush, QColor, QPixmap, QGuiApplication
from server import DataHeader
from popupgui import Ui_NotifyDialog
from shutil import copyfile
from pathlib import Path
import subprocess
import tempfile
import os
from config import CACHE_DIR
#https://evileg.com/en/post/146/
class PopupWidget(QtWidgets.QWidget):
    ''' show text or image when buffer received '''
    @pyqtProperty(float)
    def popupOpacity(self):
        return self._popupOpacity;

    @popupOpacity.setter
    def popupOpacity(self, opacity):
        self._popupOpacity = opacity
        self.setWindowOpacity(opacity)

    def __init__(self, hdr, sets,  onPopupResult):
        super(PopupWidget, self).__init__()
        self._popupOpacity = 0
        self.ui = Ui_NotifyDialog()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool |  Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.animation = QPropertyAnimation()
        self.animation.setTargetObject(self)
        self.animation.setPropertyName(b'popupOpacity')
        self.animation.finished.connect(self.hide)
        self.timer = QTimer()
        self.timer.timeout.connect(self.hideAnimation)
        self.ui.bCancel.clicked.connect(self.doCancel)
        self.ui.bSpam.clicked.connect(self.toBlock)
        self.popupResult = 2
        self.onPopupResult = onPopupResult
        self.hdr = hdr
        self.sets = sets
        fs = round(hdr.filesize / 1024, 2)
        self.ui.lInfo.setText(f'Отправленно от {hdr.addr[0]}\nФайл: {hdr.filename}\nРазмер файла: {fs} Kb.')
        if hdr.filetype == 2:
            with open(os.path.join(CACHE_DIR, hdr.filename),'r', encoding = 'utf-8') as f:
                self.ui.label.setText(f.read())
        elif hdr.filetype == 1:
            self.ui.label.setText('')
            pix = QPixmap(os.path.join(CACHE_DIR, hdr.filename))
            self.ui.label.setScaledContents(True)
            self.ui.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            self.ui.label.setPixmap(pix)
        else:
            self.ui.bCopy.setVisible(False)
            self.ui.label.setText('')
            self.ui.bOpenFile.setVisible(True)

        self.ui.bCopy.clicked.connect(self.copy)
        self.ui.bCopyFile.clicked.connect(self.save)
        self.ui.bOpenFile.clicked.connect(self.openfile)

    def copy(self):
        cb = QGuiApplication.clipboard()
        if self.hdr.filetype == 2:
            cb.setText(self.ui.label.text())
        elif self.hdr.filetype == 1:
            cb.setPixmap(self.ui.label.pixmap())

        self.timer.stop()
        self.timer.start(400)

    def save(self):
        self.timer.stop()
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fn = os.path.join(CACHE_DIR, self.hdr.filename)
        fn,_ = QFileDialog.getSaveFileName(self,'Сохранить как...',fn,options=options)
        self.timer.start(400)
        if len(fn) > 0:
            copyfile(os.path.join(CACHE_DIR, self.hdr.filename), fn)


    def openfile(self):
        self.timer.stop()
        #fn = os.path.join(tempfile.gettempdir(), self.hdr.filename)
        #fn = Path(os.path.realpath(__file__)).parent / self.hdr.filename
        #copyfile(os.path.join(CACHE_DIR, self.hdr.filename), fn)
        fn = os.path.join(CACHE_DIR, self.hdr.filename)

        if os.name == 'nt':
            os.startfile(fn)
        else:
            subprocess.Popen(['xdg-open', fn])

        self.timer.start(400)

    def toBlock(self):
        self.timer.stop()
        if self.hdr.addr[0] in self.sets.whitelist:
            self.sets.whitelist.remove(self.hdr.addr[0])
        self.sets.blacklist.append(self.hdr.addr[0])
        self.sets.save()
        self.timer.start(400)



    #def closeEvent(self,event):
    #    super(MessagePopup, self).closeEvent(event)

    def hide(self):
        if (self._popupOpacity == 0):
            super().hide()
            '''if len(self.hdr.filename) > 1:
                try:
                    os.remove(os.path.join(CACHE_DIR, self.hdr.filename))
                except:
                    pass'''
            if (self.onPopupResult != None):
                self.onPopupResult(self)
            super().close()

    def setPopupText(self, text):
       self.ui.label.setText(text)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing);
        roundedRect = QRect()
        roundedRect.setX(self.rect().x() + 5);
        roundedRect.setY(self.rect().y() + 5);
        roundedRect.setWidth(self.rect().width() - 10);
        roundedRect.setHeight(self.rect().height() - 10);
        painter.setBrush(QBrush(QColor(0,0,0,180)));
        painter.setPen(Qt.NoPen);
        painter.drawRoundedRect(roundedRect, 10, 10);

    def show(self):
        self.setWindowOpacity(0.0) # Set the transparency to zero
        self.animation.setDuration(150) # Configuring the duration of the animation
        self.animation.setStartValue(0.0) # The start value is 0 (fully transparent widget)
        self.animation.setEndValue(1.0)  # End - completely opaque widget
        g = QApplication.desktop().availableGeometry()
        self.setGeometry(g.width() - 36 - self.width() + g.x(),
            g.height() - 36 - self.height() + g.y(),  self.width(), self.height())
        super().show()
        self.animation.start();
        self.timer.start(30000);

    def hideAnimation(self):
        self.timer.stop()
        self.animation.setDuration(1000);
        self.animation.setStartValue(1.0);
        self.animation.setEndValue(0.0);
        self.animation.start();

    def doCancel(self):
        self.popupResult = 2
        self.hideAnimation()
