# coding:utf-8
from app.common.auto_wrap import autoWrap
from PyQt5.QtCore import pyqtSignal, QFile
from PyQt5.QtWidgets import QLabel,QPushButton

from .mask_dialog_base import MaskDialogBase


class MessageDialog(MaskDialogBase):
    """ 消息对话框 """

    yesSignal = pyqtSignal()
    cancelSignal = pyqtSignal()

    def __init__(self, title: str, content: str, parent):
        super().__init__(parent=parent)
        self.content = content
        self.titleLabel = QLabel(title, self.widget)
        self.contentLabel = QLabel(content, self.widget)
        self.yesButton = QPushButton(self.tr('OK'), self.widget)
        self.cancelButton = QPushButton(self.tr('Cancel'), self.widget)
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.windowMask.resize(self.size())
        self.widget.setMaximumWidth(675)
        self.titleLabel.move(30, 30)
        self.contentLabel.move(30, 70)
        self.contentLabel.setText(autoWrap(self.content, 71)[0])
        # 设置层叠样式和布局
        self.__setQss()
        self.__initLayout()
        # 信号连接到槽
        self.yesButton.clicked.connect(self.__onYesButtonClicked)
        self.cancelButton.clicked.connect(self.__onCancelButtonClicked)

    def __initLayout(self):
        """ 初始化布局 """
        self.contentLabel.adjustSize()
        self.widget.setFixedSize(60+self.contentLabel.width(),
                                 self.contentLabel.y() + self.contentLabel.height()+115)
        self.yesButton.resize((self.widget.width() - 68) // 2, 40)
        self.cancelButton.resize(self.yesButton.width(), 40)
        self.yesButton.move(30, self.widget.height()-70)
        self.cancelButton.move(
            self.widget.width()-30-self.cancelButton.width(), self.widget.height()-70)

    def __onCancelButtonClicked(self):
        self.cancelSignal.emit()
        self.close()

    def __onYesButtonClicked(self):
        self.yesSignal.emit()
        self.close()

    def __setQss(self):
        """ 设置层叠样式 """
        self.windowMask.setObjectName('windowMask')
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

        f = QFile(':/qss/mask_dialog.qss')
        f.open(QFile.ReadOnly)
        self.setStyleSheet(str(f.readAll(), encoding='utf-8'))
        f.close()
