# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtWidgets import QApplication
from app.View.main_window import MainWindow
from app.common.os_utils import getDevicePixelRatio

# 启用高分屏缩放
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
os.environ["QT_SCALE_FACTOR"] = str(max(1, getDevicePixelRatio()-0.25))
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

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
