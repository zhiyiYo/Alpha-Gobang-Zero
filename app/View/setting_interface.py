# coding: utf-8
import json
import os

from app.components.dialogs.select_model_dialog import SelectModelDialog
from app.components.widgets.label import ClickableLabel
from app.components.widgets.scroll_area import ScrollArea
from app.components.widgets.slider import Slider
from app.components.widgets.switch_button import SwitchButton
from PyQt5.QtCore import QFile, Qt, QUrl, pyqtSignal
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QLabel, QPushButton, QRadioButton, QWidget
from torch import cuda


class SettingInterface(ScrollArea):

    enableAcrylicChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # 默认配置
        self.config = {
            "c_puct": 4,
            "is_use_gpu": True,
            "n_mcts_iters": 1500,
            "is_human_first": True,
            "is_enable_acrylic": True,
            "model": "model/history/best_policy_value_net_4400.pth"
        }
        # 读入用户配置
        self.__readConfig()

        self.scrollWidget = QWidget(self)

        # 此 PC 上的阿尔法狗
        self.modelInPCLabel = QLabel(
            self.tr('Alpha Gobang in this PC'), self.scrollWidget)
        self.selectModelLabel = ClickableLabel(
            self.tr('Choose where we look for Alpha Gobang'), self.scrollWidget)

        # 使用亚克力背景
        self.acrylicLabel = QLabel(
            self.tr("Acrylic Background"), self.scrollWidget)
        self.acrylicHintLabel = QLabel(
            self.tr("Use the acrylic background effect"), self.scrollWidget)
        self.acrylicSwitchButton = SwitchButton(
            self.tr("Off"), self.scrollWidget)

        # 显卡
        self.useGPULabel = QLabel(self.tr('Graphics Card'), self.scrollWidget)
        self.useGPUSwitchButton = SwitchButton(parent=self.scrollWidget)
        self.useGPUHintLabel = QLabel(
            self.tr('Use GPU to speed up Alpha Gobang thinking (if available)'), self.scrollWidget)

        # 先手
        self.firstHandLabel = QLabel(
            self.tr('Offensive Position'), self.scrollWidget)
        self.AIButton = QRadioButton(
            self.tr('Alpha Gobang'), self.scrollWidget)
        self.humanButton = QRadioButton(self.tr('Human'), self.scrollWidget)

        # 蒙特卡洛树
        self.mctsLabel = QLabel(self.tr('Monte Carlo tree'), self.scrollWidget)
        self.mctsIterTimeSlider = Slider(Qt.Horizontal, self.scrollWidget)
        self.cPuctSlider = Slider(Qt.Horizontal, self.scrollWidget)
        self.cPuctLabel = QLabel(
            self.tr('Set exploration constant'), self.scrollWidget)
        self.mctsIterTimeLabel = QLabel(
            self.tr('Set search times'), self.scrollWidget)
        self.cPuctValueLabel = QLabel(
            str(self.config['c_puct']), self.scrollWidget)
        self.mctsIterTimeValueLabel = QLabel(
            str(self.config['n_mcts_iters']), self.scrollWidget)

        # 关于此应用
        self.aboutAppLabel = QLabel(
            self.tr('About this App'), self.scrollWidget)
        self.giveIssueButton = QPushButton(
            self.tr('Send feedback'), self.scrollWidget)
        self.appInfoLabel = QLabel('Alpha Gobang Zero v1.0', self.scrollWidget)

        self.__initWidget()

    def __initWidget(self):
        """ 初始化界面 """
        self.resize(700, 700)
        self.scrollWidget.resize(540, 900)
        self.cPuctValueLabel.setMinimumWidth(50)
        self.setWidget(self.scrollWidget)

        # 选择模型文件
        self.modelInPCLabel.move(30, 30)
        self.selectModelLabel.move(30, 78)

        # 亚克力背景
        self.acrylicLabel.move(30, 138)
        self.acrylicHintLabel.move(30, 180)
        self.acrylicSwitchButton.move(30, 210)

        # 使用 GPU 加速
        self.useGPULabel.move(30, 270)
        self.useGPUHintLabel.move(30, 312)
        self.useGPUSwitchButton.move(30, 342)

        # 先手后手
        self.firstHandLabel.move(30, 402)
        self.humanButton.move(30, 447)
        self.AIButton.move(30, 492)

        # 蒙特卡洛树参数
        self.mctsLabel.move(30, 552)
        self.cPuctLabel.move(30, 598)
        self.cPuctSlider.move(30, 628)
        self.cPuctValueLabel.move(230, 628)
        self.mctsIterTimeLabel.move(30, 662)
        self.mctsIterTimeSlider.move(30, 692)
        self.mctsIterTimeValueLabel.move(230, 692)

        # 关于此应用
        self.aboutAppLabel.move(30, 752)
        self.appInfoLabel.move(30, 794)
        self.giveIssueButton.move(30, 824)

        # 初始化亚克力背景开关按钮
        enableAcrylic = self.config['is_enable_acrylic']
        self.acrylicSwitchButton.setText(
            self.tr('On') if enableAcrylic else self.tr('Off'))
        self.acrylicSwitchButton.setChecked(enableAcrylic)

        # 初始化 GPU 开关按钮
        isUseGPU = self.config['is_use_gpu'] and cuda.is_available()
        self.useGPUSwitchButton.setText(
            self.tr('On') if isUseGPU else self.tr('Off'))
        self.useGPUSwitchButton.setChecked(isUseGPU)
        self.useGPUSwitchButton.setEnabled(cuda.is_available())

        # 初始化滑动条
        self.cPuctSlider.setRange(5, 200)
        self.cPuctSlider.setSingleStep(5)
        self.mctsIterTimeSlider.setSingleStep(50)
        self.mctsIterTimeSlider.setRange(400, 4000)
        self.cPuctSlider.setValue(10 * self.config['c_puct'])
        self.mctsIterTimeSlider.setValue(self.config['n_mcts_iters'])

        # 初始化先手单选框
        isHumanFirst = self.config['is_human_first']
        self.humanButton.setChecked(isHumanFirst)
        self.AIButton.setChecked(not isHumanFirst)

        # 设置层叠样式
        self.__setQss()
        # 信号连接到槽
        self.__connectSignalToSlot()

    def __setQss(self):
        """ 设置层叠样式 """
        self.mctsLabel.setObjectName('titleLabel')
        self.useGPULabel.setObjectName('titleLabel')
        self.acrylicLabel.setObjectName('titleLabel')
        self.aboutAppLabel.setObjectName('titleLabel')
        self.firstHandLabel.setObjectName('titleLabel')
        self.modelInPCLabel.setObjectName('titleLabel')
        self.selectModelLabel.setObjectName("clickableLabel")

        f = QFile(':/qss/setting_interface.qss')
        f.open(QFile.ReadOnly)
        self.setStyleSheet(str(f.readAll(), encoding='utf-8'))
        f.close()

    def __readConfig(self):
        """ 读入配置 """
        self.__checkDir()
        try:
            with open('app/config/config.json', encoding='utf-8') as f:
                self.config.update(json.load(f))
        except:
            pass

    def __checkDir(self):
        """ 检查配置文件夹是否存在 """
        if not os.path.exists('app/config'):
            os.mkdir('app/config')

    def __showSelectModelDialog(self):
        """ 显示选择模型对话框 """
        w = SelectModelDialog(self.config['model'], self.window())
        w.modelChangedSignal.connect(self.__onModelChanged)
        w.exec_()

    def __connectSignalToSlot(self):
        """ 信号连接到槽 """
        self.AIButton.clicked.connect(self.__onFirstHandChanged)
        self.humanButton.clicked.connect(self.__onFirstHandChanged)
        self.cPuctSlider.valueChanged.connect(self.__onCPuctChanged)
        self.selectModelLabel.clicked.connect(self.__showSelectModelDialog)
        self.acrylicSwitchButton.checkedChanged.connect(
            self.__onEnableAcrylicChanged)
        self.useGPUSwitchButton.checkedChanged.connect(
            self.__onUseGPUChanged)
        self.mctsIterTimeSlider.valueChanged.connect(
            self.__onMctsIterTimesChanged)
        self.giveIssueButton.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl('https://github.com/zhiyiYo/Alpha-Gobang-Zero/issues')))

    def __onModelChanged(self, model: str):
        """ 模型改变信号槽函数 """
        if model != self.config['model']:
            self.config['model'] = model

    def __onEnableAcrylicChanged(self, isEnableAcrylic: bool):
        """ 使用亚克力背景开关按钮的开关状态变化槽函数 """
        self.config['is_enable_acrylic'] = isEnableAcrylic
        self.acrylicSwitchButton.setText(
            self.tr('On') if isEnableAcrylic else self.tr('Off'))
        self.enableAcrylicChanged.emit(isEnableAcrylic)

    def __onUseGPUChanged(self, isUseGPU: bool):
        """ 使用 GPU 加速开关按钮的开关状态改变槽函数 """
        self.config['is_use_gpu'] = isUseGPU
        self.useGPUSwitchButton.setText(
            self.tr('On') if isUseGPU else self.tr('Off'))

    def __onFirstHandChanged(self):
        """ 先手改变 """
        self.config['is_human_first'] = self.humanButton.isChecked()

    def __onCPuctChanged(self, cPuct: float):
        """ 调整探索常数槽函数 """
        self.config['c_puct'] = cPuct/10
        self.cPuctValueLabel.setText(str(cPuct/10))

    def __onMctsIterTimesChanged(self, iterTime: int):
        """ 调整蒙特卡洛树搜索次数槽函数 """
        self.config['n_mcts_iters'] = iterTime
        self.mctsIterTimeValueLabel.setNum(iterTime)

    def saveConfig(self):
        """ 保存设置 """
        self.__checkDir()
        with open('app/config/config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f)
