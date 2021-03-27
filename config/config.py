# coding: utf-8

# 训练设置
train_config = {
    'c_puct': 4,
    'board_len': 9,
    'batch_size': 10,
    'is_use_gpu': True,
    'n_test_games': 10,
    'n_mcts_iters': 800,
    'n_self_plays': 1500,
    "check_frequency": 100,
}


# 游戏设置
game_config = {
    'c_puct': 5,
    'is_use_gpu': True,
    'n_mcts_iters': 1500,
    'is_human_first': True,
}
