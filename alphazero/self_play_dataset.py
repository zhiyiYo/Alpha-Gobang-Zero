# coding:utf-8
from collections import deque, namedtuple

import numpy as np
import torch
from torch import Tensor, from_numpy
from torch.utils.data import Dataset

from config.config import train_config

SelfPlayData = namedtuple(
    'SelfPlayData', ['pi_list', 'z_list', 'feature_planes_list'])


class SelfPlayDataSet(Dataset):
    """ 自我博弈数据集类，每个样本为元组 `(feature_planes, pi, z)` """

    def __init__(self):
        super().__init__()
        self.data_deque = deque()

    def __len__(self):
        return len(self.data_deque)

    def __getitem__(self, index):
        return self.data_deque[index]

    def clear(self):
        """ 清空数据集 """
        self.data_deque.clear()

    def append(self, self_play_data: SelfPlayData):
        """ 向数据集中插入数据 """
        n = train_config['board_len']
        z_list = self_play_data.z_list
        pi_list = self_play_data.pi_list
        feature_planes_list = self_play_data.feature_planes_list
        # 使用翻转和镜像扩充已有数据集
        for pi, feature_planes in zip(pi_list, feature_planes_list):
            for i in range(4):
                # 逆时针旋转 i*90°
                rot_features = torch.rot90(Tensor(feature_planes), i, (1, 2))
                rot_pi = torch.rot90(Tensor(pi.reshape(n, n)), i)
                self.data_deque.append(
                    (rot_features, rot_pi.flatten(), Tensor(z_list)))

                # 对逆时针旋转后的数组进行水平翻转
                flip_features = torch.flip(Tensor(rot_features), [2])
                flip_pi = torch.fliplr(Tensor(rot_pi))
                self.data_deque.append(
                    (flip_features, flip_pi.flatten(0), Tensor(z_list)))
