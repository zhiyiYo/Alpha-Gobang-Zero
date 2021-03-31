# coding:utf-8
from collections import deque, namedtuple

import torch
from config.config import train_config
from torch import Tensor
from torch.utils.data import Dataset

SelfPlayData = namedtuple(
    'SelfPlayData', ['pi_list', 'z_list', 'feature_planes_list'])


class SelfPlayDataSet(Dataset):
    """ 自我博弈数据集类，每个样本为元组 `(feature_planes, pi, z)` """

    def __init__(self):
        super().__init__()
        self.__data_deque = deque(maxlen=10000)

    def __len__(self):
        return len(self.__data_deque)

    def __getitem__(self, index):
        return self.__data_deque[index]

    def clear(self):
        """ 清空数据集 """
        self.__data_deque.clear()

    def append(self, self_play_data: SelfPlayData):
        """ 向数据集中插入数据 """
        n = train_config.get('board_len', 9)
        z_list = Tensor(self_play_data.z_list)
        pi_list = self_play_data.pi_list
        feature_planes_list = self_play_data.feature_planes_list
        # 使用翻转和镜像扩充已有数据集
        for z, pi, feature_planes in zip(z_list, pi_list, feature_planes_list):
            for i in range(4):
                # 逆时针旋转 i*90°
                rot_features = torch.rot90(Tensor(feature_planes), i, (1, 2))
                rot_pi = torch.rot90(Tensor(pi.reshape(n, n)), i)
                self.__data_deque.append(
                    (rot_features, rot_pi.flatten(), z))

                # 对逆时针旋转后的数组进行水平翻转
                flip_features = torch.flip(rot_features, [2])
                flip_pi = torch.fliplr(rot_pi)
                self.__data_deque.append(
                    (flip_features, flip_pi.flatten(), z))
