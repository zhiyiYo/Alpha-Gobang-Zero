# coding:utf-8
from app.components.widgets.label import PixmapLabel
from PyQt5.QtCore import QFile, Qt
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtWidgets import QLabel, QWidget
from win32.lib import win32con
from win32.win32api import SendMessage
from win32.win32gui import ReleaseCapture

from .title_bar_buttons import MaximizeButton, TitleBarButton


class TitleBar(QWidget):
    """ 定义标题栏 """

    def __init__(self, parent):
        super().__init__(parent)
        self.resize(700, 40)
        self.iconLabel = PixmapLabel(self)
        self.minButton = TitleBarButton(parent=self)
        self.closeButton = TitleBarButton(parent=self)
        self.maxButton = MaximizeButton(self)
        self.titleLabel = QLabel('Alpha Gobang Zero', self)

        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.setFixedHeight(40)
        self.iconLabel.move(9, 9)
        self.titleLabel.move(34, 8)
        self.setAttribute(Qt.WA_StyledBackground)
        self.iconLabel.setPixmap(QPixmap(':/images/icon/二哈.png').scaled(
            20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        self.__setQss()

        # 将按钮的点击信号连接到槽函数
        self.minButton.clicked.connect(self.window().showMinimized)
        self.maxButton.clicked.connect(self.__showRestoreWindow)
        self.closeButton.clicked.connect(self.window().close)

    def resizeEvent(self, e: QResizeEvent):
        self.closeButton.move(self.width() - 57, 0)
        self.maxButton.move(self.width() - 2 * 57, 0)
        self.minButton.move(self.width() - 3 * 57, 0)

    def mouseDoubleClickEvent(self, event):
        self.__showRestoreWindow()

    def mousePressEvent(self, event):
        """ 移动窗口 """
        if not self.__isPointInDragRegion(event.pos()):
            return

        ReleaseCapture()
        SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                    win32con.SC_MOVE + win32con.HTCAPTION, 0)
        event.ignore()

    def __showRestoreWindow(self):
        """ 复原窗口并更换最大化按钮的图标 """
        if self.window().isMaximized():
            self.window().showNormal()
            self.maxButton.setMaxState(False)
        else:
            self.window().showMaximized()
            self.maxButton.setMaxState(True)

    def __isPointInDragRegion(self, pos) -> bool:
        return 0 < pos.x() < self.width() - 57 * 3

    def __setQss(self):
        """ 设置层叠样式 """
        self.minButton.setObjectName("minButton")
        self.maxButton.setObjectName("maxButton")
        self.closeButton.setObjectName("closeButton")

        f = QFile(':/qss/title_bar.qss')
        f.open(QFile.ReadOnly)
        self.setStyleSheet(str(f.readAll(), encoding='utf-8'))
        f.close()
