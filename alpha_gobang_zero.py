# coding:utf-8
import sys

from PyQt5.QtWidgets import QApplication

from app.View.main_window import MainWindow
from config.config import game_config

app = QApplication(sys.argv)
alpha_gobnag_zero = MainWindow(**game_config)
alpha_gobnag_zero.show()
sys.exit(app.exec_())
