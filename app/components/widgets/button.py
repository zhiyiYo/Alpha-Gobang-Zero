# coding:utf-8
from app.common.icon import Icon
from PyQt5.QtCore import QFile, QSize, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import QPushButton, QToolButton


class ThreeStateToolButton(QToolButton):

    def __init__(self, iconPaths: dict, icon_size: tuple = (50, 50), parent=None):
        super().__init__(parent)
        self.iconPaths = iconPaths
        self.resize(*icon_size)
        self.initWidget()

    def initWidget(self):
        """ 初始化小部件 """
        self.setCursor(Qt.ArrowCursor)
        self.setIcon(Icon(self.iconPaths['normal']))
        self.setIconSize(QSize(self.width(), self.height()))
        self.setStyleSheet('border: none; margin: 0px')

    def enterEvent(self, e):
        self.setIcon(Icon(self.iconPaths['hover']))

    def leaveEvent(self, e):
        self.setIcon(Icon(self.iconPaths['normal']))

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            return
        self.setIcon(Icon(self.iconPaths['pressed']))
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.RightButton:
            return

        self.setIcon(Icon(self.iconPaths['normal']))
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
        self.__setQss()
        self.setFixedSize(320, 50)

    def setSelected(self, isSelected: bool):
        """ 设置按钮选中状态 """
        self.__isSelected = isSelected
        self.update()

    def paintEvent(self, e):
        """ 绘制按钮 """
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.Antialiasing |
            QPainter.SmoothPixmapTransform |
            QPainter.TextAntialiasing
        )
        painter.setPen(Qt.NoPen)

        # 绘制图标
        painter.drawPixmap(15, 15, self.__iconPixmap)

        # 绘制文本
        painter.setPen(QPen(Qt.black))
        painter.setFont(self.font())
        painter.drawText(50, 15 + 16, self.__text)

        # 绘制选中标志
        if self.__isSelected:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor(0, 153, 188)))
            painter.drawRoundedRect(5, 10, 3, 30, 2, 2)

    def __setQss(self):
        """ 设置层叠样式 """
        f = QFile(':/qss/navigation_button.qss')
        f.open(QFile.ReadOnly)
        self.setStyleSheet(str(f.readAll(), encoding='utf-8'))
        f.close()
