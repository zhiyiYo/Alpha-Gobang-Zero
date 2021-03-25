# coding:utf-8
from alphazero.rollout_mcts import RolloutMCTS
from PyQt5.QtCore import pyqtSignal, QThread


class AIThread(QThread):
    """ AI """

    searchComplete = pyqtSignal(int)

    def __init__(self, chessBoard, c_puct=5, n_iters=2000, parent=None):
        """
        Parameters
        ----------
        board: ChessBoard
            棋盘

        parent:
            父级
        """
        super().__init__(parent=parent)
        self.chessBoard = chessBoard
        self.mcts = RolloutMCTS(c_puct=c_puct, n_iters=n_iters)

    def run(self):
        """ 根据当前局面获取动作 """
        action = self.mcts.get_action(self.chessBoard)
        self.searchComplete.emit(action)
