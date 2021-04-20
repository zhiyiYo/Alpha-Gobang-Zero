# coding:utf-8
from app.components.widgets.button import ThreeStateToolButton
from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QLabel, QWidget, QGraphicsDropShadowEffect


class StateTooltip(QWidget):
    """ 进度提示框 """

    closedSignal = pyqtSignal()

    def __init__(self, title="", content="", parent=None):
        """
        Parameters
        ----------
        title: str
            状态气泡标题

        content: str
            状态气泡内容

        parant:
            父级窗口
        """
        super().__init__(parent)
        self.title = title
        self.content = content
        # 实例化小部件
        self.__createWidgets()
        # 初始化参数
        self.isDone = False
        self.rotateAngle = 0
        self.deltaAngle = 20
        # 初始化
        self.__initWidget()

    def __createWidgets(self):
        """ 创建小部件 """
        icon_path = {
            "normal": r"app\resource\images\state_tooltip\stateToolTip_closeBt_normal_14_14.png",
            "hover": r"app\resource\images\state_tooltip\stateToolTip_closeBt_hover_14_14.png",
            "pressed": r"app\resource\images\state_tooltip\stateToolTip_closeBt_hover_14_14.png",
        }

        self.titleLabel = QLabel(self.title, self)
        self.contentLabel = QLabel(self.content, self)
        self.rotateTimer = QTimer(self)
        self.closeTimer = QTimer(self)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.busyImage = QPixmap(
            r"app\resource\images\state_tooltip\running_22_22.png"
        )
        self.doneImage = QPixmap(
            r"app\resource\images\state_tooltip\complete_20_20.png"
        )
        self.closeButton = ThreeStateToolButton(icon_path, (14, 14), self)

    def __initWidget(self):
        """ 初始化小部件 """
        self.setFixedSize(240, 64)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_StyledBackground)
        self.rotateTimer.setInterval(50)
        self.closeTimer.setInterval(1000)
        self.contentLabel.setMinimumWidth(200)
        # 分配ID
        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")
        # 将信号连接到槽函数
        self.closeButton.clicked.connect(self.hide)
        self.rotateTimer.timeout.connect(self.__rotateTimerFlowSlot)
        self.closeTimer.timeout.connect(self.__slowlyClose)
        self.__initLayout()
        self.__setQss()
        # 打开定时器
        self.rotateTimer.start()

    def __initLayout(self):
        """ 初始化布局 """
        self.titleLabel.move(39, 11)
        self.contentLabel.move(15, 34)
        self.closeButton.move(self.width() - 29, 23)
        # self.__setShadowEffect()

    def __setQss(self):
        """ 设置层叠样式 """
        with open(r"app\resource\qss\state_tooltip.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

    def setTitle(self, title):
        """ 更新提示框的标题 """
        self.title = title
        self.titleLabel.setText(title)

    def setContent(self, content):
        """ 更新提示框内容 """
        self.content = content
        self.contentLabel.setText(content)

    def setState(self, isDone=False):
        """ 设置运行状态 """
        self.isDone = isDone
        self.update()
        # 运行完成后主动关闭窗口
        if self.isDone:
            self.closeTimer.start()

    def __slowlyClose(self):
        """ 缓慢关闭窗口 """
        self.rotateTimer.stop()
        self.animation.setEasingCurve(QEasingCurve.Linear)
        self.animation.setDuration(500)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.finished.connect(self.deleteLater)
        self.animation.start()

    def __rotateTimerFlowSlot(self):
        """ 定时器溢出时旋转箭头 """
        self.rotateAngle = (self.rotateAngle + self.deltaAngle) % 360
        self.update()

    def paintEvent(self, QPaintEvent):
        """ 绘制背景 """
        super().paintEvent(QPaintEvent)
        # 绘制旋转箭头
        painter = QPainter(self)
        painter.setRenderHints(QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        if not self.isDone:
            painter.translate(24, 20)  # 原点平移到旋转中心
            painter.rotate(self.rotateAngle)  # 坐标系旋转
            painter.drawPixmap(
                -int(self.busyImage.width() / 2),
                -int(self.busyImage.height() / 2),
                self.busyImage,
            )
        else:
            painter.drawPixmap(
                14, 13, self.doneImage.width(), self.doneImage.height(), self.doneImage
            )

    def __setShadowEffect(self):
        """ 添加阴影 """
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(50)
        self.shadowEffect.setOffset(0, 5)
        self.setGraphicsEffect(self.shadowEffect)
