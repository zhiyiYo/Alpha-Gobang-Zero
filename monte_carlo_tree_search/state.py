# coding:utf-8
import numpy as np
import random


class State:
    """ 五子棋局面 """

    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __init__(self, state_mat: np.ndarray, color: int = BLACK) -> None:
        """
        Parameters
        ----------
        state_mat: `~np.ndarray` of shape (board_len, board_len)
            代表当前局面的矩阵，黑方为0，白方为1，空白处为2

        color: int
            棋子的颜色，可以是 `State.BLACK` 或 `State.WHITE`
        """
        if color not in [State.BLACK, State.WHITE]:
            raise ValueError("传入的颜色只能是 `State.BLACK` 或者 `State.WHITE`")
        self.color = color
        self.is_win = False
        self.state_mat = state_mat.copy()
        self.board_len = self.state_mat.shape[0]
        self.action_pos = None
        rows, cols = np.where(self.state_mat == State.EMPTY)
        self.available_poses = [(i, j) for i, j in zip(rows, cols)]

    def __eq__(self, other):
        return np.array_equal(self.state_mat, other.state_mat)

    def next_state(self):
        """ 随机走一步棋，返回下一局面 """
        i, j = random.choice(self.available_poses)
        self.action_pos = (i, j)
        state_mat = self.state_mat.copy()
        state_mat[i, j] = self.color
        return State(state_mat, 3 - self.color)

    def is_game_over(self):
        """ 判断游戏是否结束 """
        for i in range(self.board_len):
            for j in range(self.board_len):
                # 水平方向搜索
                if j <= self.board_len - 5 and np.all(
                        self.state_mat[i, j: j + 5] == self.color):
                    self.is_win = True  # 能走到当前状态只可能赢
                    return True
                # 竖直方向搜索
                elif i <= self.board_len - 5 and np.all(
                        self.state_mat[i: i + 5, j] == self.color):
                    self.is_win = True
                    return True
                # 副对角线方向搜索
                if i <= self.board_len-5 and j >= 4:
                    row = [i + x for x in range(5)]
                    col = [j - x for x in range(5)]
                    if np.all(self.state_mat[row, col] == self.color):
                        self.is_win = True
                        return True
                # 沿主对角线方向搜索
                if i <= self.board_len-5 and j <= self.board_len-5:
                    row = [i + x for x in range(5)]
                    col = [j + x for x in range(5)]
                    if np.all(self.state_mat[row, col] == self.color):
                        self.is_win = True
                        return True

        if len(self.available_poses) == 0:
            self.is_win = None
            return True
        return False


if __name__ == "__main__":
    state_mat = np.ones((15, 15), int) * State.EMPTY
    p1_x = [0, 0, 0, 0, 0]
    p1_y = [14, 13, 12, 11, 10]
    state_mat[p1_x, p1_y] = 1
    state = State(state_mat, [1, 1])
    print(state.next_state().state_mat)
