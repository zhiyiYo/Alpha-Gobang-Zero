# coding: utf-8

# 训练设置
train_config = {
    'lr': 0.01,
    'c_puct': 3,
    'board_len': 9,
    'batch_size': 32,
    'is_use_gpu': True,
    'n_test_games': 10,
    'n_mcts_iters': 500,
    'n_self_plays': 4000,
    'n_feature_planes': 6,
    'check_frequency': 100,
    'start_train_size': 2000
}


# 游戏设置
game_config = {
    'c_puct': 4,
    'is_use_gpu': True,
    'n_mcts_iters': 1500,
    'is_human_first': True,
    'model': 'model\\best_policy_value_net.pth'
}
