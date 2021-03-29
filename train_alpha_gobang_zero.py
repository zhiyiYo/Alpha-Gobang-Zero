# coding: utf-8
from config.config import train_config
from alphazero.train import TrainModel


train_config['n_mcts_iters'] = 500
train_model = TrainModel(**train_config)
train_model.train()
