# coding:utf-8
from monte_carlo_tree_search import MCTS, Node, State
from PyQt5.QtCore import pyqtSignal, QThread


class AIThread(QThread):
    """ AI """

    searchComplete = pyqtSignal(int)

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
        state = State(self.chessBoard.state_mat, self.color,
                      self.chessBoard.pre_action)
        tree = MCTS(Node(state))
        action = tree.search(400)
        self.searchComplete.emit(action)
