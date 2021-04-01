# coding:utf-8
import sys

from PyQt5.QtWidgets import QApplication

from app.View.main_window import MainWindow

app = QApplication(sys.argv)
alpha_gobnag_zero = MainWindow()
alpha_gobnag_zero.show()
sys.exit(app.exec_())
