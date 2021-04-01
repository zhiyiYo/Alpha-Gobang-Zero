# coding:utf-8

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QResizeEvent, QPixmap
from PyQt5.QtWidgets import QToolButton, QWidget, QLabel
from win32.lib import win32con
from win32.win32api import SendMessage
from win32.win32gui import ReleaseCapture


class ThreeStateToolButton(QToolButton):
    """ 三种状态对应三种图标的按钮，iconPath_dict提供按钮normal、hover、pressed三种状态下的图标地址 """

    def __init__(self, iconPath_dict: dict, icon_size: tuple = (50, 50), parent=None):
        super().__init__(parent)
        # 引用图标地址字典
        self.iconPath_dict = iconPath_dict
        self.resize(*icon_size)
        # 初始化小部件
        self.initWidget()

    def initWidget(self):
        """ 初始化小部件 """
        self.setCursor(Qt.ArrowCursor)
        self.setIcon(QIcon(self.iconPath_dict['normal']))
        self.setIconSize(QSize(self.width(), self.height()))
        self.setStyleSheet('border: none; margin: 0px')

    def enterEvent(self, e):
        """ hover时更换图标 """
        self.setIcon(QIcon(self.iconPath_dict['hover']))

    def leaveEvent(self, e):
        """ leave时更换图标 """
        self.setIcon(QIcon(self.iconPath_dict['normal']))

    def mousePressEvent(self, e):
        """ 鼠标左键按下时更换图标 """
        if e.button() == Qt.RightButton:
            return
        self.setIcon(QIcon(self.iconPath_dict['pressed']))
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """ 鼠标左键按下时更换图标 """
        if e.button() == Qt.RightButton:
            return
        self.setIcon(QIcon(self.iconPath_dict['normal']))
        super().mouseReleaseEvent(e)


class TitleBar(QWidget):
    """ 定义标题栏 """

    def __init__(self, parent):
        super().__init__(parent)
        self.resize(700, 40)
        self.title = QLabel('Alpha Gobang Zero', self)
        self.icon = QLabel(self)
        # 实例化小部件
        self.__createButtons()
        # 初始化界面
        self.__initWidget()
        self.__adjustButtonPos()

    def __createButtons(self):
        """ 创建各按钮 """
        self.minBt = ThreeStateToolButton(
            {'normal': r'app\resource\images\title_bar\透明黑色最小化按钮_57_40.png',
             'hover': r'app\resource\images\title_bar\绿色最小化按钮_hover_57_40.png',
             'pressed': r'app\resource\images\title_bar\黑色最小化按钮_pressed_57_40.png'}, (57, 40), self)
        self.closeBt = ThreeStateToolButton(
            {'normal': r'app\resource\images\title_bar\透明黑色关闭按钮_57_40.png',
             'hover': r'app\resource\images\title_bar\关闭按钮_hover_57_40.png',
             'pressed': r'app\resource\images\title_bar\关闭按钮_pressed_57_40.png'}, (57, 40), self)

    def __initWidget(self):
        """ 初始化小部件 """
        self.setFixedHeight(40)
        self.icon.move(9, 9)
        self.title.move(34, 8)
        self.setAttribute(Qt.WA_StyledBackground)
        self.icon.setPixmap(QPixmap(r'app\resource\images\icon\二哈.png').scaled(
            20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.__setQss()
        # 将按钮的点击信号连接到槽函数
        self.minBt.clicked.connect(self.window().showMinimized)
        self.closeBt.clicked.connect(self.window().close)

    def __adjustButtonPos(self):
        """ 初始化小部件位置 """
        self.closeBt.move(self.width() - 57, 0)
        self.minBt.move(self.width() - 2 * 57, 0)

    def resizeEvent(self, e: QResizeEvent):
        """ 尺寸改变时移动按钮 """
        self.__adjustButtonPos()

    def mousePressEvent(self, e):
        """ 移动窗口 """
        # 判断鼠标点击位置是否允许拖动
        if 0 < e.pos().x() < self.width() - 57 * 2:
            ReleaseCapture()
            SendMessage(self.window().winId(), win32con.WM_SYSCOMMAND,
                        win32con.SC_MOVE + win32con.HTCAPTION, 0)
            e.ignore()

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'app\resource\qss\title_bar.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
