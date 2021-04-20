# coding:utf-8
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QBrush, QFont, QPainter, QPen
from PyQt5.QtWidgets import QLabel


class FlatChess(QLabel):
    """ 扁平化的棋子 """

    def __init__(self, number, color=Qt.black, radius=18, parent=None):
        """
        Parameters
        ----------
        number: int
            棋子的序号

        color: int
            棋子颜色，只能是 `Qt.white` 或者 `Qt.black`

        radius: int
            棋子半径

        parent:
            父级窗口
        """
        super().__init__(parent=parent)
        if color not in [Qt.white, Qt.black]:
            raise ValueError('棋子颜色只能是 `Qt.white` 或者 `Qt.black`')
        self.color = color
        self.number = number
        self.radius = radius
        self.textColor = Qt.black if color == Qt.white else Qt.white
        self.setFixedSize(2*radius, 2*radius)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, e):
        """ 绘制棋子 """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.TextAntialiasing)
        # 绘制背景
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(self.color))
        r = self.radius-1
        painter.drawEllipse(1, 1, 2*r, 2*r)
        # 绘制序号
        painter.setPen(QPen(self.textColor))
        painter.setFont(QFont('Microsoft YaHei', 10))
        painter.drawText(QRect(0, 6, self.width(), self.height()),
                         Qt.AlignHCenter, str(self.number))
