# coding: utf-8
from copy import deepcopy

import numpy as np

from .chess_board import ChessBoard
from .node import Node


class RolloutMCTS:
    """ 基于随机走棋策略的蒙特卡洛树搜索 """

    def __init__(self, c_puct: float = 2, n_iters=1000):
        """
        Parameters
        ----------
        c_puct: float
            探索常数

        n_iters: int
            迭代搜索次数
        """
        self.c_puct = c_puct
        self.n_iters = n_iters
        self.root = Node(1, c_puct, parent=None)

    def get_action(self, chess_board: ChessBoard) -> int:
        """ 根据当前局面返回下一步动作

        Parameters
        ----------
        chess_board: ChessBoard
            棋盘
        """
        for i in self.n_iters:
            # 拷贝一个棋盘用来模拟
            board = deepcopy(chess_board)

            # 如果没有遇到叶节点，就一直向下搜索并更新棋盘
            node = self.root
            while not node.is_leaf_node():
                action, node = node.select()
                board.do_action(action)

            # 判断游戏是否结束，如果没结束就拓展叶节点
            is_over, winner = board.is_game_over()
            if not is_over:

                node.expand()

    def __default_policy(self,chess_board: ChessBoard):
        """ 根据当前局面返回可进行的动作及其概率

        Returns
        -------
        action_probs: List[Tuple[int, float]]
            每个元素都为 `(action, prior_prob)` 元组，根据这个元组创建子节点，
            `action_probs` 的长度为当前棋盘的可用落点的总数
        """

