# coding:utf-8
import sys

from PyQt5.QtWidgets import QApplication

from app.View.main_window import MainWindow

app = QApplication(sys.argv)
bang_go = MainWindow()
bang_go.show()
sys.exit(app.exec_())