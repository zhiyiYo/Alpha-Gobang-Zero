# coding:utf-8
from app.common.auto_wrap import autoWrap
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPen
from PyQt5.QtWidgets import (QGraphicsDropShadowEffect, QLabel, QPushButton,
                             QWidget)

from .sub_panel_frame import SubPanelFrame


class ContinueGameDialog(SubPanelFrame):
    """ 创建播放列表面板 """

    def __init__(self, title: str, content: str, parent=None):
        """
        Parameters
        ----------
        title: str
            对话框标题

        content: str
            对话框内容

        parent:
            父级窗口
        """
        super().__init__(parent)
        # 实例化子属性面板
        self.__subPanel = SubContinueGameDialog(title, content, self)
        self.continueGameSignal = self.__subPanel.continueGameSignal
        self.exitGameSignal = self.__subPanel.exitGameSignal
        # 初始化
        self.showMask()
        self.__setSubWindowPos()

    def __setSubWindowPos(self):
        """ 设置子窗口的位置 """
        self.__subPanel.move(
            int(self.width() / 2 - self.__subPanel.width() / 2),
            int(self.height() / 2 - self.__subPanel.height() / 2),
        )


class SubContinueGameDialog(QWidget):
    """ 是否继续游戏对话框 """

    continueGameSignal = pyqtSignal()
    exitGameSignal = pyqtSignal()

    def __init__(self, title: str, content: str, parent):
        super().__init__(parent)
        # 创建小部件
        self.yesButton = QPushButton("来啦老弟", self)
        self.cancelButton = QPushButton("拒绝", self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content, self)
        # 初始化
        self.__initWidgets()

    def __initWidgets(self):
        """ 初始化小部件 """
        self.setFixedHeight(230)
        self.setAttribute(Qt.WA_StyledBackground)
        self.__setShadowEffect()
        # 根据标签的宽度调整宽度
        self.__adjustWidth()
        self.yesButton.resize(int((self.width() - 62 - 6) / 2), 40)
        self.cancelButton.resize(self.yesButton.width(), 40)
        # 调整位置
        self.titleLabel.move(31, 29)
        self.contentLabel.move(31, 70)
        self.yesButton.move(31, 159)
        self.cancelButton.move(
            self.width() - self.cancelButton.width() - 31, 159)
        # 设置层叠样式
        self.setObjectName("subPanel")
        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")
        self.__setQss()
        # 信号连接到槽
        self.yesButton.clicked.connect(self.__continueGameSlot)
        self.cancelButton.clicked.connect(self.__exitGameSlot)

    def __adjustWidth(self):
        """ 调整宽度 """
        newText, isWrap = autoWrap(self.contentLabel.text(), 72)
        if isWrap:
            self.setFixedWidth(682)
            self.contentLabel.setText(newText)
            self.contentLabel.setFixedHeight(50)
        else:
            fontMetrics = QFontMetrics(QFont("Microsoft YaHei", 11))
            self.setFixedWidth(fontMetrics.width(
                self.contentLabel.text()) + 62)

    def __setShadowEffect(self):
        """ 添加阴影 """
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(60)
        self.shadowEffect.setOffset(0, 5)
        self.setGraphicsEffect(self.shadowEffect)

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r"app\resource\qss\continue_game_dialog.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def paintEvent(self, e):
        """ 绘制背景和阴影 """
        # 创建画笔
        painter = QPainter(self)
        # 绘制边框
        pen = QPen(QColor(175, 175, 175))
        painter.setPen(pen)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    def __continueGameSlot(self):
        """ 发送删除专辑卡信号 """
        self.parent().close()
        self.continueGameSignal.emit()
        self.parent().deleteLater()

    def __exitGameSlot(self):
        """ 退出游戏槽函数 """
        self.parent().deleteLater()
        self.exitGameSignal.emit()
