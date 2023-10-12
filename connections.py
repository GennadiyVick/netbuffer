from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from connections_gui import Ui_ConnectionsDialog


class ConnectionsDialog(QtWidgets.QDialog):
    def __init__(self, connections, lang, parent=None):
        super(ConnectionsDialog, self).__init__(parent)
        self.ui = Ui_ConnectionsDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(lang.tr('connections'))
        self.connections = connections.copy()
        self.model = QtGui.QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(lang.tr('conn_dlg_header'))
        self.model.setRowCount(len(self.connections))
        for i, con in enumerate(connections):
            self.model.setItem(i, 0, QtGui.QStandardItem(con['name']))
            self.model.setItem(i, 1, QtGui.QStandardItem(con['ip']))
            self.model.setItem(i, 2, QtGui.QStandardItem(str(con['port'])))

        self.ui.tv.setModel(self.model)
        self.ui.tv.setColumnWidth(0, 100)
        self.ui.tv.setColumnWidth(1, 120)
        self.ui.tv.setColumnWidth(2, 50)
        self.ui.bAdd.clicked.connect(self.addrow)
        self.ui.bDel.clicked.connect(self.delrow)

    def addrow(self):
        con = {'name': '', 'ip': '', 'port': 5305}
        self.connections.append(con)
        self.model.setRowCount(len(self.connections))
        for j, key in enumerate(con):
            self.model.setItem(len(self.connections) - 1, j, QtGui.QStandardItem(str(con[key])))

    def delrow(self):
        r = self.ui.tv.selectionModel().selectedRows()[0].row()
        del self.connections[r]
        self.model.removeRow(r)

    def getConnections(self):
        result = []
        for i in range(self.model.rowCount()):
            result.append({'name': self.model.item(i, 0).text(), 'ip': self.model.item(i, 1).text(),
                           'port': int(self.model.item(i, 2).text())})
        return result


def main():
    app = QtWidgets.QApplication(sys.argv)
    dlg = ConnectionsDialog([{'name': 'MyComp', 'ip': '10.51.3.100', 'port': 5305}])
    if dlg.exec() == 1:
        print(dlg.getConnections())
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
