# coding:utf-8
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QToolButton


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
