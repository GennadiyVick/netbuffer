from PyQt5.QtWidgets import QLabel


class MyLabel(QLabel):
    def __init__(self, parent):
        super(MyLabel, self).__init__(parent)
        self.pixmapWidth = 0
        self.pixmapHeight = 0

    def setPixmap(self, pm):
        if pm is not None:
            self.pixmapWidth = pm.width()
            self.pixmapHeight = pm.height()
            self.updateMargins()
        else:
            self.pixmapWidth = 0
            self.pixmapHeight = 0
        super().setPixmap(pm)

    def resizeEvent(self, event):
        self.updateMargins()
        super().resizeEvent(event)

    def updateMargins(self):
        if self.pixmapWidth <= 0 | self.pixmapHeight <= 0:
            return
        w = self.width()
        h = self.height()
        if w <= 0 | h <= 0:
            return
        if w * self.pixmapHeight > h * self.pixmapWidth:
            m = round((w - (self.pixmapWidth * h / self.pixmapHeight)) / 2)
            self.setContentsMargins(m, 0, m, 0)
        else:
            m = round((h - (self.pixmapHeight * w / self.pixmapWidth)) / 2)
            self.setContentsMargins(0, m, 0, m)
