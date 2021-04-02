# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from app.View.main_window import MainWindow

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
alpha_gobnag_zero = MainWindow()
alpha_gobnag_zero.show()
sys.exit(app.exec_())