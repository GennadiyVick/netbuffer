from PyQt5 import QtCore, QtGui, QtWidgets
import images

class MyLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.clicked.emit()

class Ui_ConnectionsDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(348, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tv = QtWidgets.QTableView(self.widget)
        self.tv.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.tv.setStyleSheet("background: #333;")
        #self.tv.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tv.horizontalHeader().setStretchLastSection(True)
        self.tv.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tv.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tv.setObjectName("tv")
        self.tv.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.tv)
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setMinimumSize(QtCore.QSize(40, 0))
        self.widget_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.bAdd = MyLabel(self.widget_2)
        self.bAdd.setMinimumSize(QtCore.QSize(40, 40))
        self.bAdd.setMaximumSize(QtCore.QSize(40, 40))
        self.bAdd.setObjectName("bAdd")
        self.bAdd.setPixmap(QtGui.QPixmap(':/add.png'))
        self.bAdd.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.bAdd.setStyleSheet('QLabel:hover {background: #40000000; border-style: inset; border-width: 1px; border-color: #a0404050;  border-radius: 4px;}')
        self.verticalLayout_2.addWidget(self.bAdd)
        self.bDel = MyLabel(self.widget_2)
        self.bDel.setMinimumSize(QtCore.QSize(40, 40))
        self.bDel.setMaximumSize(QtCore.QSize(40, 40))
        self.bDel.setObjectName("bDel")
        self.bDel.setPixmap(QtGui.QPixmap(':/delete.png'))
        self.bDel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.bDel.setStyleSheet('QLabel:hover {background: #40000000; border-style: inset; border-width: 1px; border-color: #a0404050;  border-radius: 4px;}')
        self.verticalLayout_2.addWidget(self.bDel)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout.addWidget(self.widget_2)
        self.verticalLayout.addWidget(self.widget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)


        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)




