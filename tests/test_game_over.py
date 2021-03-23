import unittest

import numpy as np

from monte_carlo_tree_search.state import State


class TestGameOver(unittest.TestCase):
    """ 测试游戏结束函数 """

    def test_horizon(self):
        """ 测试水平方向 """
        px = [[0, 0, 0, 0, 0],
              [8, 8, 8, 8, 8],
              [8, 8, 8, 8, 8]]
        py = [[8, 7, 6, 5, 4],
              [0, 1, 2, 3, 4],
              [0, 2, 3, 4, 5]]
        self.__simulation(px, py, [True, True, False])

    def test_vertical(self):
        """ 测试竖直方向 """
        px = [[0, 1, 2, 3, 4],
              [8, 7, 6, 5, 4],
              [8, 7, 6, 5, 3]]
        py = [[0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0]]
        self.__simulation(px, py, [True, True, False])

    def test_main_diagonal(self):
        """ 测试主对角线方向 """
        px = [[0, 1, 2, 3, 4],
              [4, 5, 6, 7, 8],
              [4, 5, 6, 7, 8],
              [1, 2, 3, 4, 5]]
        py = [[0, 1, 2, 3, 4],
              [0, 1, 2, 3, 4],
              [0, 1, 2, 3, 3],
              [1, 2, 3, 4, 4]]
        self.__simulation(px, py, [True, True, False, False])

    def test_sub_diagonal(self):
        """ 测试副对角线方向 """
        px = [[0, 1, 2, 3, 4],
              [4, 5, 6, 7, 8],
              [4, 5, 6, 7, 8],
              [3, 3, 2, 1, 0]]
        py = [[4, 3, 2, 1, 0],
              [8, 7, 6, 5, 4],
              [0, 1, 2, 3, 3],
              [0, 1, 2, 3, 4]]
        self.__simulation(px, py, [True, True, False, False])

    def __simulation(self, px, py, labels):
        """ 测试结果 """
        state_mats = [np.ones((9, 9), int) *
                      State.EMPTY for i in range(len(px))]
        for x, y, state_mat in zip(px, py, state_mats):
            state_mat[x, y] = State.BLACK
        overs = [State(state_mat).is_game_over() for state_mat in state_mats]
        self.assertSequenceEqual(overs, labels)
