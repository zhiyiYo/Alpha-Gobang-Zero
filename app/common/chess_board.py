# coding: utf-8
import numpy as np


class ChessBoard:
    """ 15 × 15 五子棋棋盘 """

    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __init__(self, state_mat=None):
        self.board_len = 15
        self.__state_mat = np.ones(
            (15, 15), int)*self.EMPTY if state_mat is None else state_mat
        # 计算可用区域
        rows, cols = np.where(self.__state_mat == self.EMPTY)
        self.__updateAvailablePos()

    @property
    def state_mat(self):
        return self.__state_mat

    def setBoard(self, state_mat: np.ndarray):
        """ 设置棋局

        Parameters
        ----------
        state_mat: `np.ndarray` of shape (15, 15)
            代表棋局的矩阵
        """
        self.__state_mat = state_mat.copy()

    def clearBoard(self):
        """ 清空棋盘 """
        self.__state_mat = np.ones((15, 15), int)*self.EMPTY
        self.__updateAvailablePos()

    def updateBoard(self, corordinate: tuple, color):
        """ 在棋盘上放置棋子，只允许在没有棋子的地方放置

        parameters
        ----------
        corordinate: Tuple[int, int]
            着棋点

        color: int
            棋子颜色，可以是 `ChessBoard.BLACK` 或 `ChessBoard.WHITE`

        Returns
        -------
        updateOK: bool
            是否成功更新
        """
        if color not in [self.BLACK, self.WHITE]:
            raise ColorError()
        if corordinate not in self.__available_poses:
            return False
        self.__state_mat[corordinate[0], corordinate[1]] = color
        self.__available_poses.remove(corordinate)
        return True

    def isGameOver(self):
        """ 判断游戏是否结束

        Returns
        -------
        isOver: bool
            游戏是否结束

        winner: int
            如果没有分出胜负, winner为 None，否则 winner 为胜者的颜色
        """
        for i in range(self.board_len):
            for j in range(self.board_len):
                # 水平方向搜索
                if j <= self.board_len - 5:
                    if np.all(self.__state_mat[i, j: j + 5] == self.BLACK):
                        return True, self.BLACK
                    elif np.all(self.__state_mat[i, j: j + 5] == self.WHITE):
                        return True, self.WHITE
                # 竖直方向搜索
                if i <= self.board_len - 5:
                    if np.all(self.__state_mat[i: i + 5, j] == self.BLACK):
                        return True, self.BLACK
                    elif np.all(self.__state_mat[i: i + 5, j] == self.WHITE):
                        return True, self.WHITE
                # 副对角线方向搜索
                if i <= self.board_len-5 and j >= 4:
                    row = [i + x for x in range(5)]
                    col = [j - x for x in range(5)]
                    if np.all(self.__state_mat[row, col] == self.BLACK):
                        return True, self.BLACK
                    elif np.all(self.__state_mat[row, col] == self.WHITE):
                        return True, self.WHITE
                # 沿主对角线方向搜索
                if i <= self.board_len-5 and j <= self.board_len-5:
                    row = [i + x for x in range(5)]
                    col = [j + x for x in range(5)]
                    if np.all(self.__state_mat[row, col] == self.BLACK):
                        return True, self.BLACK
                    if np.all(self.__state_mat[row, col] == self.WHITE):
                        return True, self.WHITE
        return False, None

    def __updateAvailablePos(self):
        """ 更新当前可落子区域 """
        rows, cols = np.where(self.__state_mat == self.EMPTY)
        self.__available_poses = [(i, j) for i, j in zip(rows, cols)]


class ColorError(ValueError):
    """ 棋子颜色值错误异常 """

    def __init__(self) -> None:
        error_msg = "棋子颜色只能是 `ChessBoard.BLACK` 或 `ChessBoard.WHITE`"
        super().__init__(error_msg)


if __name__ == '__main__':
    chess_board = ChessBoard()
    chess_board.updateBoard((1, 1), -1)
