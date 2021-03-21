# coding:utf-8
from monte_carlo_tree_search import MCTree, Node, State
from PyQt5.QtCore import QObject, pyqtSignal, QThread


class AIThread(QThread):
    """ AI """

    searchComplete = pyqtSignal(tuple)

    def __init__(self, chessBoard, color, parent=None):
        """
        Parameters
        ----------
        board: ChessBoard
            棋盘

        color: int
            AI 所执棋子的颜色

        parent:
            父级
        """
        super().__init__(parent=parent)
        self.chessBoard = chessBoard
        self.color = color

    def run(self):
        """ 根据当前局面获取动作 """
        tree = MCTree(Node(State(self.chessBoard.state_mat, self.color)))
        pos = tree.search(50)
        self.searchComplete.emit(pos)
