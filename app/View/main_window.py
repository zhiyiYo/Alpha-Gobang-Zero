# coding: utf-8
import numpy as np
from alphazero import ChessBoard
from app.common.ai_thread import AIThread
from app.components.chess import Chess
from app.components.continue_game_dialog import ContinueGameDialog
from app.components.state_tooltip import StateTooltip
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QBrush, QCursor, QIcon, QMouseEvent, QPalette, QPixmap
from PyQt5.QtWidgets import QWidget, qApp


class MainWindow(QWidget):
    """ 主界面 """

    def __init__(self, model, c_puct=5, n_mcts_iters=1500, is_human_first=True, is_use_gpu=True, parent=None):
        """
        Parameters
        ----------
        model: str
            模型路径

        c_puct: float
            探索常数

        n_mcts_iters: int
            蒙特卡洛树搜索次数

        is_human_first: bool
            是否人类先手

        is_use_gpu: bool
            是否使用 GPU

        parent:
            父级窗口
        """
        super().__init__(parent=parent)
        self.boardLen = 9
        self.chess_list = []
        self.isEnableAI = True
        self.isUseGPU = is_use_gpu
        self.isAllowHumanAct = True
        self.previousAIChess = None
        self.isHumanFirst = is_human_first
        self.chessBoard = ChessBoard(self.boardLen, n_feature_planes=6)
        self.aiThread = AIThread(
            self.chessBoard, model, c_puct, n_mcts_iters, is_use_gpu, self)
        self.humanColor = ChessBoard.BLACK if is_human_first else ChessBoard.WHITE
        self.AIColor = ChessBoard.BLACK if not is_human_first else ChessBoard.WHITE
        # 初始化
        self.initWidget()

    def initWidget(self):
        """ 初始化窗口 """
        self.setFixedSize(540, 540)
        self.setWindowTitle('Alpha Gobang Zero')
        self.setWindowIcon(QIcon(r'app\resource\images\icon\二哈.jpg'))
        # 设置背景图像
        palette = QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(
            r'app\resource\images\chessboard.png')))
        self.setPalette(palette)
        # 设置光标
        color = 'black' if self.isHumanFirst else 'white'
        self.setCursor(QCursor(QPixmap(fr'app\resource\images\{color}.png').scaled(
            20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        # 信号连接到槽函数
        self.aiThread.searchComplete.connect(self.searchCompleteSlot)
        # 如果AI先手就激活AI
        if not self.isHumanFirst:
            self.show()
            self.getAIAction()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """ 鼠标按下后放置棋子 """
        # AI还在思考就直接返回
        if not self.isAllowHumanAct or e.button() == Qt.RightButton:
            return
        self.isEnableAI = True
        # 计算棋子在矩阵上的坐标
        cor = self.mapQPoint2MatIndex(e.pos())
        updateOK = self.putChess(cor, self.humanColor)
        if updateOK and self.isEnableAI:
            self.getAIAction()

    def getAIAction(self):
        """ 获取 AI 的动作 """
        self.stateTooltip = StateTooltip("AI 正在思考中", "客官请耐心等待哦~~", self)
        self.stateTooltip.raise_()
        self.stateTooltip.show()
        self.isAllowHumanAct = False
        self.aiThread.start()

    def mapQPoint2MatIndex(self, pos: QPoint):
        """ 将桌面坐标映射到矩阵下标 """
        n = self.boardLen
        poses = np.array([[[i*60+30, j*60+30] for j in range(n)]
                         for i in range(n)])
        # Qt坐标系与矩阵的相反
        distances = (poses[:, :, 0]-pos.x())**2+(poses[:, :, 1]-pos.y())**2
        col, row = np.where(distances == distances.min())
        return row[0], col[0]

    def putChess(self, pos: tuple, color):
        """ 在棋盘上放置棋子

        Parameters
        ----------
        pos: tuple
            棋子的坐标，范围为 `(0, boardLen-1) ~ (0, boardLen-1)`

        color: int
            棋子的颜色

        Returns
        -------
        updateOK: bool
            成功更新棋盘
        """
        # 矩阵的行和列
        row, col = pos
        updateOk = self.chessBoard.do_action_(pos)
        if updateOk:
            isAIChess = color != self.humanColor
            # 矩阵的 axis = 0 方向为 y 轴方向
            chessPos = QPoint(col, row) * 60 + QPoint(11, 13)
            chess = Chess(color, self, isAIChess)
            chess.show()
            chess.move(chessPos)
            self.chess_list.append(chess)
            # 取消上一个白棋的提示状态
            if self.previousAIChess:
                self.previousAIChess.tipLabel.hide()
            self.previousAIChess = chess if isAIChess else None
            # 检查游戏是否结束
            self.checkGameOver()
        return updateOk

    def searchCompleteSlot(self, action: int):
        """ AI 思考完成槽函数 """
        self.stateTooltip.setState(True)
        pos = (action//self.boardLen, action % self.boardLen)
        self.putChess(pos, self.AIColor)
        self.isAllowHumanAct = True

    def checkGameOver(self):
        """ 检查游戏是否结束 """
        # 锁住 AI
        self.isEnableAI = False
        isOver, winner = self.chessBoard.is_game_over()
        if not isOver:
            self.isEnableAI = True  # 解锁
            return
        if winner == self.humanColor:
            msg = '恭喜客官赢得比赛，AI 表示不服，要不再战一局?'
        elif winner == self.AIColor:
            msg = '客官别气馁，可以再试一次哦~~'
        else:
            msg = '平局！果然棋盘太小，施展不开，要不再战一局？'
        continueGameDiaglog = ContinueGameDialog('游戏结束', msg, self)
        continueGameDiaglog.exitGameSignal.connect(self.exitGame)
        continueGameDiaglog.continueGameSignal.connect(self.restartGame)
        continueGameDiaglog.exec_()

    def restartGame(self):
        """ 重新开始游戏 """
        self.chessBoard.clear_board()
        for chess in self.chess_list:
            chess.deleteLater()
        self.chess_list.clear()
        self.previousAIChess = None

    def exitGame(self):
        """ 退出游戏 """
        qApp.exit()
