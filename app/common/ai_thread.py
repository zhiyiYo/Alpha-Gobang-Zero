# coding:utf-8
from alphazero import AlphaZeroMCTS, PolicyValueNet, RolloutMCTS
from PyQt5.QtCore import QThread, pyqtSignal


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
        self.policyValueNet = PolicyValueNet(9, 9)
        # self.mcts = RolloutMCTS(c_puct=c_puct, n_iters=n_iters)
        self.mcts = AlphaZeroMCTS(self.policyValueNet, n_iters=500)

    def run(self):
        """ 根据当前局面获取动作 """
        action = self.mcts.get_action(self.chessBoard)
        self.searchComplete.emit(action)
