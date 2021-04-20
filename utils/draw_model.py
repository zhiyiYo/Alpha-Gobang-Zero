# coding:utf-8
import torch
from torch.utils.tensorboard import SummaryWriter

from alphazero import PolicyValueNet


net = PolicyValueNet(is_use_gpu=False)
with SummaryWriter('log', comment='策略-价值模型') as w:
    w.add_graph(net, torch.zeros(1, 6, 9, 9))
