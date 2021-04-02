# coding:utf-8
import torch
from alphazero import PolicyValueNet


def testModel(model: str):
    """ 测试模型是否可用

    Parameters
    ----------
    model: str
        模型路径
    """
    try:
        model = torch.load(model)
        return isinstance(model, PolicyValueNet)
    except:
        return False
