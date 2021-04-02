# coding:utf-8

from app.components.button import ThreeStateToolButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QPixmap, QResizeEvent
from PyQt5.QtWidgets import QLabel, QToolButton, QWidget
from win32.lib import win32con
from win32.win32api import SendMessage
from win32.win32gui import ReleaseCapture

from .title_bar_buttons import MaximizeButton


class TitleBar(QWidget):
    """ 定义标题栏 """

    def __init__(self, parent):
        super().__init__(parent)
        self.resize(700, 40)
        self.icon = QLabel(self)
        # 如果直接使用qss来画图标会糊掉
        self.minBt = ThreeStateToolButton(
            {'normal': r'app\resource\images\title_bar\最小化按钮_normal_57_40.png',
             'hover': r'app\resource\images\title_bar\最小化按钮_hover_57_40.png',
             'pressed': r'app\resource\images\title_bar\最小化按钮_pressed_57_40.png'}, (57, 40), self)
        self.closeBt = ThreeStateToolButton(
            {'normal': r'app\resource\images\title_bar\关闭按钮_normal_57_40.png',
             'hover': r'app\resource\images\title_bar\关闭按钮_hover_57_40.png',
             'pressed': r'app\resource\images\title_bar\关闭按钮_pressed_57_40.png'}, (57, 40), self)
        self.maxBt = MaximizeButton(self)
        self.title = QLabel('Alpha Gobang Zero', self)
        # 初始化界面
        self.__initWidget()
        self.__adjustButtonPos()

    def __initWidget(self):
        """ 初始化小部件 """
        self.setFixedHeight(40)
        self.icon.move(9, 9)
        self.title.move(34, 8)
        self.setAttribute(Qt.WA_StyledBackground)
        self.icon.setPixmap(QPixmap(r'app\resource\images\icon\二哈.png').scaled(
            20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # 设置层叠样式
        self.__setQss()
        # 将按钮的点击信号连接到槽函数
        self.minBt.clicked.connect(self.window().showMinimized)
        self.maxBt.clicked.connect(self.__showRestoreWindow)
        self.closeBt.clicked.connect(self.window().close)

    def __adjustButtonPos(self):
        """ 初始化小部件位置 """
        self.closeBt.move(self.width() - 57, 0)
        self.maxBt.move(self.width() - 2 * 57, 0)
        self.minBt.move(self.width() - 3 * 57, 0)

    def resizeEvent(self, e: QResizeEvent):
        """ 尺寸改变时移动按钮 """
        self.__adjustButtonPos()

    def mouseDoubleClickEvent(self, event):
        """ 双击最大化窗口 """
        self.__showRestoreWindow()

    def mousePressEvent(self, event):
        """ 移动窗口 """
        # 判断鼠标点击位置是否允许拖动
        if self.__isPointInDragRegion(event.pos()):
            ReleaseCapture()
            SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                        win32con.SC_MOVE + win32con.HTCAPTION, 0)
            event.ignore()

    def __showRestoreWindow(self):
        """ 复原窗口并更换最大化按钮的图标 """
        if self.window().isMaximized():
            self.window().showNormal()
            # 更新标志位用于更换图标
            self.maxBt.setMaxState(False)
        else:
            self.window().showMaximized()
            self.maxBt.setMaxState(True)

    def __isPointInDragRegion(self, pos) -> bool:
        """ 检查鼠标按下的点是否属于允许拖动的区域 """
        x = pos.x()
        # 如果最小化按钮看不见也意味着最大化按钮看不见
        right = self.width() - 57 * 3 if self.minBt.isVisible() else self.width() - 57
        return (0 < x < right)


    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'app\resource\qss\title_bar.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
