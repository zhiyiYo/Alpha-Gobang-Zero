# coding:utf-8
from alphazero import ChessBoard, ColorError

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class Chess(QLabel):

    def __init__(self, color, parent=None, needTips=True):
        """
        Parameters
        ----------
        color: int
            棋子颜色，可以是 `ChessBoard.BLACK` 或 `ChessBoard.WHITE`
         """
        super().__init__(parent=parent)
        self.__checkColor(color)
        self.color = color
        self.__imagePath_dict = {
            ChessBoard.BLACK: 'app\\resource\\images\\black.png',
            ChessBoard.WHITE: 'app\\resource\\images\\white.png',
        }
        self.setPixmap(QPixmap(self.__imagePath_dict[self.color]).scaled(
            40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        if needTips:
            self.tipLabel = QLabel(self)
            self.tipLabel.setPixmap(QPixmap('app\\resource\\images\\气泡.png'))
            self.tipLabel.move(24, 0)
        else:
            self.tipLabel = QLabel(self)

    def __checkColor(self, color):
        """ 检查颜色是否合法 """
        if color not in [ChessBoard.BLACK, ChessBoard.WHITE]:
            raise ColorError("颜色只能是 `ChessBoard.BLACK` 或 `ChessBoard.WHITE`")
