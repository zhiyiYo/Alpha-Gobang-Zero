# coding: utf-8
import torch
from torch import nn
from torch.nn import functional as F

from .chess_board import ChessBoard


class ResidueBlock(nn.Module):
    """ 残差块 """

    def __init__(self, in_channels=128, out_channels=128):
        """
        Parameters
        ----------
        in_channels: int
            输入图像通道数

        out_channels: int
            输出图像通道数
        """
        super().__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.conv1 = nn.Conv2d(in_channels, out_channels,
                               kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(out_channels, out_channels,
                               kernel_size=3, stride=1, padding=1)
        self.batch_norm1 = nn.BatchNorm2d(num_features=out_channels)
        self.batch_norm2 = nn.BatchNorm2d(num_features=out_channels)

    def forward(self, x):
        out = F.relu(self.batch_norm1(self.conv1(x)))
        out = self.batch_norm2(self.conv2(out))
        return F.relu(out + x)


class PolicyHead(nn.Module):
    """ 策略头 """

    def __init__(self, in_channels=128, board_len=9):
        """
        Parameters
        ----------
        in_channels: int
            输入通道数

        board_len: int
            棋盘大小
        """
        super().__init__()
        self.board_len = board_len
        self.in_channels = in_channels
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, 2, 1, stride=1),
            nn.BatchNorm2d(num_features=2),
            nn.ReLU()
        )
        self.fc = nn.Linear(2*board_len**2, board_len**2)

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x.flatten(1))
        return F.log_softmax(x, dim=1)


class ValueHead(nn.Module):
    """ 价值头 """

    def __init__(self, in_channels=128, board_len=9):
        """
        Parameters
        ----------
        in_channels: int
            输入通道数

        board_len: int
            棋盘大小
        """
        super().__init__()
        self.in_channels = in_channels
        self.board_len = board_len
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, 1, kernel_size=1, stride=1),
            nn.BatchNorm2d(num_features=1),
            nn.ReLU()
        )
        self.fc = nn.Sequential(
            nn.Linear(board_len**2, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Tanh()
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x.flatten(1))
        return x


class PolicyValueNet(nn.Module):
    """ 策略价值网络 """

    def __init__(self, board_len=9, n_feature_planes=9, is_use_gpu=True):
        """
        Parameters
        ----------
        board_len: int
            棋盘大小

        n_feature_planes: int
            输入图像通道数，对应特征
        """
        super().__init__()
        self.board_len = board_len
        self.is_use_gpu = is_use_gpu
        self.n_feature_planes = n_feature_planes
        self.device = torch.device('cuda:0' if is_use_gpu else 'cpu')
        self.conv = nn.Sequential(
            nn.Conv2d(n_feature_planes, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(num_features=128),
            nn.ReLU()
        )
        self.residues = nn.Sequential(
            *[ResidueBlock(128, 128) for i in range(5)])
        self.policy_head = PolicyHead(128, board_len)
        self.value_head = ValueHead(128, board_len)

    def forward(self, x):
        """ 前馈，输出 `p_hat` 和 `V`

        Parameters
        ----------
        x: Tensor of shape (N, C, H, W)
            棋局的状态特征平面张量

        Returns
        -------
        p_hat: Tensor of shape (N, board_len^2)
            对数先验概率向量

        value: Tensor of shape (N, 1)
            当前局面的估值
        """
        x = self.conv(x)
        x = self.residues(x)
        p_hat = self.policy_head(x)
        value = self.value_head(x)
        return p_hat, value

    def get_action_probs_value(self, chess_board: ChessBoard):
        """ 获取当前局面上所有可用 `action` 和他对应的先验概率 `P(s, a)`，以及局面的 `value`

        Parameters
        ----------
        chess_board: ChessBoard
            棋盘

        Returns
        -------
        action_probs: zip of length `len(chess_board.available_actions)`
            当前局面上所有可用 `action` 和他对应的先验概率 `P(s, a)`

        value: float
            当前局面的估值
        """
        feature_planes = chess_board.get_feature_planes().to(self.device)
        feature_planes.unsqueeze_(0)
        p_hat, value = self(feature_planes)
        # 将对数概率转换为非对数概率
        p = torch.exp(p_hat).flatten()
        # 只取可行的落点
        if self.is_use_gpu:
            p = p[chess_board.available_actions].cpu().detach().numpy()
        else:
            p = p[chess_board.available_actions].detach().numpy()
        return zip(chess_board.available_actions, p), value[0].item()

    def get_action_probs_value_(self, batch_feature_planes):
        """ 返回动作空间的所有动作对应的先验概率向量 `p` ，以及局面的 `value`

        Parameters
        ----------
        batch_feature_planes: Tensor of shape (N, C, H, W)
            批量状态特征平面张量

        Returns
        -------
        p: Tensor of shape (N, board_len^2)
            先验概率向量 `p`

        value: Tensor of shape (N, 1)
            当前局面的估值
        """
        p_hat, value = self(batch_feature_planes)
        p = torch.exp(p_hat)
        return p, value
