# coding: utf-8
import json
import os

from app.components.label import ClickableLabel
from app.components.scroll_area import ScrollArea
from app.components.slider import Slider
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (QCheckBox, QHBoxLayout, QLabel, QPushButton,
                             QRadioButton, QWidget)
from torch import cuda

from .select_model_dialog import SelectModelDialog


class SettingInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.config = self.__readConfig()
        self.hBoxLayout = QHBoxLayout(self)
        self.scrollWidget = QWidget(self)
        self.scrollArea = ScrollArea()
        self.useGPUCheckBox = QCheckBox(self.scrollWidget)
        self.useGPULabel = QLabel('显卡', self.scrollWidget)
        self.firstHandLabel = QLabel('先手', self.scrollWidget)
        self.mctsLabel = QLabel('蒙特卡洛树', self.scrollWidget)
        self.humanButton = QRadioButton('人类', self.scrollWidget)
        self.cPuctLabel = QLabel('调整探索常数', self.scrollWidget)
        self.AIButton = QRadioButton('阿尔法狗', self.scrollWidget)
        self.cPuctSlider = Slider(Qt.Horizontal, self.scrollWidget)
        self.aboutAppLabel = QLabel('关于此应用', self.scrollWidget)
        self.giveIssueButton = QPushButton('发送反馈', self.scrollWidget)
        self.mctsIterTimeLabel = QLabel('调整搜索次数', self.scrollWidget)
        self.mctsIterTimeSlider = Slider(Qt.Horizontal, self.scrollWidget)
        self.modelInPCLabel = QLabel('此 PC 上的阿尔法狗', self.scrollWidget)
        self.appInfoLabel = QLabel('Alpha Gobang Zero v1.0', self.scrollWidget)
        # QSlider 不能设置浮点数，先扩大十倍
        self.cPuctValueLabel = QLabel(
            str(self.config.get('c_puct', 40)), self.scrollWidget)
        self.mctsIterTimeValueLabel = QLabel(
            str(self.config.get('n_mcts_iters', 1500)), self.scrollWidget)
        self.useGPUTipsLabel = QLabel(
            '使用 GPU 加速阿尔法狗的思考(如可用)', self.scrollWidget)
        self.selectModelLabel = ClickableLabel('选择阿尔法狗的位置', self.scrollWidget)
        self.__initWidget()

    def __initWidget(self):
        """ 初始化界面 """
        self.resize(700, 700)
        self.scrollWidget.resize(540, 900)
        self.giveIssueButton.resize(94, 40)
        self.cPuctValueLabel.setMinimumWidth(50)
        self.scrollArea.setWidget(self.scrollWidget)
        self.hBoxLayout.addWidget(self.scrollArea)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        # 选择模型文件
        self.modelInPCLabel.move(30, 30)
        self.selectModelLabel.move(30, 138-60)
        # 使用 GPU 加速
        self.useGPULabel.move(30, 198-60)
        self.useGPUTipsLabel.move(30, 240-60)
        self.useGPUCheckBox.move(30, 270-60)
        # 先手后手
        self.firstHandLabel.move(30, 330-60)
        self.humanButton.move(30, 380-60)
        self.AIButton.move(30, 420-60)
        # 蒙特卡洛树参数
        self.mctsLabel.move(30, 480-60)
        self.cPuctLabel.move(30, 526-60)
        self.cPuctSlider.move(30, 556-60)
        self.cPuctValueLabel.move(230, 556-60)
        self.mctsIterTimeLabel.move(30, 590-60)
        self.mctsIterTimeSlider.move(30, 620-60)
        self.mctsIterTimeValueLabel.move(230, 620-60)
        # 关于此应用
        self.aboutAppLabel.move(30, 680-60)
        self.appInfoLabel.move(30, 722-60)
        self.giveIssueButton.move(30, 780-60)
        # 初始化 GPU 复选框
        isUseGPU = self.config.get('is_use_gpu', False) and cuda.is_available()
        self.useGPUCheckBox.setText('开' if isUseGPU else '关')
        self.useGPUCheckBox.setChecked(isUseGPU)
        self.useGPUCheckBox.setEnabled(cuda.is_available())
        # 初始化滑动条
        self.cPuctSlider.setRange(5, 200)
        self.cPuctSlider.setSingleStep(5)
        self.mctsIterTimeSlider.setSingleStep(50)
        self.mctsIterTimeSlider.setRange(1000, 3000)
        self.cPuctSlider.setValue(10*self.config.get('c_puct', 4))
        self.mctsIterTimeSlider.setValue(self.config.get('n_mcts_iters', 1500))
        # 初始化先手单选框
        isHumanFirst = self.config.get('is_human_first', True)
        self.humanButton.setChecked(isHumanFirst)
        self.humanButton.setChecked(not isHumanFirst)
        # 设置层叠样式
        self.mctsLabel.setObjectName('titleLabel')
        self.useGPULabel.setObjectName('titleLabel')
        self.aboutAppLabel.setObjectName('titleLabel')
        self.firstHandLabel.setObjectName('titleLabel')
        self.modelInPCLabel.setObjectName('titleLabel')
        self.selectModelLabel.setObjectName("clickableLabel")
        self.__setQss()
        # 信号连接到槽
        self.__connectSignalToSlot()

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r'app\resource\qss\setting_interface.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __readConfig(self) -> dict:
        """ 读入配置 """
        self.__checkDir()
        if not os.path.exists('app\config\config.json'):
            config = {
                "c_puct": 4,
                "is_use_gpu": False,
                "n_mcts_iters": 1500,
                "is_human_first": True,
                "model": "model\\best_policy_value_net.pth"
            }
            return config
        with open('app\config\config.json', encoding='utf-8') as f:
            return json.load(f)

    def __checkDir(self):
        """ 检查配置文件夹是否存在 """
        if not os.path.exists('app\config'):
            os.mkdir('app\config')

    def __showSelectModelDialog(self):
        """ 显示选择模型对话框 """
        dialog = SelectModelDialog(self.config['model'], self.window())
        dialog.modelChangedSignal.connect(self.__modelChangedSlot)
        dialog.exec_()

    def __connectSignalToSlot(self):
        """ 信号连接到槽 """
        self.cPuctSlider.valueChanged.connect(self.__adjustCPuct)
        self.selectModelLabel.clicked.connect(self.__showSelectModelDialog)
        self.useGPUCheckBox.stateChanged.connect(self.__useGPUChangedSlot)
        self.humanButton.clicked.connect(self.__firstHandChangedSlot)
        self.AIButton.clicked.connect(self.__firstHandChangedSlot)
        self.mctsIterTimeSlider.valueChanged.connect(
            self.__adjustMctsIterTimer)
        self.giveIssueButton.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl('https://github.com/zhiyiYo/Alpha-Gobang-Zero')))

    def __modelChangedSlot(self, model: str):
        """ 模型改变信号槽函数 """
        if model != self.config['model']:
            self.config['model'] = model

    def __useGPUChangedSlot(self):
        """ 使用 GPU 加速复选框选中状态改变槽函数 """
        isUse = self.useGPUCheckBox.isChecked()
        self.config['is_use_gpu'] = isUse
        self.useGPUCheckBox.setText('开' if isUse else '关')

    def __firstHandChangedSlot(self):
        """ 先手改变 """
        self.config['is_human_first'] = self.humanButton.isChecked()

    def __adjustCPuct(self, cPuct: float):
        """ 调整探索常数槽函数 """
        self.config['c_puct'] = cPuct/10
        self.cPuctValueLabel.setText(str(cPuct/10))

    def __adjustMctsIterTimer(self, iterTime: int):
        """ 调整蒙特卡洛树搜索次数槽函数 """
        self.config['n_mcts_iters'] = iterTime
        self.mctsIterTimeValueLabel.setNum(iterTime)

    def saveConfig(self):
        """ 保存设置 """
        self.__checkDir()
        with open('app\config\config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f)
