# coding:utf-8

import os

from app.common.model_utils import testModel
from app.components.sub_panel_frame import SubPanelFrame
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (QFileDialog, QGraphicsDropShadowEffect, QLabel,
                             QPushButton, QWidget)

from .delete_model_dialog import DeleteModelDialog
from .folding_window import FoldingWindow
from .model_card import ModelCard


class SelectModelDialog(SubPanelFrame):
    """ 选择歌曲文件夹面板 """

    def __init__(self, selectedModel: str, parent=None):
        """
        Parameters
        ----------
        selectedModel: str
            选中的模型文件路径

        parent:
            父级窗口
        """
        super().__init__(parent)
        # 实例化子属性面板
        self.__subDialog = SubSelectModelDialog(selectedModel, self)
        self.modelChangedSignal = self.__subDialog.modelChangedSignal
        # 初始化
        self.showMask()
        self.setSubWindowPos()

    def setSubWindowPos(self):
        """ 设置子窗口的位置 """
        self.__subDialog.move(
            int(self.width() / 2 - self.__subDialog.width() / 2),
            int(self.height() / 2 - self.__subDialog.height() / 2),
        )


class SubSelectModelDialog(QWidget):
    """ 子选择歌曲文件夹面板 """

    modelChangedSignal = pyqtSignal(str)  # 发送更新了的歌曲文件夹列表

    def __init__(self, selectedModel: str, parent):
        super().__init__(parent)
        self.selectedModel = selectedModel
        # 创建小部件
        self.selectModelTimer = QTimer(self)
        self.deleteModelTimer = QTimer(self)
        self.addModelCard = AddModelCard(self)
        self.completeButton = QPushButton("完成", self)
        self.titleLabel = QLabel('从本地模型库选择阿尔法狗', self)
        self.subTitleLabel = QLabel('当前未使用任何模型', self)
        if self.selectedModel:
            tip = '' if testModel(selectedModel) else '(模型不可用)'
            self.subTitleLabel.setText("现在我们正在使用这个模型"+tip)
            self.modelCard = ModelCard(self.selectedModel, self)
            # 在显示删除文件卡对话框前加个延时
            self.modelCard.clicked.connect(self.deleteModelTimer.start)
        else:
            self.modelCard = None
        # 初始化
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.setFixedSize(440, 324)
        self.setAttribute(Qt.WA_StyledBackground)
        # 添加阴影
        self.setShadowEffect()
        # 初始化定时器
        self.selectModelTimer.setInterval(500)
        self.deleteModelTimer.setInterval(600)
        self.selectModelTimer.timeout.connect(self.showFileDialog)
        self.deleteModelTimer.timeout.connect(self.showDeleteModelPanel)
        # 将信号连接到槽函数
        self.addModelCard.clicked.connect(self.selectModelTimer.start)
        self.completeButton.clicked.connect(self.updateModel)
        # 分配ID
        self.setObjectName("father")
        self.titleLabel.setObjectName("titleLabel")
        self.subTitleLabel.setObjectName("subTitleLabel")
        self.__initLayout()
        self.__setQss()

    def __initLayout(self):
        """ 初始化布局 """
        self.titleLabel.move(31, 31)
        self.addModelCard.move(36, 130)
        self.completeButton.move(223, self.height() - 71)
        self.subTitleLabel.move(31, 79)
        if self.modelCard:
            self.modelCard.move(36, 130)
            self.addModelCard.hide()

    def showFileDialog(self):
        """ 定时器溢出时显示文件对话框 """
        self.selectModelTimer.stop()
        path, _ = QFileDialog.getOpenFileName(
            self, "选择模型", "./model", '模型文件 (*.pth; *.pt; *.pkl);;所有文件 (*.*)')
        if path:
            self.addModelCard.hide()
            # 检验模型是否可用
            isModelOk = testModel(path)
            path = path.replace("/", "\\")
            self.modelCard = ModelCard(path, self)
            self.modelCard.move(36, 130)
            self.modelCard.clicked.connect(self.deleteModelTimer.start)
            self.selectedModel = path
            # 设置提示并根据模型是否可用来设置按钮可用性
            tip = '' if isModelOk else '(模型不可用)'
            self.subTitleLabel.setText("现在我们正在使用这个模型" + tip)
            self.subTitleLabel.adjustSize()
            self.completeButton.setEnabled(isModelOk)

    def showDeleteModelPanel(self):
        """ 显示删除模型对话框 """
        self.deleteModelTimer.stop()
        self.deleteModelDialog = DeleteModelDialog(
            os.path.basename(self.selectedModel), self.window())
        self.deleteModelDialog.deleteButton.clicked.connect(
            self.deleteModelFolder)
        self.deleteModelDialog.exec_()

    def deleteModelFolder(self):
        """ 删除选中的模型卡 """
        self.deleteModelDialog.deleteLater()
        self.modelCard.deleteLater()
        self.subTitleLabel.setText('当前未使用任何模型')
        self.addModelCard.show()
        self.selectedModel = None

    def setShadowEffect(self):
        """ 添加阴影 """
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(60)
        self.shadowEffect.setOffset(0, 5)
        self.setGraphicsEffect(self.shadowEffect)

    def paintEvent(self, e):
        """ 绘制边框 """
        pen = QPen(QColor(172, 172, 172))
        pen.setWidth(2)
        painter = QPainter(self)
        painter.setPen(pen)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r"app\resource\qss\select_model_dialog.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def updateModel(self):
        """ 更新选中的模型 """
        # 保存设置后禁用窗口
        self.setEnabled(False)
        self.modelChangedSignal.emit(self.selectedModel)
        self.parent().deleteLater()


class AddModelCard(FoldingWindow):
    """ 点击选择模型 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QPixmap(r"app\resource\images\setting_interface\黑色加号.png")

    def paintEvent(self, e):
        """ 绘制背景 """
        super().paintEvent(e)
        painter = QPainter(self)
        if not self.pressedPos:
            painter.drawPixmap(
                int(self.width() / 2 - self.image.width() / 2),
                int(self.height() / 2 - self.image.height() / 2),
                self.image.width(),
                self.image.height(),
                self.image,
            )
        elif self.pressedPos in ["top", "bottom"]:
            painter.drawPixmap(
                int(self.width() / 2 - (self.image.width() - 2) / 2),
                int(self.height() / 2 - (self.image.height() - 4) / 2),
                self.image.width() - 2,
                self.image.height() - 4,
                self.image,
            )
        elif self.pressedPos in ["left", "right"]:
            painter.drawPixmap(
                int(self.width() / 2 - (self.image.width() - 4) / 2),
                int(self.height() / 2 - (self.image.height() - 2) / 2),
                self.image.width() - 4,
                self.image.height() - 2,
                self.image,
            )
        else:
            painter.drawPixmap(
                int(self.width() / 2 - (self.image.width() - 4) / 2),
                int(self.height() / 2 - (self.image.height() - 4) / 2),
                self.image.width() - 4,
                self.image.height() - 4,
                self.image,
            )
