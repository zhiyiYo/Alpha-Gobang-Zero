# coding:utf-8
from app.common.windoweffect import WindowEffect
from app.components.widgets.button import NavigationButton
from PyQt5.QtCore import (QEasingCurve, QFile, QPoint, QPropertyAnimation,
                          QRect, Qt, pyqtSignal)
from PyQt5.QtGui import QColor, QIcon, QPainter, QPen
from PyQt5.QtWidgets import QApplication, QLabel, QToolButton, QWidget


class NavigationInterface(QWidget):

    switchToSettingInterfaceSig = pyqtSignal()
    switchToChessBoardInterfaceSig = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.title = QLabel(self.tr('Chess board'), self)
        self.navigationButton = QToolButton(self)
        self.navigationMenu = NavigationMenu(self)
        # 初始化界面
        self.__initWidget()

    def __initWidget(self):
        """ 初始化界面 """
        self.resize(320, 755)
        self.title.move(60, 7)
        self.navigationMenu.move(self.mapToGlobal(QPoint(0, 0)))
        self.navigationButton.setFixedSize(50, 50)
        self.navigationButton.setIcon(
            QIcon(':images/navigation_menu/显示导航菜单.png'))
        # 设置层叠样式
        self.__setQss()
        # 信号连接到槽
        self.__connectSignalToSlot()

    def __setQss(self):
        """ 设置层叠样式 """
        f = QFile(':/qss/navigation_interface.qss')
        f.open(QFile.ReadOnly)
        self.setStyleSheet(str(f.readAll(), encoding='utf-8'))
        f.close()

    def __connectSignalToSlot(self):
        """ 信号连接到槽 """
        self.navigationButton.clicked.connect(self.__showNavigationMenu)
        self.navigationMenu.navigationButton.clicked.connect(
            self.navigationMenu.aniHide)
        self.navigationMenu.boardButton.clicked.connect(
            self.__boardButtonClickedSlot)
        self.navigationMenu.settingButton.clicked.connect(
            self.__settingButtonClickedSlot)

    def __showNavigationMenu(self):
        """ 显示导航菜单 """
        self.navigationMenu.move(self.mapToGlobal(QPoint(0, 0)))
        self.navigationMenu.aniShow()

    def __boardButtonClickedSlot(self):
        """ 棋盘按钮点击槽函数 """
        self.navigationMenu.setSelectedButton(0)
        self.title.setText(self.tr('Chess board'))
        self.switchToChessBoardInterfaceSig.emit()
        self.navigationMenu.aniHide()
        self.navigationButton.setProperty('state', 'normal')
        self.title.adjustSize()
        self.setStyle(QApplication.style())

    def __settingButtonClickedSlot(self):
        """ 设置按钮点击槽函数 """
        self.navigationMenu.setSelectedButton(1)
        self.title.setText(self.tr('Settings'))
        self.switchToSettingInterfaceSig.emit()
        self.navigationMenu.aniHide()
        self.navigationButton.setProperty('state', 'normal')
        self.title.adjustSize()
        self.setStyle(QApplication.style())

    def resizeEvent(self, e):
        self.navigationMenu.resize(self.navigationMenu.width(), self.height())
        self.navigationMenu.settingButton.move(0, self.height()-60)


class NavigationMenu(QWidget):
    """ 导航菜单 """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 创建按钮
        self.navigationButton = QToolButton(self)
        self.boardButton = NavigationButton(
            self.tr('Chess board'), ':images/navigation_menu/棋盘.png', True, self)
        self.settingButton = NavigationButton(
            self.tr('Settings'), ':images/navigation_menu/设置.png', False, self)
        self.button_list = [self.boardButton, self.settingButton]
        # 实例化窗口特效和动画
        self.windowEffect = WindowEffect()
        self.__ani = QPropertyAnimation(self, b'geometry')
        # 初始化界面
        self.__initWidget()

    def __initWidget(self):
        """ 初始化界面 """
        self.resize(320, 755)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.NoDropShadowWindowHint | Qt.Popup)
        self.windowEffect.setAcrylicEffect(self.winId(), "E9ECED99", False)
        self.boardButton.move(0, 50)
        self.settingButton.move(0, self.height()-60)
        self.navigationButton.setFixedSize(50, 50)
        self.navigationButton.setIcon(
            QIcon(':images/navigation_menu/显示导航菜单.png'))

    def aniShow(self):
        """ 动画显示 """
        super().show()
        self.__ani.setStartValue(QRect(self.x(), self.y(), 50, self.height()))
        self.__ani.setEndValue(QRect(self.x(), self.y(), 320, self.height()))
        self.__ani.setEasingCurve(QEasingCurve.InOutQuad)
        self.__ani.setDuration(85)
        self.__ani.start()

    def aniHide(self):
        """ 动画隐藏 """
        self.__ani.setStartValue(QRect(self.x(), self.y(), 320, self.height()))
        self.__ani.setEndValue(QRect(self.x(), self.y(), 50, self.height()))
        self.__ani.finished.connect(self.__hideAniFinishedSlot)
        self.__ani.setDuration(85)
        self.__ani.start()

    def __hideAniFinishedSlot(self):
        """ 隐藏窗体的动画结束 """
        super().hide()
        self.resize(1, self.height())
        self.__ani.disconnect()

    def paintEvent(self, e):
        """ 绘制分隔符 """
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 0, 30))
        painter.setPen(pen)
        painter.drawLine(15, self.settingButton.y() - 1,
                         self.width() - 15, self.settingButton.y() - 1)

    def setSelectedButton(self, index: int):
        """ 设置选中的按钮 """
        for i, button in enumerate(self.button_list):
            button.setSelected(i == index)
