# coding: utf-8
from app.common import resource
from app.components.framelesswindow import FramelessWindow
from app.components.widgets.pop_up_ani_stacked_widget import PopUpAniStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWinExtras import QtWin
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
        self.resize(750, 850)
        self.setMinimumSize(700, 790)
        self.setObjectName("mainWindow")
        self.setWindowTitle('Alpha Gobang Zero')
        self.setWindowIcon(QIcon(':/images/icon/二哈.png'))
        QtWin.enableBlurBehindWindow(self)
        self.setWindowFlags(Qt.FramelessWindowHint |
                            Qt.WindowMinMaxButtonsHint)
        self.windowEffect.addWindowAnimation(self.winId())
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
        # 设置窗口特效
        self.setWindowEffect(self.settingInterface.config["is_enable_acrylic"])

    def connectSignalToSlot(self):
        """ 信号连接到槽 """
        self.settingInterface.enableAcrylicChanged.connect(
            self.setWindowEffect)
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
        self.navigationInterface.switchInterface('Chess board')

    def switchToSettingInterface(self):
        """ 切换到设置界面 """
        self.stackedWidget.setCurrentWidget(self.settingInterface, False)
        self.navigationInterface.switchInterface('Settings')

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

    def setWindowEffect(self, isEnableAcrylic: bool):
        """ 设置窗口特效 """
        if isEnableAcrylic:
            self.windowEffect.setAcrylicEffect(self.winId(), "F2F2F2F2", True)
            self.setStyleSheet("#mainWindow{background:transparent}")
        else:
            self.setStyleSheet("#mainWindow{background:#F0F0F0}")
            self.windowEffect.addShadowEffect(self.winId())
            self.windowEffect.removeBackgroundEffect(self.winId())
