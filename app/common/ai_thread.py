# coding:utf-8
import torch
from alphazero import AlphaZeroMCTS, PolicyValueNet, RolloutMCTS
from PyQt5.QtCore import QThread, pyqtSignal


class AIThread(QThread):
    """ AI """

    searchComplete = pyqtSignal(int)

    def __init__(self, chessBoard, model: str, c_puct=5, n_iters=2000, isUseGPU=True, parent=None):
        """
        Parameters
        ----------
        board: ChessBoard
            棋盘

        model: str
            模型路径

        c_puct: float
            探索常数

        n_iters: int
            蒙特卡洛树搜索次数

        isUseGPU: bool
            是否使用 GPU

        parent:
            父级
        """
        super().__init__(parent=parent)
        self.chessBoard = chessBoard
        self.device = torch.device('cuda:0' if isUseGPU else 'cpu')
        self.policyValueNet = torch.load(model).to(
            self.device)  # type:PolicyValueNet
        self.policyValueNet.set_device(is_use_gpu=isUseGPU)
        self.mcts = AlphaZeroMCTS(
            self.policyValueNet, c_puct=c_puct, n_iters=n_iters)

    def run(self):
        """ 根据当前局面获取动作 """
        action = self.mcts.get_action(self.chessBoard)
        self.searchComplete.emit(action)
