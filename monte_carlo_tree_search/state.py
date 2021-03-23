# coding:utf-8
import numpy as np
import random


class State:
    """ 五子棋局面 """

    EMPTY = 0
    BLACK = -1
    WHITE = 1

    def __init__(self, state_mat: np.ndarray, color, pre_action: int) -> None:
        """
        Parameters
        ----------
        state_mat: `~np.ndarray` of shape (board_len, board_len)
            代表当前局面的矩阵

        color: int
            棋子的颜色，可以是 `State.BLACK` 或 `State.WHITE`

        pre_action: int
            上一步棋的落点，范围为 `0 - 80`
        """
        if color not in [State.BLACK, State.WHITE]:
            raise ValueError("传入的颜色只能是 `State.BLACK` 或者 `State.WHITE`")
        self.color = color
        self.is_ends_in_a_draw = False
        self.__state_mat = state_mat.copy()
        self.board_len = self.state_mat.shape[0]
        self.pre_action = pre_action
        rows, cols = np.where(self.state_mat == State.EMPTY)
        self.available_actions = (rows*self.board_len+cols).tolist()

    @property
    def state_mat(self):
        return self.__state_mat

    def __eq__(self, other):
        return np.array_equal(self.state_mat, other.state_mat)

    def next_state(self):
        """ 随机走一步棋，返回下一局面 """
        action = random.choice(self.available_actions)
        return self.do_action(action)

    def do_action(self, action: int):
        """ 走棋

        Parameters
        ----------
        action: int
            落点
        """
        i, j = action//self.board_len, action % self.board_len
        mat = self.state_mat.copy()
        mat[i, j] = self.color
        return State(mat, -self.color, action)

    def is_game_over(self):
        """ 判断游戏是否结束 """
        for i in range(self.board_len):
            for j in range(self.board_len):
                # 水平方向搜索，只可能是输
                if j <= self.board_len - 5 and np.all(
                        self.state_mat[i, j: j + 5] == -self.color):
                    return True
                # 竖直方向搜索
                if i <= self.board_len - 5 and np.all(
                        self.state_mat[i: i + 5, j] == -self.color):
                    return True
                # 副对角线方向搜索
                if i <= self.board_len-5 and j >= 4:
                    row = [i + x for x in range(5)]
                    col = [j - x for x in range(5)]
                    if np.all(self.state_mat[row, col] == -self.color):
                        return True
                # 沿主对角线方向搜索
                if i <= self.board_len-5 and j <= self.board_len-5:
                    row = [i + x for x in range(5)]
                    col = [j + x for x in range(5)]
                    if np.all(self.state_mat[row, col] == -self.color):
                        return True

        # 没有可以落子的位置，游戏结束
        if not self.available_actions:
            self.is_ends_in_a_draw = True
            return True

        return False


if __name__ == "__main__":
    state_mat = np.ones((9, 9), int) * State.EMPTY
    state_mat[1, 1] = State.BLACK
    state = State(state_mat, State.BLACK, 10)
    print(len(state.available_actions))
