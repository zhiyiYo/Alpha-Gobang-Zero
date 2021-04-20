# coding:utf-8
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QIcon, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QPushButton, QToolButton


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


class NavigationButton(QPushButton):
    """ 导航按钮 """

    def __init__(self, text: str, iconPath: str, isSelected=False, parent=None):
        """
        Parameters
        ----------
        text: str
            按钮文本

        iconPath: str
            图标路径

        isSelected: bool
            是否处于选中状态

        parent:
            父级窗口
        """
        super().__init__(parent=parent)
        self.__iconPixmap = QPixmap(iconPath)
        self.__isSelected = isSelected
        self.__text = text
        self.setFixedSize(320, 50)
        self.__setQss()

    def setSelected(self, isSelected: bool):
        """ 设置按钮选中状态 """
        self.__isSelected = isSelected
        self.update()

    def paintEvent(self, e):
        """ 绘制按钮 """
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        # 绘制图标
        painter.drawPixmap(15, 15, self.__iconPixmap)
        # 绘制文本
        painter.setPen(QPen(Qt.black))
        painter.setFont(QFont("Microsoft YaHei", 11, 25))
        painter.drawText(50, 15 + 16, self.__text)
        # 绘制选中标志
        if self.__isSelected:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(0, 153, 188)))
            painter.drawRoundedRect(5, 10, 3, 30, 2, 2)

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'app\resource\qss\navigation_button.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
