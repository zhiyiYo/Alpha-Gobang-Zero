# coding: utf-8
from config.config import train_config
from alphazero.train import TrainPipeLine


train_config['n_mcts_iters'] = 600
train_pipe_line = TrainPipeLine(**train_config)
train_pipe_line.train()
