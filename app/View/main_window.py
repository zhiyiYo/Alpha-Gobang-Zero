# coding: utf-8
import numpy as np
from app.common.ai_thread import AIThread
from app.common.chess_board import ChessBoard
from app.components.chess import Chess
from app.components.continue_game_dialog import ContinueGameDialog
from app.components.state_tooltip import StateTooltip
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QBrush, QCursor, QIcon, QMouseEvent, QPalette, QPixmap
from PyQt5.QtWidgets import QWidget, qApp


class MainWindow(QWidget):
    """ 主界面 """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.board_len = 9
        self.chessBoard = ChessBoard(self.board_len)
        self.aiThread = AIThread(self.chessBoard, ChessBoard.WHITE, self)
        self.chess_list = []
        self.isAllowPlayerPutChess = True
        self.isEnableAI = True
        self.pre_white_chess = None
        # 初始化
        self.initWidget()

    def initWidget(self):
        """ 初始化窗口 """
        self.setFixedSize(540, 540)
        self.setWindowTitle('BangGo')
        self.setWindowIcon(QIcon(r'app\resource\images\icon.jpeg'))
        # 设置背景图像
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(
            r'app\resource\images\chessboard_1.png')))
        self.setPalette(palette)
        # 设置光标
        self.setCursor(QCursor(QPixmap(r'app\resource\images\black.png').scaled(
            20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        # 信号连接到槽函数
        self.aiThread.searchComplete.connect(self.searchCompleteSlot)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """ 鼠标按下后放置棋子 """
        # AI还在思考就直接返回
        if not self.isAllowPlayerPutChess:
            return
        self.isEnableAI = True
        # 计算棋子在矩阵上的坐标
        cor = self.mapQPoint2MatIndex(e.pos())
        updateOK = self.putChess(cor, ChessBoard.BLACK)
        if updateOK and self.isEnableAI:
            self.stateTooltip = StateTooltip("AI 正在思考中", "客官请耐心等待哦~~", self)
            self.stateTooltip.raise_()
            self.stateTooltip.show()
            self.isAllowPlayerPutChess = False
            self.aiThread.start()

    def mapQPoint2MatIndex(self, pos: QPoint):
        """ 将桌面坐标映射到矩阵下标 """
        poses = np.array([[QPoint(i, j)*60 + QPoint(30, 30) for j in range(self.board_len)]
                          for i in range(self.board_len)])
        # Qt坐标系与矩阵的相反
        distances = np.array([
            [(poses[i, j].x()-pos.x())**2 + (poses[i, j].y()-pos.y())**2
             for j in range(self.board_len)] for i in range(self.board_len)
        ])
        col, row = np.where(distances == distances.min())
        return row[0], col[0]

    def putChess(self, corordinate: tuple, color):
        """ 在棋盘上放置棋子

        Parameters
        ----------
        corordinate: tuple
            棋子的坐标，范围为 `(0, board_len-1) ~ (0, board_len-1)`

        color: int
            棋子的颜色

        Returns
        -------
        updateOK: bool
            成功更新棋盘
        """
        # 矩阵的行和列
        row, col = corordinate
        updateOk = self.chessBoard.updateBoard(corordinate, color)
        if updateOk:
            isWhite = color == ChessBoard.WHITE
            # 矩阵的 axis = 0 方向为 y 轴方向
            chessPos = QPoint(col, row) * 60 + QPoint(11, 13)
            chess = Chess(color, self, isWhite)
            chess.show()
            chess.move(chessPos)
            self.chess_list.append(chess)
            # 取消上一个白棋的提示状态
            if self.pre_white_chess:
                self.pre_white_chess.tipLabel.hide()
            self.pre_white_chess = chess if isWhite else None
            # 检查游戏是否结束
            self.checkGameOver()
        return updateOk

    def searchCompleteSlot(self, action: int):
        """ AI 思考完成槽函数 """
        self.stateTooltip.setState(True)
        pos = (action//self.board_len, action % self.board_len)
        self.putChess(pos, ChessBoard.WHITE)
        self.isAllowPlayerPutChess = True

    def checkGameOver(self):
        """ 检查游戏是否结束 """
        # 锁住 AI
        self.isEnableAI = False
        isOver, winner = self.chessBoard.isGameOver()
        if not isOver:
            self.isEnableAI = True  # 解锁
            return
        if winner == ChessBoard.BLACK:
            msg = '恭喜客官赢得比赛，AI 表示不服，要不再战一局?'
        else:
            msg = '客官别气馁，可以再试一次哦~~'
        continueGameDiaglog = ContinueGameDialog('游戏结束', msg, self)
        continueGameDiaglog.exitGameSignal.connect(qApp.exit)
        continueGameDiaglog.continueGameSignal.connect(self.restartGame)
        continueGameDiaglog.exec_()

    def restartGame(self):
        """ 重新开始游戏 """
        self.chessBoard.clearBoard()
        for chess in self.chess_list:
            chess.deleteLater()
        self.chess_list.clear()

    def exitGame(self):
        """ 退出游戏 """
        qApp.exit()
