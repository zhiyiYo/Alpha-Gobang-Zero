# coding: utf-8
from config.config import train_config
from alphazero.train import TrainModel


train_config['batch_size'] = 500
train_config['start_train_size'] = 500
train_model = TrainModel(**train_config)
train_model.train()
