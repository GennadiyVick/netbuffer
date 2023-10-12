from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtProperty, QPropertyAnimation, QSize, QRect, QTimer
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtWidgets import QApplication


class MessagePopup(QtWidgets.QWidget):
    @pyqtProperty(float)
    def popupOpacity(self):
        return self._popupOpacity

    @popupOpacity.setter
    def popupOpacity(self, opacity):
        self._popupOpacity = opacity
        self.setWindowOpacity(opacity)

    ''' for errors messages only '''
    '''@pyqtProperty(float)
    def popupOpacity(self):
        return self._popupOpacity;

    @popupOpacity.setter'''
    '''
    def set_popupOpacity(self, opacity):
        self._popupOpacity = opacity
        self.setWindowOpacity(opacity)


    popupOpacity = pyqtProperty(float, fset=set_popupOpacity)
    '''

    def __init__(self, msg):
        super(MessagePopup, self).__init__()
        self._popupOpacity = 0
        self.setObjectName("MessagePopup")
        self.resize(348, 96)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label.setStyleSheet("QLabel{color: #eee;}")
        self.label.setText(msg)
        self.horizontalLayout.addWidget(self.label)
        self.setWindowTitle("Message")
        # QtCore.QMetaObject.connectSlotsByName(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        self.animation = QPropertyAnimation()
        self.animation.setTargetObject(self)
        self.animation.setPropertyName(b'popupOpacity')
        self.animation.finished.connect(self.hide)
        # self.animation = QPropertyAnimation(self, b'popupOpacity')
        # self.animation = QPropertyAnimation(self, b'windowOpacity')
        # self.animation = QPropertyAnimation(self.fadeEffect, b'opacity')
        # self.animation.setTargetObject(self.fadeEffect)

        self.timer = QTimer()
        self.timer.timeout.connect(self.hideAnimation)
        # self.anitimer = QTimer()
        # self.anitimer.setInterval(60)
        # self.anitimer.timeout.connect(self.on_anitimer)
        # self.curopacity = 0.1
        # self.ani_showing = True
        # self.timer.start(4000)

    def hide(self):
        if (self._popupOpacity == 0):
            super().close()

    def show(self):
        self.setWindowOpacity(0.0)  # Set the transparency to zero
        self.animation.setDuration(150)  # Configuring the duration of the animation
        self.animation.setStartValue(0.0)  # The start value is 0 (fully transparent widget)
        self.animation.setEndValue(1.0)  # End - completely opaque widget
        g = QApplication.desktop().availableGeometry()
        self.setGeometry(g.width() - 36 - self.width() + g.x(),
                         g.height() - 36 - self.height() + g.y(), self.width(), self.height())
        super().show()
        self.animation.start();
        self.timer.start(5000);

    '''def show(self):
        self.setWindowOpacity(1.0)
        #self.animation.setDuration(400)
        #self.animation.setStartValue(0.1)
        #self.animation.setEndValue(1.0)
        #self.animation.setLoopCount(10)
        g = QApplication.desktop().availableGeometry()
        self.setGeometry(g.width() - 36 - self.width() + g.x(),
            g.height() - 36 - self.height() + g.y(),  self.width(), self.height())
        super().show()
        #self.animation.start();
        print('animation started')
        self.anitimer.start()
        self.timer.start(4000)'''

    def hideAnimation(self):
        self.timer.stop()
        self.animation.setDuration(600)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        roundedRect = QRect()
        roundedRect.setX(self.rect().x() + 5)
        roundedRect.setY(self.rect().y() + 5)
        roundedRect.setWidth(self.rect().width() - 10)
        roundedRect.setHeight(self.rect().height() - 10)
        painter.setBrush(QBrush(QColor(0, 0, 0, 180)))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(roundedRect, 10, 10)
