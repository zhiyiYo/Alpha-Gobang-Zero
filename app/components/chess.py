# coding:utf-8
from app.common.chess_board import ChessBoard, ColorError
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class Chess(QLabel):

    def __init__(self, color, parent=None):
        super().__init__(parent=parent)
        self.__checkColor(color)
        self.color = color
        self.__imagePath_dict = {
            ChessBoard.BLACK: 'app\\resource\\images\\black.png',
            ChessBoard.WHITE: 'app\\resource\\images\\white.png',
        }
        self.setPixmap(QPixmap(self.__imagePath_dict[self.color]))

    def __checkColor(self, color):
        """ 检查颜色是否合法 """
        if color not in [ChessBoard.BLACK, ChessBoard.WHITE]:
            raise ColorError()
