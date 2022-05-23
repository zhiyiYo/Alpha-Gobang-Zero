# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QPixmap, QPainter
from PyQt5.QtWidgets import QLabel


class ClickableLabel(QLabel):
    """ Clickable label """

    clicked = pyqtSignal()

    def __init__(self, text="", parent=None, isSendEventToParent: bool = True):
        super().__init__(text, parent)
        self.isSendEventToParent = isSendEventToParent

    def mousePressEvent(self, e):
        if self.isSendEventToParent:
            super().mousePressEvent(e)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """ 鼠标松开时发送信号 """
        if self.isSendEventToParent:
            super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.clicked.emit()



class PixmapLabel(QLabel):
    """ Label for high dpi pixmap """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__pixmap = QPixmap()

    def setPixmap(self, pixmap: QPixmap):
        self.__pixmap = pixmap
        self.setFixedSize(pixmap.size())
        self.update()

    def pixmap(self):
        return self.__pixmap

    def paintEvent(self, e):
        if self.__pixmap.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        painter.drawPixmap(self.rect(), self.__pixmap)
