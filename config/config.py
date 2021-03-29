# coding: utf-8

# 训练设置
train_config = {
    'lr': 0.01,
    'c_puct': 4,
    'board_len': 9,
    'batch_size': 32,
    'is_use_gpu': True,
    'n_test_games': 10,
    'n_mcts_iters': 600,
    'n_self_plays': 1500,
    'check_frequency': 100,
    'start_train_size': 600
}


# 游戏设置
game_config = {
    'c_puct': 4,
    'is_use_gpu': True,
    'n_mcts_iters': 1500,
    'is_human_first': True,
    'model': 'model\\best_policy_value_net.pth'
}
