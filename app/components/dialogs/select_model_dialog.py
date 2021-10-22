# coding:utf-8
import os

from app.common.get_pressed_pos import getPressedPos
from app.common.model_utils import testModel
from PyQt5.QtCore import QFile, QPoint, Qt, pyqtSignal
from PyQt5.QtGui import (QBrush, QColor, QFont, QFontMetrics, QMouseEvent,
                         QPainter, QPen, QPixmap, QPolygon)
from PyQt5.QtWidgets import QFileDialog, QLabel, QPushButton, QWidget

from .dialog import Dialog
from .mask_dialog_base import MaskDialogBase


class SelectModelDialog(MaskDialogBase):
    """ 选择模型对话框 """

    modelChangedSignal = pyqtSignal(str)

    def __init__(self, selectedModel: str, parent):
        super().__init__(parent=parent)
        self.selectedModel = selectedModel
        self.windowMask = QWidget(self)
        self.addModelCard = AddModelCard(self.widget)
        self.completeButton = QPushButton(self.tr("Done"), self.widget)
        self.titleLabel = QLabel(
            self.tr('Select Alpha Gobang from local model library'), self.widget)
        self.contentLabel = QLabel(
            self.tr('No model is used currently'), self.widget)

        if self.selectedModel:
            tip = '' if testModel(selectedModel) else self.tr(
                ' (model is not available) ')
            self.contentLabel.setText(
                self.tr("Now we are using this model")+tip)
            self.modelCard = ModelCard(self.selectedModel, self.widget)
            self.modelCard.clicked.connect(self.showDeleteModelPanel)
        else:
            self.modelCard = None

        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.__setQss()
        self.__initLayout()

        # 信号连接到槽
        self.addModelCard.clicked.connect(self.showFileDialog)
        self.completeButton.clicked.connect(self.updateModel)

    def __initLayout(self):
        """ 初始化布局 """
        w = max(440, self.contentLabel.width()+60, self.titleLabel.width()+60)
        self.widget.setFixedSize(w, 324)

        self.titleLabel.move(31, 31)
        self.contentLabel.move(31, 79)

        self.__adjustWidgetsPos()

    def showDeleteModelPanel(self):
        """ 显示删除模型对话框 """
        title = self.tr('Delete this model?')
        content = self.tr('If you remove')+f' "{os.path.basename(self.selectedModel)}" ' + \
            self.tr("the model will no longer appear in the list"
                    ", but will not be deleted.")
        deleteModelDialog = Dialog(title, content, self.window())
        deleteModelDialog.yesSignal.connect(self.deleteModelFolder)
        deleteModelDialog.exec_()

    def deleteModelFolder(self):
        """ 删除选中的模型卡 """
        self.sender().deleteLater()
        self.modelCard.deleteLater()
        self.contentLabel.setText(self.tr('No model is used currently'))
        self.addModelCard.show()
        self.selectedModel = None
        self.modelCard = None
        self.__adjustWidgetsPos()

    def showFileDialog(self):
        """ 定时器溢出时显示文件对话框 """
        path, _ = QFileDialog.getOpenFileName(self, self.tr("Select model"), "./model", self.tr(
            'Model file') + ' (*.pth; *.pt; *.pkl);;' + self.tr('All files') + ' (*.*)')

        if path:
            self.addModelCard.hide()

            # 检验模型是否可用
            isModelOk = testModel(path)
            path = path.replace("/", "\\")
            self.modelCard = ModelCard(path, self.widget)
            self.modelCard.clicked.connect(self.showDeleteModelPanel)
            self.selectedModel = path

            # 设置提示并根据模型是否可用来设置按钮可用性
            tip = '' if isModelOk else self.tr(' (model is not available) ')
            self.contentLabel.setText(
                self.tr("Now we are using this model") + tip)
            self.contentLabel.adjustSize()
            self.completeButton.setEnabled(isModelOk)

            self.__adjustWidgetsPos()

    def updateModel(self):
        """ 更新选中的模型 """
        self.setEnabled(False)
        self.modelChangedSignal.emit(self.selectedModel)
        self.deleteLater()

    def __setQss(self):
        """ 设置层叠样式 """
        self.windowMask.setObjectName('windowMask')
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName("contentLabel")

        f = QFile(':/qss/select_model_dialog.qss')
        f.open(QFile.ReadOnly)
        self.setStyleSheet(str(f.readAll(), encoding='utf-8'))
        f.close()

        self.titleLabel.adjustSize()
        self.contentLabel.adjustSize()
        self.completeButton.adjustSize()

    def __adjustWidgetsPos(self):
        """ 调整卡片位置 """
        w = max(440, self.contentLabel.width() +
                60, self.titleLabel.width()+60)
        self.widget.setFixedSize(w, 324)
        self.completeButton.move(
            w-30-self.completeButton.width(), self.widget.height() - 71)

        self.addModelCard.move((w-365)//2, 130)
        if self.modelCard:
            self.modelCard.move((w-365)//2, 130)
            self.addModelCard.hide()


class FoldingWindow(QWidget):
    """ 点击不同方位翻折效果不同的窗口 """

    # 创建点击信号
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(365, 90)
        # 设置标志位
        self.pressedPos = None
        self.isEnter = False

    def enterEvent(self, e):
        """ 鼠标进入界面就置位进入标志位 """
        self.isEnter = True
        self.update()

    def leaveEvent(self, e):
        """ 鼠标离开就清零置位标志位 """
        self.isEnter = False
        self.update()

    def mouseReleaseEvent(self, e):
        """ 鼠标松开时更新界面 """
        self.pressedPos = None
        self.update()
        if e.button() == Qt.LeftButton:
            self.clicked.emit()

    def mousePressEvent(self, e: QMouseEvent):
        """ 根据鼠标的不同按下位置更新标志位 """
        self.pressedPos = getPressedPos(self, e)
        self.update()

    def paintEvent(self, e):
        """ 根据不同的情况绘制不同的背景 """
        # super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        brush = QBrush(QColor(204, 204, 204))
        painter.setPen(Qt.NoPen)
        if not self.isEnter:
            painter.setBrush(brush)
            painter.drawRoundedRect(self.rect(), 5, 5)
        else:
            painter.setPen(QPen(QColor(204, 204, 204), 2))
            painter.drawRect(1, 1, self.width() - 2, self.height() - 2)
            painter.setPen(Qt.NoPen)
            if not self.pressedPos:
                brush.setColor(QColor(230, 230, 230))
                painter.setBrush(brush)
                painter.drawRect(2, 2, self.width() - 4, self.height() - 4)
            else:
                brush.setColor(QColor(153, 153, 153))
                painter.setBrush(brush)
                # 左上角
                if self.pressedPos == "left-top":
                    points = [
                        QPoint(6, 2),
                        QPoint(self.width() - 1, 1),
                        QPoint(self.width() - 1, self.height() - 1),
                        QPoint(1, self.height() - 1),
                    ]
                    painter.drawPolygon(QPolygon(points), 4)
                # 左边
                elif self.pressedPos == "left":
                    painter.drawRoundedRect(
                        6, 1, self.width() - 7, self.height() - 2, 3, 3
                    )
                # 左下角
                elif self.pressedPos == "left-bottom":
                    points = [
                        QPoint(1, 1),
                        QPoint(self.width() - 1, 1),
                        QPoint(self.width() - 1, self.height() - 1),
                        QPoint(6, self.height() - 2),
                    ]
                    painter.drawPolygon(QPolygon(points), 4)
                # 顶部
                elif self.pressedPos == "top":
                    points = [
                        QPoint(6, 2),
                        QPoint(self.width() - 6, 2),
                        QPoint(self.width() - 1, self.height() - 1),
                        QPoint(1, self.height() - 1),
                    ]
                    painter.drawPolygon(QPolygon(points), 4)
                # 中间
                elif self.pressedPos == "center":
                    painter.drawRoundedRect(
                        6, 1, self.width() - 12, self.height() - 2, 3, 3
                    )
                # 底部
                elif self.pressedPos == "bottom":
                    points = [
                        QPoint(1, 1),
                        QPoint(self.width() - 1, 1),
                        QPoint(self.width() - 6, self.height() - 2),
                        QPoint(6, self.height() - 2),
                    ]
                    painter.drawPolygon(QPolygon(points), 4)
                # 右上角
                elif self.pressedPos == "right-top":
                    points = [
                        QPoint(1, 1),
                        QPoint(self.width() - 6, 2),
                        QPoint(self.width() - 1, self.height() - 1),
                        QPoint(1, self.height() - 1),
                    ]
                    painter.drawPolygon(QPolygon(points), 4)
                # 右边
                elif self.pressedPos == "right":
                    painter.drawRoundedRect(
                        1, 1, self.width() - 7, self.height() - 2, 3, 3
                    )
                # 右下角
                elif self.pressedPos == "right-bottom":
                    points = [
                        QPoint(1, 1),
                        QPoint(self.width() - 1, 1),
                        QPoint(self.width() - 6, self.height() - 2),
                        QPoint(1, self.height() - 1),
                    ]
                    painter.drawPolygon(QPolygon(points), 4)


class ModelCard(FoldingWindow):
    """ 显示当前使用的模型 """

    def __init__(self, modelPath: str, parent=None):
        super().__init__(parent)
        self.modelPath = modelPath
        self.modelName = os.path.split(modelPath)[-1]
        self.image = QPixmap(":/images/setting_interface/黑色叉号.png")
        self.show()

    def paintEvent(self, e):
        """ 绘制背景 """
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform
        )
        # 绘制文字
        if self.pressedPos in ["left-top", "top", "right-bottom"]:
            # 左右扭曲字体
            painter.shear(-0.05, 0)
            self.paintText(painter, 14, 10, 15, 9)
        elif self.pressedPos in ["left", "center", "right"]:
            self.paintText(painter, 15, 10, 15, 9)
        elif self.pressedPos in ["left-bottom", "bottom", "right-top"]:
            painter.shear(0.05, 0)
            self.paintText(painter, 12, 10, 12, 9)
        else:
            self.paintText(painter, 12, 11, 12, 10)
        # 绘制叉号
        if self.pressedPos in ["left", "left-top", "left-bottom", "top", None]:
            painter.drawPixmap(
                self.width() - 30,
                25,
                self.image.width(),
                self.image.height(),
                self.image,
            )
        else:
            painter.drawPixmap(
                self.width() - 33,
                23,
                self.image.width(),
                self.image.height(),
                self.image,
            )

    def paintText(self, painter, x1, fontSize1, x2, fontSize2):
        """ 绘制文字 """
        # 绘制模型名字
        font = QFont("Microsoft YaHei", fontSize1, 75)
        painter.setFont(font)
        name = QFontMetrics(font).elidedText(
            self.modelName, Qt.ElideRight, self.width()-60)
        painter.drawText(x1, 37, name)
        # 绘制模型路径
        font = QFont("Microsoft YaHei", fontSize1)
        painter.setFont(font)
        path = QFontMetrics(font).elidedText(
            self.modelPath, Qt.ElideRight, self.width()-30)
        painter.drawText(x2, 46, self.width() - 20, 23, Qt.AlignLeft, path)


class AddModelCard(FoldingWindow):
    """ 点击选择模型 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QPixmap(":/images/setting_interface/黑色加号.png")

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
