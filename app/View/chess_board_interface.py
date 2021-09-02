# coding:utf-8
from typing import List

import numpy as np
from alphazero.chess_board import ChessBoard
from app.common.ai_thread import AIThread
from app.components.chesses.chess import Chess
from app.components.widgets.menu import ChessBoardMenu
from app.components.dialogs.message_dialog import MessageDialog
from app.components.state_tooltip import StateTooltip
from PyQt5.QtCore import QPoint, QRect, Qt, pyqtSignal
from PyQt5.QtGui import (QBrush, QCursor, QMouseEvent, QPainter, QPen, QPixmap,
                         QResizeEvent, QContextMenuEvent)
from PyQt5.QtWidgets import QWidget


class ChessBoardInterface(QWidget):
    """ 棋盘界面 """

    exitGameSignal = pyqtSignal()
    restartGameSignal = pyqtSignal()
    switchToSettingInterfaceSignal = pyqtSignal()

    def __init__(self, model, c_puct=5, n_mcts_iters=1500, is_human_first=True,
                 is_use_gpu=True, boardLen=9, margin=37, gridSize=78, parent=None):
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

        boardLen: int
            棋盘大小

        margin: int
            棋盘边距

        gridSize: int
            网格大小

        parent:
            父级窗口
        """
        super().__init__(parent=parent)
        self.chess_list = []  # type: List[Chess]
        self.margin = margin
        self.isEnableAI = True
        self.boardLen = boardLen
        self.gridSize = gridSize
        self.isUseGPU = is_use_gpu
        self.isAIThinking = False
        self.previousAIChess = None
        self.stateTooltip = None
        self.isHumanFirst = is_human_first
        self.contextMenu = ChessBoardMenu(self)
        self.chessBoard = ChessBoard(self.boardLen, n_feature_planes=6)
        self.aiThread = AIThread(
            self.chessBoard, model, c_puct, n_mcts_iters, is_use_gpu, parent=self)
        self.humanColor = ChessBoard.BLACK if is_human_first else ChessBoard.WHITE
        self.AIColor = ChessBoard.BLACK if not is_human_first else ChessBoard.WHITE
        self.__initWidget()

    def __initWidget(self):
        """ 初始化界面 """
        size = 2*self.margin + (self.boardLen-1)*self.gridSize
        self.setMinimumSize(size, size)
        self.setMouseTracking(True)
        # 信号连接到槽函数
        self.__connectSignalToSlot()
        if not self.isHumanFirst:
            self.__getAIAction()

    def paintEvent(self, e):
        """ 绘制棋盘 """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        # 绘制网格
        left, top = self.__getMargin()
        for i in range(self.boardLen):
            x = y = self.margin + i*self.gridSize
            x = left + i*self.gridSize
            y = top + i*self.gridSize
            # 竖直线
            width = 2 if i in [0, self.boardLen-1] else 1
            painter.setPen(QPen(Qt.black, width))
            painter.drawLine(x, top, x, self.height()-top)
            # 水平线
            painter.drawLine(left, y, self.width()-left-1, y)

        # 绘制圆点
        painter.setBrush(QBrush(Qt.black))
        painter.setPen(Qt.NoPen)
        r = 6
        x = self.width()//2-r
        y = self.height()//2-r
        painter.drawEllipse(x, y, 2*r, 2*r)
        for pos in [(-1, -1), (1, -1), (-1, 1), (1, 1)]:
            x_ = self.gridSize*pos[0]*(self.boardLen-1)//2/2 + x
            y_ = self.gridSize*pos[1]*(self.boardLen-1)//2/2 + y
            painter.drawEllipse(x_, y_, 2*r, 2*r)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        """ 鼠标按下后放置棋子 """
        # AI还在思考就直接返回
        if self.isAIThinking or e.button() == Qt.RightButton or \
                e.pos() not in self.__getChessRegion():
            return

        self.isEnableAI = True

        # 计算棋子在矩阵上的坐标
        cor = self.__mapQPoint2MatIndex(e.pos())
        updateOK = self.__putChess(cor, self.humanColor)
        if updateOK and self.isEnableAI:
            self.__getAIAction()

    def __getAIAction(self):
        """ 获取 AI 的动作 """
        title = self.tr('AI is thinking')
        content = self.tr("Please wait patiently...")
        self.stateTooltip = StateTooltip(title, content, self.window())
        self.stateTooltip.move(
            self.window().width() - self.stateTooltip.width() - 63, 60)
        self.stateTooltip.raise_()
        self.stateTooltip.show()
        self.isAIThinking = True
        self.aiThread.start()

    def __mapQPoint2MatIndex(self, pos: QPoint):
        """ 将桌面坐标映射到矩阵下标 """
        n = self.boardLen
        left, top = self.__getMargin()
        poses = np.array([[[i*self.gridSize+left, j*self.gridSize+top] for j in range(n)]
                         for i in range(n)])
        # Qt坐标系与矩阵的相反
        distances = (poses[:, :, 0]-pos.x())**2+(poses[:, :, 1]-pos.y())**2
        col, row = np.where(distances == distances.min())
        return row[0], col[0]

    def __putChess(self, pos: tuple, color):
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
            chess = Chess(color, self, isAIChess)
            left, top = self.__getMargin()
            chessPos = QPoint(col, row) * self.gridSize + \
                QPoint(left-20, top-20)
            chess.show()
            chess.move(chessPos)
            self.chess_list.append(chess)

            # 取消上一个白棋的提示状态
            if self.previousAIChess:
                self.previousAIChess.tipLabel.hide()
            self.previousAIChess = chess if isAIChess else None

            # 检查游戏是否结束
            self.__checkGameOver()

        return updateOk

    def __searchCompleteSlot(self, action: int):
        """ AI 思考完成槽函数 """
        self.stateTooltip.setState(True)
        pos = (action//self.boardLen, action % self.boardLen)
        self.isAIThinking = False
        self.stateTooltip = None
        self.__putChess(pos, self.AIColor)

    def __checkGameOver(self):
        """ 检查游戏是否结束 """
        # 锁住 AI
        self.isEnableAI = False
        isOver, winner = self.chessBoard.is_game_over()
        if not isOver:
            self.isEnableAI = True  # 解锁
            return

        title=self.tr('Game over')
        if winner == self.humanColor:
            msg = self.tr("Congratulations on winning the game. AI said"
                          " he didn't accept it. Why don't we fight another game?")
        elif winner == self.AIColor:
            msg = self.tr("Don't be discouraged. You can try again")
        else:
            msg = self.tr("it ends in a draw! Sure enough, the chessboard"
                          " is too small to play. Why don't you fight another game?")

        continueGameDiaglog = MessageDialog(title, msg, self.window())
        continueGameDiaglog.cancelSignal.connect(self.exitGameSignal)
        continueGameDiaglog.yesSignal.connect(self.__restartGame)
        continueGameDiaglog.exec_()

    def __setCursor(self, isChess=True):
        """ 设置光标 """
        if isChess:
            color = 'black' if self.isHumanFirst else 'white'
            self.setCursor(QCursor(QPixmap(f':/images/chess_board_interface/{color}.png').scaled(
                20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        else:
            self.setCursor(Qt.ArrowCursor)

    def __restartGame(self):
        """ 重新开始游戏 """
        if self.isAIThinking:
            return
        self.restartGameSignal.emit()
        self.chessBoard.clear_board()
        for chess in self.chess_list:
            chess.deleteLater()
        self.chess_list.clear()
        self.previousAIChess = None
        if not self.isHumanFirst:
            self.__getAIAction()

    def updateGameConfig(self, config: dict):
        """ 更新游戏参数 """
        self.aiThread.setModel(**config)
        self.isHumanFirst = config.get('is_human_first', True)
        self.isUseGPU = config.get('is_use_gpu', False)
        self.humanColor = ChessBoard.BLACK if self.isHumanFirst else ChessBoard.WHITE
        self.AIColor = ChessBoard.BLACK if not self.isHumanFirst else ChessBoard.WHITE
        self.__setCursor()

    def __getMargin(self):
        """ 获取棋盘边距 """
        left = (self.width() - (self.boardLen-1)*self.gridSize)//2
        top = (self.height() - (self.boardLen-1)*self.gridSize)//2
        return left, top

    def resizeEvent(self, e: QResizeEvent) -> None:
        """ 移动棋子位置 """
        # 调整棋子位置
        size = (self.size()-e.oldSize())/2
        for chess in self.chess_list:
            chess.move(chess.pos()+QPoint(size.width(), size.height()))
        # 调整气泡位置
        if self.stateTooltip:
            self.stateTooltip.move(
                self.window().width() - self.stateTooltip.width() - 63, 60)

    def __getChessRegion(self):
        """ 返回棋盘区域 """
        left, top = self.__getMargin()
        rect = QRect(left-20, top-20, self.width() -
                     2*left+40, self.height()-2*top+40)
        return rect

    def mouseMoveEvent(self, e: QMouseEvent):
        """ 鼠标移动改变光标 """
        self.__setCursor(e.pos() in self.__getChessRegion())

    def contextMenuEvent(self, e: QContextMenuEvent):
        """ 显示右击菜单 """
        self.contextMenu.exec_(e.globalPos())

    def __connectSignalToSlot(self):
        """ 信号连接到槽 """
        self.aiThread.searchComplete.connect(self.__searchCompleteSlot)
        self.contextMenu.restartGameAct.triggered.connect(self.__restartGame)
        self.contextMenu.settingAct.triggered.connect(
            self.switchToSettingInterfaceSignal)

    def closeEvent(self, e):
        """ 关闭界面 """
        self.aiThread.quit()
        self.aiThread.wait()
        self.aiThread.deleteLater()
        e.accept()
