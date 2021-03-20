# coding: utf-8
import numpy as np
from app.common.chess_board import ChessBoard
from app.components.chess import Chess
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import (QBrush, QIcon, QMouseEvent, QPainter, QPalette,
                         QPixmap)
from PyQt5.QtWidgets import QLabel, QWidget


class MainWindow(QWidget):
    """ 主界面 """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(540, 540)
        self.chessBoard = ChessBoard()
        self.chess = Chess(ChessBoard.BLACK, self)
        self.chess_list = []
        self.isAllowPutChess = True
        # 初始化
        self.initWidget()

    def initWidget(self):
        """ 初始化窗口 """
        self.setWindowTitle('BangGo')
        self.setWindowIcon(QIcon(r'app\resource\images\icon.jpeg'))
        # 设置背景图像
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(
            r'app\resource\images\chessboard.jpg')))
        self.setPalette(palette)
        # 跟踪鼠标
        self.setMouseTracking(True)
        # 棋子置顶
        self.chess.raise_()
        # 调整鼠标下棋子的大小
        self.chess.setPixmap(self.chess.pixmap().scaled(
            20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        """ 跟踪鼠标移动 """
        self.chess.move(e.pos())

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """ 鼠标按下后放置棋子 """
        # 计算棋子在矩阵上的坐标
        cor = self.getChessCoordinate(e.pos())
        self.putChess(cor, ChessBoard.BLACK)

    def getChessCoordinate(self, pos: QPoint):
        """ 计算棋子在矩阵上的坐标 """
        poses = np.array([[QPoint(i, j)*36 + QPoint(23, 23) for j in range(15)]
                          for i in range(15)])
        # Qt坐标系与矩阵的相反
        distances = np.array([
            [(poses[i, j].x()-pos.x())**2 + (poses[i, j].y()-pos.y())**2
             for j in range(15)] for i in range(15)
        ])
        col, row = np.where(distances == distances.min())
        return row[0], col[0]

    def putChess(self, corordinate: tuple, color):
        """ 在棋盘上放置棋子

        Parameters
        ----------
        corordinate: tuple
            棋子的坐标，范围为 `(0, 14) ~ (0, 14)`

        color: int
            棋子的颜色
        """
        # 矩阵的行和列
        row, col = corordinate
        updateOk = self.chessBoard.updateBoard(corordinate, color)
        if updateOk:
            # 矩阵的 axis = 0 方向为 y 轴方向
            chessPos = QPoint(col, row)*36+QPoint(23, 23)-QPoint(18, 18)
            chess = Chess(color, self)
            chess.show()
            chess.move(chessPos)
            self.chess_list.append(chess)
