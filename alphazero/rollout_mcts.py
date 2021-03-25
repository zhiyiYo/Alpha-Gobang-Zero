# coding: utf-8
import random
import numpy as np

from .chess_board import ChessBoard
from .node import Node


class RolloutMCTS:
    """ 基于随机走棋策略的蒙特卡洛树搜索 """

    def __init__(self, c_puct: float = 5, n_iters=1000):
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
        # 更新根节点
        # pre_action = chess_board.previous_action
        # if pre_action and pre_action in self.root.children:
        #     self.root = self.root.children[pre_action]
        #     self.root.parent = None
        self.root = Node(1, self.c_puct, parent=None)

        for i in range(self.n_iters):
            # 拷贝一个棋盘用来模拟
            board = chess_board.copy()

            # 如果没有遇到叶节点，就一直向下搜索并更新棋盘
            node = self.root
            while not node.is_leaf_node():
                action, node = node.select()
                board.do_action(action)

            # 判断游戏是否结束，如果没结束就拓展叶节点
            is_over, winner = board.is_game_over()
            if not is_over:
                node.expand(self.__default_policy(board))

            # 模拟
            value = self.__rollout(board)
            # 反向传播
            node.backup(-1*value)

        # 根据子节点的访问次数来选择动作
        action = max(self.root.children.items(), key=lambda i: i[1].N)[0]
        # 更新根节点
        # self.root = Node(prior_prob=1)
        self.root = self.root.children[action]
        self.root.parent = None
        return action

    def __default_policy(self, chess_board: ChessBoard):
        """ 根据当前局面返回可进行的动作及其概率

        Returns
        -------
        action_probs: List[Tuple[int, float]]
            每个元素都为 `(action, prior_prob)` 元组，根据这个元组创建子节点，
            `action_probs` 的长度为当前棋盘的可用落点的总数
        """
        n = len(chess_board.available_actions)
        probs = np.ones(n) / n
        return zip(chess_board.available_actions, probs)

    def __rollout(self, board: ChessBoard):
        """ 快速走棋，模拟一局 """
        current_player = board.current_player

        while True:
            is_over, winner = board.is_game_over()
            if is_over:
                break
            action = random.choice(board.available_actions)
            board.do_action(action)

        # 计算 Value，平局为 0，当前玩家胜利则为 1, 输为 -1
        if winner is not None:
            return 1 if winner == current_player else -1
        return 0
