# coding:utf-8
from typing import List

from app.components.chesses.flat_chess import FlatChess
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QBrush, QPainter, QPen
from PyQt5.QtWidgets import QWidget


class FlatChessBoardInterface(QWidget):
    """ 只用来绘制棋谱的扁平化棋盘界面 """

    def __init__(self, board_len=9, parent=None):
        super().__init__(parent=parent)
        self.boardLen = board_len
        self.gridSize = 60
        self.margin = 30
        self.chesses = []  # type: List[FlatChess]
        size = 2*self.margin + (self.boardLen-1)*self.gridSize
        self.setFixedSize(size, size)
        self.setStyleSheet('background: white')

    def paintEvent(self, e):
        """ 绘制棋盘 """
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        # 绘制网格
        left, top = self.__getMargin()
        for i in range(self.boardLen):
            x = y = self.margin + i*self.gridSize
            x = left + i*self.gridSize
            y = top + i*self.gridSize
            width = 2 if i in [0, self.boardLen-1] else 1
            painter.setPen(QPen(Qt.black, width))
            # 竖直线
            painter.drawLine(x, top, x, self.height()-top)
            # 水平线
            painter.drawLine(left, y, self.width()-left-1, y)
        # 绘制圆点
        painter.setBrush(QBrush(Qt.black))
        painter.setPen(Qt.NoPen)
        r = 5
        x = self.width()//2-r
        y = self.height()//2-r
        painter.drawEllipse(x, y, 2*r, 2*r)
        for pos in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            x_ = self.gridSize*pos[0]*(self.boardLen-1)//2/2 + x
            y_ = self.gridSize*pos[1]*(self.boardLen-1)//2/2 + y
            painter.drawEllipse(x_, y_, 2*r, 2*r)

    def __getMargin(self):
        """ 获取棋盘边距 """
        left = (self.width() - (self.boardLen-1)*self.gridSize)//2
        top = (self.height() - (self.boardLen-1)*self.gridSize)//2
        return left, top

    def save(self, path: str):
        """ 保存棋谱为图片 """
        self.grab().save(path, quality=100)

    def drawGame(self, actions: list):
        """ 绘制棋谱

        Parameters
        ----------
        actions: list
            动作列表
        """
        color = Qt.black
        left, top = self.__getMargin()
        for i, action in enumerate(actions, 1):
            chess = FlatChess(i, color, parent=self)
            y = (action // self.boardLen) * self.gridSize + top - 18
            x = (action % self.boardLen) * self.gridSize + left - 18
            chess.move(x, y)
            chess.show()
            self.chesses.append(chess)
            color = Qt.black if color == Qt.white else Qt.white

    def clearBoard(self):
        """ 清空棋盘 """
        for chess in self.chesses:
            chess.deleteLater()
        self.chesses.clear()
