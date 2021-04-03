# coding:utf-8

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap, QFont, QFontMetrics

from .folding_window import FoldingWindow


class ModelCard(FoldingWindow):
    """ 显示当前使用的模型 """

    def __init__(self, modelPath: str, parent=None):
        super().__init__(parent)
        self.modelPath = modelPath
        self.modelName = self.modelPath.split("\\")[-1]
        self.image = QPixmap(r"app\resource\images\setting_interface\黑色叉号.png")
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
