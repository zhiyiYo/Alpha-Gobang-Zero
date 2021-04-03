# coding: utf-8
from alphazero.train import TrainModel


train_config = {
    'lr': 1e-4,
    'c_puct': 3,
    'board_len': 9,
    'batch_size': 500,
    'is_use_gpu': True,
    'n_test_games': 10,
    'n_mcts_iters': 500,
    'n_self_plays': 4000,
    'n_feature_planes': 6,
    'check_frequency': 100,
    'start_train_size': 500
}
train_model = TrainModel(**train_config)
train_model.train()
