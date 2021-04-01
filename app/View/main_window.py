# coding: utf-8

from app.components.framelesswindow import FramelessWindow
from app.components.pop_up_ani_stacked_widget import PopUpAniStackedWidget
from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, qApp

from .chess_board_interface import ChessBoardInterface
from .navigation_interface import NavigationInterface
from .settinginterface import SettingInterface


class MainWindow(FramelessWindow):
    """ 主界面 """

    updateGameConfigSignal = pyqtSignal(dict)

    def __init__(self):
        super().__init__(parent=None)
        self.boardLen = 9
        self.settingInterface = SettingInterface()
        self.chessBoardInterface = ChessBoardInterface(
            **self.settingInterface.config)
        self.stackedWidget = PopUpAniStackedWidget(self)
        self.navigationInterface = NavigationInterface(self)
        # 初始化
        self.initWidget()

    def initWidget(self):
        """ 初始化界面 """
        self.setFixedSize(700, 790)
        self.navigationInterface.move(0, 40)
        self.stackedWidget.resize(700, 700)
        self.stackedWidget.move(0, 90)
        # 子窗口添加到层叠窗口中
        self.stackedWidget.addWidget(
            self.chessBoardInterface, 0, 0, isNeedOpacityAni=False)
        self.stackedWidget.addWidget(
            self.settingInterface, 0, 120, isNeedOpacityAni=False)
        # 在去除任务栏的显示区域居中显示
        desktop = QApplication.desktop().availableGeometry()
        self.move(
            int(desktop.width() / 2 - self.width() / 2),
            int(desktop.height() / 2 - self.height() / 2),
        )
        # 信号连接到槽
        self.connectSignalToSlot()

    def connectSignalToSlot(self):
        """ 信号连接到槽 """
        self.chessBoardInterface.exitGameSignal.connect(self.exitGame)
        self.chessBoardInterface.restartGameSignal.connect(
            self.updateGameConfig)
        self.navigationInterface.switchToChessBoardInterfaceSig.connect(
            self.switchToChessBoardInterface)
        self.navigationInterface.switchToSettingInterfaceSig.connect(
            self.switchToSettingInterface)
        self.updateGameConfigSignal.connect(
            self.chessBoardInterface.updateGameConfig)

    def closeEvent(self, e):
        self.settingInterface.saveConfig()
        e.accept()

    def exitGame(self):
        """ 退出游戏 """
        self.settingInterface.saveConfig()
        qApp.exit()

    def switchToChessBoardInterface(self):
        """ 切换到棋盘界面 """
        self.stackedWidget.setCurrentWidget(self.chessBoardInterface, True)

    def switchToSettingInterface(self):
        """ 切换到设置界面 """
        self.stackedWidget.setCurrentWidget(self.settingInterface, False)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.stackedWidget.resize(self.width(), self.height()-90)
        self.navigationInterface.resize(
            self.navigationInterface.width(), self.height()-40)

    def updateGameConfig(self):
        """ 更新游戏配置 """
        self.updateGameConfigSignal.emit(self.settingInterface.config)
