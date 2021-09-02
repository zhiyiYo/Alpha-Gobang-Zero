# coding:utf-8

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolButton


class MaximizeButton(QToolButton):
    """ 最大化按钮 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.iconPathDict_list = [
            {'normal': ':/images/title_bar/最大化按钮_normal_57_40.png',
             'hover': ':/images/title_bar/最大化按钮_hover_57_40.png',
             'pressed': ':/images/title_bar/最大化按钮_pressed_57_40.png'},
            {'normal': ':/images/title_bar/向下还原按钮_normal_57_40.png',
             'hover': ':/images/title_bar/向下还原按钮_hover_57_40.png',
             'pressed': ':/images/title_bar/向下还原按钮_pressed_57_40.png'}
        ]
        self.resize(57, 40)
        # 设置标志位
        self.isMax = False
        self.setIcon(QIcon(':/images/title_bar/最大化按钮_normal_57_40.png'))
        self.setIconSize(QSize(57, 40))

    def __updateIcon(self, iconState: str):
        """ 更新图标 """
        self.setIcon(
            QIcon(self.iconPathDict_list[self.isMax][iconState]))

    def enterEvent(self, e):
        """ hover时更换图标 """
        self.__updateIcon('hover')

    def leaveEvent(self, e):
        """ leave时更换图标 """
        self.__updateIcon('normal')

    def mousePressEvent(self, e):
        """ 鼠标左键按下时更换图标 """
        if e.button() == Qt.RightButton:
            return
        self.__updateIcon('pressed')
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        """ 鼠标松开时更换按钮图标 """
        if e.button() == Qt.RightButton:
            return
        self.isMax = not self.isMax
        self.__updateIcon('normal')
        super().mouseReleaseEvent(e)

    def setMaxState(self, isMax: bool):
        """ 更新最大化标志位和图标 """
        if self.isMax == isMax:
            return
        self.isMax = isMax
        self.__updateIcon('normal')
