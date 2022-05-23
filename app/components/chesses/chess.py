# coding:utf-8
from alphazero import ChessBoard, ColorError
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from ..widgets.label import PixmapLabel


class Chess(PixmapLabel):

    def __init__(self, color, parent=None, needTip=True):
        """
        Parameters
        ----------
        color: int
            棋子颜色，可以是 `ChessBoard.BLACK` 或 `ChessBoard.WHITE`

        parent:
            父级窗口

        needTip: bool
            是否需要显示提示气泡
        """
        super().__init__(parent=parent)
        self.__checkColor(color)
        self.color = color
        self.__imagePath_dict = {
            ChessBoard.BLACK: ':/images/chess_board_interface/black.png',
            ChessBoard.WHITE: ':/images/chess_board_interface/white.png',
        }
        self.setPixmap(QPixmap(self.__imagePath_dict[self.color]).scaled(
            40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        if needTip:
            self.tipLabel = PixmapLabel(self)
            self.tipLabel.setPixmap(
                QPixmap(':/images/chess_board_interface/气泡.png'))
            self.tipLabel.move(24, 0)
        else:
            self.tipLabel = PixmapLabel(self)

    def __checkColor(self, color):
        """ 检查颜色是否合法 """
        if color not in [ChessBoard.BLACK, ChessBoard.WHITE]:
            raise ColorError("颜色只能是 `ChessBoard.BLACK` 或 `ChessBoard.WHITE`")
