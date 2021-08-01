# coding:utf-8
import os

from app.common.model_utils import testModel
from app.components.dialogs.dialog import Dialog
from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import (QFileDialog, QGraphicsDropShadowEffect, QLabel,
                             QPushButton, QWidget,QDialog,QGraphicsOpacityEffect)

from .folding_window import FoldingWindow
from .model_card import ModelCard


class SelectModelDialog(QDialog):
    """ 选择模型对话框 """

    modelChangedSignal = pyqtSignal(str)

    def __init__(self, selectedModel: str, parent):
        super().__init__(parent=parent)
        self.selectedModel = selectedModel
        self.windowMask = QWidget(self)
        self.widget = QWidget(self)
        self.addModelCard = AddModelCard(self.widget)
        self.completeButton = QPushButton("完成", self.widget)
        self.titleLabel = QLabel('从本地模型库选择阿尔法狗', self.widget)
        self.subTitleLabel = QLabel('当前未使用任何模型', self.widget)
        if self.selectedModel:
            tip = '' if testModel(selectedModel) else '(模型不可用)'
            self.subTitleLabel.setText("现在我们正在使用这个模型"+tip)
            self.modelCard = ModelCard(self.selectedModel, self.widget)
            self.modelCard.clicked.connect(self.showDeleteModelPanel)
        else:
            self.modelCard = None
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.__setShadowEffect()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.windowMask.resize(self.size())
        self.__initLayout()
        self.__setQss()
        # 信号连接到槽
        self.addModelCard.clicked.connect(self.showFileDialog)
        self.completeButton.clicked.connect(self.updateModel)

    def __initLayout(self):
        """ 初始化布局 """
        self.widget.setFixedSize(440, 324)
        self.titleLabel.move(31, 31)
        self.addModelCard.move(36, 130)
        self.completeButton.move(223, self.widget.height() - 71)
        self.subTitleLabel.move(31, 79)
        if self.modelCard:
            self.modelCard.move(36, 130)
            self.addModelCard.hide()
        self.widget.move(self.width()//2 - self.widget.width()//2,
                         self.height()//2 - self.widget.height()//2)

    def __setShadowEffect(self):
        """ 添加阴影 """
        shadowEffect = QGraphicsDropShadowEffect(self.widget)
        shadowEffect.setBlurRadius(50)
        shadowEffect.setOffset(0, 5)
        self.widget.setGraphicsEffect(shadowEffect)

    def showDeleteModelPanel(self):
        """ 显示删除模型对话框 """
        content = f'如果将"{os.path.basename(self.selectedModel)}"从模型中移除，则该模型文件不会再被使用，但不会被删除。'
        deleteModelDialog = Dialog('删除此模型吗？', content, self.window())
        deleteModelDialog.yesSignal.connect(self.deleteModelFolder)
        deleteModelDialog.exec_()

    def deleteModelFolder(self):
        """ 删除选中的模型卡 """
        self.sender().deleteLater()
        self.modelCard.deleteLater()
        self.subTitleLabel.setText('当前未使用任何模型')
        self.addModelCard.show()
        self.selectedModel = None

    def showFileDialog(self):
        """ 定时器溢出时显示文件对话框 """
        path, _ = QFileDialog.getOpenFileName(
            self, "选择模型", "./model", '模型文件 (*.pth; *.pt; *.pkl);;所有文件 (*.*)')
        if path:
            self.addModelCard.hide()
            # 检验模型是否可用
            isModelOk = testModel(path)
            path = path.replace("/", "\\")
            self.modelCard = ModelCard(path, self.widget)
            self.modelCard.move(36, 130)
            self.modelCard.clicked.connect(self.showDeleteModelPanel)
            self.selectedModel = path
            # 设置提示并根据模型是否可用来设置按钮可用性
            tip = '' if isModelOk else '(模型不可用)'
            self.subTitleLabel.setText("现在我们正在使用这个模型" + tip)
            self.subTitleLabel.adjustSize()
            self.completeButton.setEnabled(isModelOk)

    def updateModel(self):
        """ 更新选中的模型 """
        # 保存设置后禁用窗口
        self.setEnabled(False)
        self.modelChangedSignal.emit(self.selectedModel)
        self.deleteLater()

    def __setQss(self):
        """ 设置层叠样式 """
        self.windowMask.setObjectName('windowMask')
        self.titleLabel.setObjectName('titleLabel')
        self.subTitleLabel.setObjectName("subTitleLabel")
        with open(r'app\resource\qss\select_model_dialog.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def showEvent(self, e):
        """ 淡入 """
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(0)
        opacityAni.setEndValue(1)
        opacityAni.setDuration(200)
        opacityAni.setEasingCurve(QEasingCurve.InSine)
        opacityAni.finished.connect(opacityEffect.deleteLater)
        opacityAni.start()
        super().showEvent(e)

    def closeEvent(self, e):
        """ 淡出 """
        self.widget.setGraphicsEffect(None)
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(1)
        opacityAni.setEndValue(0)
        opacityAni.setDuration(100)
        opacityAni.setEasingCurve(QEasingCurve.OutCubic)
        opacityAni.finished.connect(self.deleteLater)
        opacityAni.start()
        e.ignore()


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
