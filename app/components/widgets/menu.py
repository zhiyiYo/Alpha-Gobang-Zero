# coding:utf-8
from app.common.icon import Icon
from app.common.windoweffect import WindowEffect
from PyQt5.QtCore import (QEasingCurve, QEvent, QFile, QPropertyAnimation,
                          QRect, Qt)
from PyQt5.QtWidgets import QAction, QApplication, QMenu


class ChessBoardMenu(QMenu):
    """ 棋盘右击菜单 """

    def __init__(self, parent):
        super().__init__('', parent)
        self.windowEffect = WindowEffect()
        self.animation = QPropertyAnimation(self, b'geometry')
        # 创建动作
        self.restartGameAct = QAction(
            Icon(':/images/chess_board_interface/重新开始.png'), self.tr('Restart'), self)
        self.settingAct = QAction(
            Icon(':/images/chess_board_interface/设置.png'), self.tr('Settings'), self)
        self.action_list = [self.restartGameAct, self.settingAct]
        self.addActions(self.action_list)
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.setWindowFlags(self.windowFlags() | Qt.NoDropShadowWindowHint)
        self.windowEffect.addShadowEffect(self.winId())
        self.__setQss()

    def event(self, e: QEvent):
        if e.type() == QEvent.WinIdChange:
            self.windowEffect.addShadowEffect(self.winId())
        return QMenu.event(self, e)

    def exec_(self, pos):
        w = max(self.fontMetrics().width(i.text()) for i in self.actions())+70
        actionNum = len(self.action_list)

        # 每个item的高度为38px，10为上下的内边距和
        h = actionNum * 38 + 10

        # 设置动画
        self.animation.setStartValue(QRect(pos.x(), pos.y(), 1, h))
        self.animation.setEndValue(QRect(pos.x(), pos.y(), w, h))
        self.setStyle(QApplication.style())

        # 开始动画
        self.animation.start()
        super().exec_(pos)

    def __setQss(self):
        """ 设置层叠样式 """
        f = QFile(':/qss/menu.qss')
        f.open(QFile.ReadOnly)
        self.setStyleSheet(str(f.readAll(), encoding='utf-8'))
        f.close()
