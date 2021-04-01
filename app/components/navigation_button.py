# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QBrush, QColor, QPainter, QPixmap,QFont
from PyQt5.QtWidgets import QPushButton


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
            painter.drawRoundedRect(5, 10, 3, 30, 1, 1)

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'app\resource\qss\navigation_button.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
