# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtWidgets import QApplication
from app.View.main_window import MainWindow

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

# 设置语言
translator = QTranslator()
translator.load(QLocale.system(), ':/i18n/AlphaGobangZero_')
app.installTranslator(translator)

# 创建主界面
w = MainWindow(board_len=9)
w.show()

sys.exit(app.exec_())
