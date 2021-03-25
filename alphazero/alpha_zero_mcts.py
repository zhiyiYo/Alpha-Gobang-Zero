# coding: utf-8
import numpy as np

from .chess_board import ChessBoard
from .node import Node
from .policy_value_net import PolicyValueNet


class AlphaZeroMCTS:
    """ 基于策略-价值网络的蒙特卡洛搜索树 """

    def __init__(self, policy_value_net: PolicyValueNet, c_puct: float = 6, n_iters=1000, is_self_play=False) -> None:
        """
        Parameters
        ----------
        policy_value_net: PolicyValueNet
            策略价值网络

        c_puct: float
            探索常数

        n_iters: int
            迭代次数

        is_self_play: bool
            是否处于自我博弈状态
        """
        self.c_puct = c_puct
        self.n_iters = n_iters
        self.is_self_play = is_self_play
        self.policy_value_net = policy_value_net
        self.root = Node(prior_prob=1, parent=None)

    def get_action(self, chess_board: ChessBoard):
        """ 根据当前局面返回下一步动作

        Parameters
        ----------
        chess_board: ChessBoard
            棋盘

        Returns
        -------
        action: int
            当前局面下的最佳动作

        pi: `np.ndarray`
            执行每个可行动作的概率，正比于根节点的子节点的访问次数，只在 `is_self_play` 模式下返回
        """
        # 更新根节点（考虑人类玩家的动作）
        # pre_action = chess_board.previous_action
        # if pre_action and pre_action in self.root.children:
        #     self.root = self.root.children[pre_action]
        #     self.root.parent = None
        self.root = Node(prior_prob=1, parent=None)

        for i in range(self.n_iters):
            # 拷贝棋盘
            board = chess_board.copy()

            # 如果没有遇到叶节点，就一直向下搜索并更新棋盘
            node = self.root
            while not node.is_leaf_node():
                action, node = node.select()
                board.do_action(action)

            # 判断游戏是否结束，如果没结束就拓展叶节点
            is_over, winner = board.is_game_over()
            action_probs, value = self.policy_value_net.get_action_probs_value()
            if not is_over:
                node.expand(action_probs)

            # 反向传播
            node.backup(-value)

        # 计算 pi，在自我博弈状态下：游戏的前三十步，温度系数为 1，后面的温度系数趋于无穷小
        tau = 1 if self.is_self_play and len(chess_board.state) <= 30 else 1e-3
        visits = np.array([i.N for i in self.root.children.items()])
        pi = visits**(1/tau)/np.sum(visits**(1/tau))
        # 添加狄利克雷噪声
        if self.is_self_play:
            pi = 0.75*pi + 0.25*np.random.dirichlet(0.03*len(pi))

        # 根据 pi 选出动作及其对应节点
        action = np.random.choice(self.root.children.keys(), p=pi)
        # self.root = self.root.children[action]
        # self.root.parent = None

        if self.is_self_play:
            return action, pi
        return action
