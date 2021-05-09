# coding:utf-8
import sys
import json

from PyQt5.QtWidgets import QApplication

from app.View.flat_chess_board_interface import FlatChessBoardInterface


# 读入棋谱
with open('log\\games.json', 'r', encoding='utf-8') as f:
    games = json.load(f)

# 创建界面
app = QApplication(sys.argv)
window = FlatChessBoardInterface()
window.show()

# 绘制棋谱
for i, game in enumerate(games, 1):
    window.clearBoard()
    window.drawGame(game)
    window.save(fr'docs\chess_manual\{i}.png')

sys.exit(app.exec_())
