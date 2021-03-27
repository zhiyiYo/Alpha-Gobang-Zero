import numpy as np
import torch

from config.config import train_config
from alphazero.train import TrainPipeLine


train_pipe_line = TrainPipeLine(**train_config)
train_pipe_line.train()
