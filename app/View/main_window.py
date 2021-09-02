# coding: utf-8
from app.common import resource
from app.components.framelesswindow import FramelessWindow
from app.components.widgets.pop_up_ani_stacked_widget import PopUpAniStackedWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, qApp

from .chess_board_interface import ChessBoardInterface
from .navigation_interface import NavigationInterface
from .setting_interface import SettingInterface


class MainWindow(FramelessWindow):
    """ 主界面 """

    def __init__(self):
        super().__init__(parent=None)
        self.boardLen = 9
        self.navigationInterface = NavigationInterface(self)
        self.settingInterface = SettingInterface()
        self.chessBoardInterface = ChessBoardInterface(
            **self.settingInterface.config)
        self.stackedWidget = PopUpAniStackedWidget(self)
        # 初始化
        self.initWidget()

    def initWidget(self):
        """ 初始化界面 """
        # 设置窗口大小
        self.resize(750, 850)
        self.setMinimumSize(700, 790)
        self.setWindowTitle('Alpha Gobang Zero')
        self.setWindowIcon(QIcon(':/images/icon/二哈.png'))
        self.navigationInterface.move(0, 40)
        self.stackedWidget.resize(750, 760)
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
        self.chessBoardInterface.switchToSettingInterfaceSignal.connect(
            self.switchToSettingInterface)
        self.navigationInterface.switchToChessBoardInterfaceSig.connect(
            self.switchToChessBoardInterface)
        self.navigationInterface.switchToSettingInterfaceSig.connect(
            self.switchToSettingInterface)

    def closeEvent(self, e):
        self.settingInterface.saveConfig()
        self.chessBoardInterface.close()
        e.accept()

    def exitGame(self):
        """ 退出游戏 """
        self.settingInterface.saveConfig()
        qApp.exit()

    def switchToChessBoardInterface(self):
        """ 切换到棋盘界面 """
        self.stackedWidget.setCurrentWidget(
            self.chessBoardInterface, True, False)

    def switchToSettingInterface(self):
        """ 切换到设置界面 """
        self.stackedWidget.setCurrentWidget(self.settingInterface, False)
        if self.sender() is self.chessBoardInterface:
            self.navigationInterface.navigationMenu.setSelectedButton(1)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.stackedWidget.resize(self.width(), self.height()-90)
        self.navigationInterface.resize(
            self.navigationInterface.width(), self.height()-40)
        self.centerChessboard()

    def updateGameConfig(self):
        """ 更新游戏配置 """
        self.chessBoardInterface.updateGameConfig(self.settingInterface.config)

    def centerChessboard(self):
        """ 居中棋盘 """
        self.chessBoardInterface.move(
            (self.width()-self.chessBoardInterface.width())//2,
            (self.height()-self.chessBoardInterface.height())//2-45)
