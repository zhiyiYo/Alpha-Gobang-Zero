# coding:utf-8
import json
import os
import time

import torch
import torch.nn.functional as F
from torch import nn, optim
from torch.optim.lr_scheduler import MultiStepLR
from torch.utils.data import DataLoader

from .alpha_zero_mcts import AlphaZeroMCTS
from .chess_board import ChessBoard
from .policy_value_net import PolicyValueNet
from .self_play_dataset import SelfPlayData, SelfPlayDataSet


def save_model(train_func):
    """ 保存模型 """
    def wrapper(train_pipe_line, *args, **kwargs):
        try:
            train_func(train_pipe_line)
        except:
            os.makedirs('model', exist_ok=True)
            t = time.strftime('%Y-%m-%d_%H-%M-%S',
                              time.localtime(time.time()))
            path = f'model\\last_policy_value_net_{t}.pth'
            train_pipe_line.policy_value_net.eval()
            torch.save(train_pipe_line.policy_value_net, path)
            print(f'🎉 训练结束，已将当前模型保存到 {os.path.join(os.getcwd(), path)}')
            # 保存数据
            with open('log\\train_losses.json',  'w', encoding='utf-8') as f:
                json.dump(train_pipe_line.train_losses, f)
    return wrapper


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

        value: Tensor of shape (N, )
            对每个局面的估值

        z: Tensor of shape (N, )
            最终的游戏结果相对每一个玩家的奖赏
        """
        value_loss = F.mse_loss(value, z)
        policy_loss = -torch.sum(pi*p_hat, dim=1).mean()
        loss = value_loss + policy_loss
        return loss


class TrainModel:
    """ 训练模型 """

    def __init__(self, board_len=9, lr=0.01, n_self_plays=1500, n_mcts_iters=500, n_feature_planes=4, batch_size=32,
                 start_train_size=2000, check_frequency=100, n_test_games=10, c_puct=4, is_use_gpu=True, **kwargs):
        """
        Parameters
        ----------
        board_len: int
            棋盘大小

        lr: float
            学习率

        n_self_plays: int
            自我博弈游戏局数

        n_mcts_iters: int
            蒙特卡洛树搜索次数

        n_feature_planes: int
            特征平面个数

        batch_size: int
            mini-batch 的大小

        start_train_size: int
            开始训练模型时的最小数据集尺寸

        check_frequency: int
            测试模型的频率

        n_test_games: int
            测试模型时与历史最优模型的比赛局数

        c_puct: float
            探索常数

        is_use_gpu: bool
            是否使用 GPU
        """
        self.c_puct = c_puct
        self.is_use_gpu = is_use_gpu
        self.batch_size = batch_size
        self.n_self_plays = n_self_plays
        self.n_test_games = n_test_games
        self.n_mcts_iters = n_mcts_iters
        self.check_frequency = check_frequency
        self.start_train_size = start_train_size
        self.device = torch.device('cuda:0' if is_use_gpu else 'cpu')
        self.chess_board = ChessBoard(board_len, n_feature_planes)
        # 实例化策略-价值网络和蒙特卡洛搜索树
        self.policy_value_net = self.__get_policy_value_net()
        self.mcts = AlphaZeroMCTS(
            self.policy_value_net, c_puct=c_puct, n_iters=n_mcts_iters, is_self_play=True)
        # 创建优化器和损失函数
        self.optimizer = optim.Adam(
            self.policy_value_net.parameters(), lr=lr, weight_decay=1e-4)
        self.criterion = PolicyValueLoss()
        self.lr_scheduler = MultiStepLR(self.optimizer, [400, 800], gamma=0.1)
        # 实例化数据集
        self.dataset = SelfPlayDataSet(board_len)
        # 记录误差
        self.train_losses = self.__load_losses()

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
        self.policy_value_net.eval()
        self.chess_board.clear_board()
        pi_list, feature_planes_list, players = [], [], []

        # 开始一局游戏
        while True:
            action, pi = self.mcts.get_action(self.chess_board)
            # 保存每一步的数据
            feature_planes_list.append(self.chess_board.get_feature_planes())
            players.append(self.chess_board.current_player)
            pi_list.append(pi)
            self.chess_board.do_action(action)
            # 判断游戏是否结束
            is_over, winner = self.chess_board.is_game_over()
            if is_over:
                if winner is not None:
                    z_list = [1 if i == winner else -1 for i in players]
                else:
                    z_list = [0]*len(players)
                break

        # 重置根节点
        self.mcts.reset_root()

        # 返回数据
        self_play_data = SelfPlayData(
            pi_list=pi_list, z_list=z_list, feature_planes_list=feature_planes_list)
        return self_play_data

    @save_model
    def train(self):
        """ 训练模型 """
        for i in range(self.n_self_plays):
            print(f'🏹 正在进行第 {i+1} 局自我博弈游戏...')
            self.dataset.append(self.__self_play())

            # 如果数据集中的数据量大于 start_train_size 就进行一次训练
            if len(self.dataset) >= self.start_train_size:
                data_loader = iter(DataLoader(
                    self.dataset, self.batch_size, shuffle=True, drop_last=False))
                print('💊 开始训练...')

                self.policy_value_net.train()
                # 随机选出一批数据来训练，防止过拟合
                feature_planes, pi, z = next(data_loader)
                feature_planes = feature_planes.to(self.device)
                pi, z = pi.to(self.device), z.to(self.device)
                for _ in range(5):
                    # 前馈
                    p_hat, value = self.policy_value_net(feature_planes)
                    # 梯度清零
                    self.optimizer.zero_grad()
                    # 计算损失
                    loss = self.criterion(p_hat, pi, value.flatten(), z)
                    # 误差反向传播
                    loss.backward()
                    # 更新参数
                    self.optimizer.step()
                    # 学习率退火
                    self.lr_scheduler.step()

                # 记录误差
                self.train_losses.append([i, loss.item()])
                print(f"🚩 train_loss = {loss.item():<10.5f}\n")

            # 测试模型
            if (i+1) % self.check_frequency == 0:
                self.__test_model()

    def __test_model(self):
        """ 测试模型 """
        model_path = 'model\\best_policy_value_net.pth'
        # 如果最佳模型不存在保存当前模型为最佳模型
        if not os.path.exists(model_path):
            torch.save(self.policy_value_net, model_path)
            return

        # 载入历史最优模型
        best_model = torch.load(model_path)  # type:PolicyValueNet
        best_model.eval()
        best_model.set_device(self.is_use_gpu)
        mcts = AlphaZeroMCTS(best_model, self.c_puct, self.n_mcts_iters)
        self.mcts.set_self_play(False)
        self.policy_value_net.eval()

        # 开始比赛
        print('🩺 正在测试当前模型...')
        n_wins = 0
        for i in range(self.n_test_games):
            self.chess_board.clear_board()
            self.mcts.reset_root()
            mcts.reset_root()
            while True:
                # 当前模型走一步
                is_over, winner = self.__do_mcts_action(self.mcts)
                if is_over:
                    n_wins += int(winner == ChessBoard.BLACK)
                    break
                # 历史最优模型走一步
                is_over, winner = self.__do_mcts_action(mcts)
                if is_over:
                    break

        # 如果胜率大于 55%，就保存当前模型为最优模型
        win_prob = n_wins/self.n_test_games
        if win_prob > 0.55:
            torch.save(self.mcts.policy_value_net, model_path)
            print(f'🥇 保存当前模型为最优模型，当前模型胜率为：{win_prob:.1%}\n')
        else:
            print(f'🎃 保持历史最优模型不变，当前模型胜率为：{win_prob:.1%}\n')
        self.mcts.set_self_play(True)

    def __do_mcts_action(self, mcts):
        """ 获取动作 """
        action = mcts.get_action(self.chess_board)
        self.chess_board.do_action(action)
        is_over, winner = self.chess_board.is_game_over()
        return is_over, winner

    def __get_policy_value_net(self):
        """ 创建策略-价值网络，如果存在历史最优模型则直接载入最优模型 """
        best_model = 'best_policy_value_net.pth'
        history_models = sorted(
            [i for i in os.listdir('model') if i.startswith('last')])
        # 从历史模型中选取最新模型
        model = history_models[-1] if history_models else best_model
        model = f'model\\{model}'
        if os.path.exists(model):
            print(f'💎 载入模型 {model} ...\n')
            net = torch.load(model).to(self.device)  # type:PolicyValueNet
            net.set_device(self.is_use_gpu)
        else:
            net = PolicyValueNet(n_feature_planes=self.chess_board.n_feature_planes,
                                 is_use_gpu=self.is_use_gpu).to(self.device)
        return net

    def __load_losses(self):
        """ 载入历史损失数据 """
        path = 'log\\train_losses.json'
        train_losses = []
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                train_losses = json.load(f)
        else:
            os.makedirs('log', exist_ok=True)
        return train_losses
