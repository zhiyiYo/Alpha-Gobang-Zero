# coding:utf-8
import torch
from alphazero import AlphaZeroMCTS, PolicyValueNet, RolloutMCTS
from app.common.model_utils import testModel
from PyQt5.QtCore import QThread, pyqtSignal


class AIThread(QThread):
    """ AI """

    searchComplete = pyqtSignal(int)

    def __init__(self, chessBoard, model: str, c_puct=5, n_iters=2000, is_use_gpu=True, parent=None):
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

        is_use_gpu: bool
            是否使用 GPU

        parent:
            父级
        """
        super().__init__(parent=parent)
        self.chessBoard = chessBoard
        self.setModel(model, c_puct, n_iters, is_use_gpu)

    def run(self):
        """ 根据当前局面获取动作 """
        action = self.mcts.get_action(self.chessBoard)
        self.searchComplete.emit(action)

    def setModel(self, model=None, c_puct=5, n_iters=2000, is_use_gpu=True, **kwargs):
        """ 设置模型

        model: str
            策略-价值模型路径，如果为 `None`，则使用随机走棋策略

        c_puct: float
            探索常数

        n_iters: int
            蒙特卡洛树搜索次数

        isUseGPU: bool
            是否使用 GPU
        """
        self.c_puct = c_puct
        self.n_iters = n_iters
        self.isUseGPU = is_use_gpu
        self.device = torch.device('cuda:0' if self.isUseGPU else 'cpu')
        if model and testModel(model):
            self.model = torch.load(model).to(
                self.device)  # type:PolicyValueNet
            self.model.set_device(is_use_gpu=self.isUseGPU)
            self.model.eval()
            self.mcts = AlphaZeroMCTS(self.model, c_puct, n_iters)
        else:
            self.model = None
            self.mcts = RolloutMCTS(c_puct, n_iters)
