# coding:utf-8

from app.common.auto_wrap import autoWrap
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPainter
from PyQt5.QtWidgets import (QDialog, QGraphicsDropShadowEffect, QLabel,
                             QPushButton, QWidget)


class DeleteModelDialog(QDialog):
    """ 删除模型对话框 """

    def __init__(self, modelName, parent):
        super().__init__(parent)
        self.subWindow = SubDeleteModelDialog(modelName, self)
        self.deleteButton = self.subWindow.deleteButton
        self.cancelButton = self.subWindow.cancelButton
        # 初始化
        self.initWidget()

    def initWidget(self):
        """ 初始化小部件 """
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.resize(self.subWindow.width() + 100,
                    self.subWindow.height() + 100)
        self.subWindow.move(
            int(self.width() / 2 - self.subWindow.width() / 2),
            int(self.height() / 2 - self.subWindow.height() / 2),
        )

    def exec_(self):
        self.move(
            int(self.parent().x() + self.parent().width() / 2 - self.width() / 2),
            int(self.parent().y() + self.parent().height() / 2 - self.height() / 2),
        )
        super().exec_()


class SubDeleteModelDialog(QWidget):
    """ 子删除模型对话框 """

    def __init__(self, modelName, parent):
        super().__init__(parent)
        self.modelName = modelName
        # 创建小部件
        self.createWidgets()
        # 初始化
        self.initLayout()
        self.initWidget()
        self.setQss()

    def createWidgets(self):
        """ 创建小部件 """
        self.titleLabel = QLabel("删除此模型吗？", self)
        self.subTitleLabel = QLabel("删除此模型吗？", self)
        self.contentLabel = QLabel(
            '如果将"' + self.modelName + '"从模型中移除，则该模型文件不会再被使用，但不会被删除。', self
        )
        self.deleteButton = QPushButton("删除模型", self)
        self.cancelButton = QPushButton("取消", self)

    def initWidget(self):
        """ 初始化小部件 """
        self.resize(550, 235)
        self.adjustHeight()
        self.setAttribute(Qt.WA_TranslucentBackground | Qt.WA_StyledBackground)
        self.setShadowEffect()
        # 初始化按钮
        self.deleteButton.resize(126, 40)
        self.cancelButton.resize(113, 40)
        # 信号连接到槽函数
        self.cancelButton.clicked.connect(self.parent().deleteLater)
        # 分配ID
        self.titleLabel.setObjectName("titleLabel")
        self.subTitleLabel.setObjectName("subTitleLabel")
        self.contentLabel.setObjectName("contentLabel")

    def initLayout(self):
        """ 初始化布局 """
        self.subTitleLabel.move(30, 67)
        self.contentLabel.move(30, 116)
        self.deleteButton.move(352, 167)
        self.cancelButton.move(508, 167)

    def setShadowEffect(self):
        """ 添加阴影 """
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(50)
        self.shadowEffect.setOffset(0, 5)
        self.setGraphicsEffect(self.shadowEffect)

    def adjustHeight(self):
        """ 调整长度 """
        newText, isWordWrap = autoWrap(self.contentLabel.text(), 68)
        if isWordWrap:
            self.resize(650, self.height() + 23)
            self.contentLabel.setText(newText)
            self.deleteButton.move(352, 190)
            self.cancelButton.move(508, 190)

    def paintEvent(self, e):
        """ 绘制背景 """
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)
        brush = QBrush(Qt.white)
        painter.setBrush(brush)
        painter.drawRect(self.rect())
        brush.setColor(QColor(0, 126, 153, 255))
        painter.setBrush(brush)
        painter.drawRect(0, 37, self.width(), self.height() - 37)
        super().paintEvent(e)

    def setQss(self):
        """ 设置层叠样式 """
        with open(r"app\resource\qss\delete_model_dialog.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
