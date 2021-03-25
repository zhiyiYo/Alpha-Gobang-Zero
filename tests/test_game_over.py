import unittest
from alphazero import ChessBoard


class TestGameOver(unittest.TestCase):
    """ 测试游戏结束函数 """

    def test_horizon(self):
        """ 测试水平方向 """
        multi_game_actions = [
            # 第一局
            [(0, 1), (1, 1), (0, 2), (1, 2), (0, 3),
             (1, 3), (0, 4), (1, 4), (0, 5)],
            # 第二局
            [(0, 4), (1, 1), (0, 5), (1, 2), (0, 6),
             (1, 3), (0, 7), (1, 4), (1, 8), (1, 5)],
            # 第三局
            [(0, 4), (1, 1), (0, 5), (1, 2), (0, 6),
             (1, 3), (0, 7), (1, 4), (1, 8)],
        ]
        self.__simulation(multi_game_actions, [
                          (True, ChessBoard.BLACK), (True, ChessBoard.WHITE), (False, None)])

    def test_vertical(self):
        """ 测试竖直方向 """
        multi_game_actions = [
            # 第一局
            [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0),
             (2, 1), (3, 0), (3, 1), (4, 0)],
            # 第二局
            [(4, 0), (4, 1), (5, 0), (5, 1), (6, 0),
             (6, 1), (7, 0), (7, 1), (0, 0), (8, 1)],
            # 第三局
            [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0),
             (2, 1), (3, 0), (3, 1)],
        ]
        self.__simulation(multi_game_actions, [
                          (True, ChessBoard.BLACK), (True, ChessBoard.WHITE), (False, None)])

    def test_main_diagonal(self):
        """ 测试主对角线方向 """
        multi_game_actions = [
            # 第一局
            [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2),
             (2, 3), (3, 3), (3, 4), (4, 4)],
            # 第二局
            [(4, 4), (3, 4), (5, 5), (4, 5), (6, 6),
             (5, 6), (7, 7), (6, 7), (8, 7), (7, 8)],
            # 第三局
            [(4, 4), (3, 4), (5, 5), (4, 5), (6, 6),
             (5, 6), (7, 7), (6, 7), (8, 7), (6, 8)],
        ]
        self.__simulation(multi_game_actions, [
                          (True, ChessBoard.BLACK), (True, ChessBoard.WHITE), (False, None)])

    def test_sub_diagonal(self):
        """ 测试副对角线方向 """
        multi_game_actions = [
            # 第一局
            [(0, 4), (0, 5), (1, 3), (1, 4), (2, 2),
             (2, 3), (3, 1), (3, 2), (4, 0)],
            # 第二局
            [(4, 4), (4, 5), (5, 3), (5, 4), (6, 2),
             (6, 3), (7, 1), (7, 2), (8, 8), (8, 1)],
            # 第三局
            [(4, 4), (4, 5), (5, 3), (5, 4), (6, 2),
             (6, 3), (7, 1), (7, 2), (8, 1), (8, 0)],
        ]
        self.__simulation(multi_game_actions, [
                          (True, ChessBoard.BLACK), (True, ChessBoard.WHITE), (False, None)])

    def __simulation(self, multi_game_actions, labels):
        """ 测试结果 """

        multi_game_actions = [[i*9+j for i, j in actions]
                              for actions in multi_game_actions]

        chess_boards = []
        for actions in multi_game_actions:
            chess_board = ChessBoard()
            for action in actions:
                chess_board.do_action(action)
            chess_boards.append(chess_board)

        overs = [board.is_game_over() for board in chess_boards]
        self.assertSequenceEqual(overs, labels)
