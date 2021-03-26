# coding:utf-8
import time
from collections import deque, namedtuple

import numpy as np
import torch
import torch.nn.functional as F
from torch import nn, optim
from torch.optim.lr_scheduler import MultiStepLR
from torch.utils.data import DataLoader

from .alpha_zero_mcts import AlphaZeroMCTS
from .chess_board import ChessBoard
from .policy_value_net import PolicyValueNet
from .self_play_dataset import SelfPlayData, SelfPlayDataSet


class PolicyValueLoss(nn.Module):
    """ 根据 self-play 产生的 `z` 和 `π` 计算误差 """

    def __init__(self):
        super().__init__()

    def forward(self, p_hat, pi, value, z):
        """ 前馈

        Parameters
        ----------
        p_hat: Tensor of shape (N, board_len^2)
            对数动作概率向量

        pi: Tensor of shape (N, board_len^2)
            `mcts` 产生的动作概率向量

        value: Tensor of shape (N, 1)
            对每个局面的估值

        z: Tensor of shape (N, n_actions)
            最终的游戏结果相对每一个玩家的奖赏
        """
        value_loss = torch.mean((z - value.repeat(1, z.size(1)))**2)
        policy_loss = -torch.sum(pi*p_hat, dim=1).mean()
        loss = value_loss + policy_loss
        return loss


class TrainPipeLine:
    """ 训练模型 """

    def __init__(self, n_self_plays=1500, n_mcts_iters=1200, n_train_epochs=5, batch_size=50, is_use_gpu=True):
        """
        Parameters
        ----------
        n_self_plays: int
            自我博弈游戏局数

        n_mcts_iters: int
            蒙特卡洛树搜索次数

        n_train_epochs: int
            训练的世代数

        batch_size: int
            mini-batch 的大小

        is_use_gpu: bool
            是否使用 GPU
        """
        self.is_use_gpu = is_use_gpu
        self.n_self_plays = n_self_plays
        self.n_mcts_iters = n_mcts_iters
        self.n_train_epochs = n_train_epochs
        self.chess_board = ChessBoard()
        self.device = torch.device('cuda:0' if is_use_gpu else 'cpu')
        # 实例化策略-价值网络和蒙特卡洛搜索树
        self.policy_value_net = PolicyValueNet(
            is_use_gpu=is_use_gpu).to(self.device)
        self.mcts = AlphaZeroMCTS(
            self.policy_value_net, c_puct=5, n_iters=n_mcts_iters, is_self_play=True)
        # 创建优化器和损失函数
        self.optimizer = optim.SGD(
            self.policy_value_net.parameters(), lr=0.01, momentum=0.9, weight_decay=1e-4)
        self.criterion = PolicyValueLoss()
        self.lr_scheduler = MultiStepLR(self.optimizer, [400, 800], gamma=0.1)
        # 实例化数据集
        self.batch_size = batch_size
        self.dataset = SelfPlayDataSet()
        # 记录误差
        self.train_losses = []

    def __self_play(self):
        """ 自我博弈一局

        Returns
        -------
        self_play_data: namedtuple
            自我博弈数据，有以下三个成员:
            * `pi_list`: 蒙特卡洛树搜索产生的动作概率向量 π 组成的列表
            * `z_list`: 一局之中每个动作的玩家相对最后的游戏结果的奖赏列表
            * `feature_planes_list`: 一局之中每个动作对应的特征平面组成的列表
        """
        # 初始化棋盘和数据容器
        self.chess_board.clear_board()
        pi_list,  feature_planes_list = [], []

        # 开始一局游戏
        while True:
            action, pi = self.mcts.get_action(self.chess_board)
            self.chess_board.do_action(action)
            # 保存每一步的数据
            pi_list.append(pi)
            feature_planes_list.append(self.chess_board.get_feature_planes())
            # 判断游戏是否结束
            is_over, winner = self.chess_board.is_game_over()
            if is_over:
                if winner is not None:
                    z_list = [1 if i == winner else -
                              1 for i in self.chess_board.state.keys()]
                else:
                    z_list = [0]*len(self.chess_board.state)
                break

        # 重置根节点
        self.mcts.reset_root()

        # 返回数据
        self_play_data = SelfPlayData(pi_list, z_list, feature_planes_list)
        return self_play_data

    def train(self):
        """ 训练模型 """
        for i in range(self.n_self_plays):
            print(f'🏹 正在进行第 {i+1} 局自我博弈游戏...')
            self.dataset.append(self.__self_play())
            # 如果 数据集中的数据量大于 batch_size 就进行一次训练
            if len(self.dataset) >= self.batch_size:
                data_loader = DataLoader(
                    self.dataset, self.batch_size, shuffle=True, drop_last=False)
                print('💊 开始训练...')
                for i in range(self.n_train_epochs):
                    for feature_planes, pi, z in data_loader:
                        feature_planes = feature_planes.to(self.device)
                        pi, z = pi.to(self.device), z.to(self.device)
                        # 前馈
                        p_hat, value = self.policy_value_net(feature_planes)
                        # 梯度清零
                        self.optimizer.zero_grad()
                        # 计算损失
                        loss = self.criterion(p_hat, pi, value, z)
                        # 误差反向传播
                        loss.backward()
                        # 更新参数
                        self.optimizer.step()
                        # 学习率退火
                        self.lr_scheduler.step()
                    self.train_losses.append(loss.item())
                    print(f"🚩 epoch {i} | ● train_loss = {loss.item():<10.5f}")
                # 清空数据集
                self.dataset.clear()
                print('\n')

                # 保存模型
                t = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
                torch.save(self.policy_value_net, f'model\\policy_value_nets_{t}.pth')
