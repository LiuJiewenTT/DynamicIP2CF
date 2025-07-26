from typing import Union

from PySide6.QtGui import QFontMetrics, Qt
from PySide6.QtWidgets import QMainWindow, QLabel


class MyQWindowHelper(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

    def setWH(self, w: int, h: int):
        # 获取当前窗口的位置
        current_geometry = self.geometry()
        x = current_geometry.x()
        y = current_geometry.y()
        # 设置新的窗口尺寸
        self.setGeometry(x, y, w, h)

    def setWidth(self, w: int):
        # 获取当前窗口的位置
        current_geometry = self.geometry()
        x = current_geometry.x()
        y = current_geometry.y()
        h = current_geometry.height()
        # 设置新的窗口宽度
        self.setGeometry(x, y, w, h)

    def setHeight(self, h: int):
        # 获取当前窗口的位置
        current_geometry = self.geometry()
        x = current_geometry.x()
        y = current_geometry.y()
        w = current_geometry.width()
        # 设置新的窗口高度
        self.setGeometry(x, y, w, h)

    def setWindowPos(self, x: int=0, y: int=0, macro: Union[str, None]=None):
        # 获取当前窗口的尺寸
        current_geometry = self.geometry()
        w = current_geometry.width()
        h = current_geometry.height()
        if macro is not None:
            if macro == 'center':
                # 获取屏幕尺寸
                screen_geometry = self.screen().geometry()
                # 获取屏幕中心坐标
                center_x = screen_geometry.width() // 2
                center_y = screen_geometry.height() // 2
                # 设置窗口居中
                self.move(center_x - w // 2, center_y - h // 2)
            elif macro == 'topleft':
                # 设置窗口在左上角
                self.move(x, y)
            elif macro == 'topright':
                # 设置窗口在右上角
                screen_geometry = self.screen().geometry()
                self.move(screen_geometry.width() - w - x, y)
            elif macro == 'bottomleft':
                # 设置窗口在左下角
                screen_geometry = self.screen().geometry()
                self.move(x, screen_geometry.height() - h - y)
            elif macro == 'bottomright':
                # 设置窗口在右下角
                screen_geometry = self.screen().geometry()
                self.move(screen_geometry.width() - w - x, screen_geometry.height() - h - y)
        else:
            # 设置窗口位置
            self.move(x, y)


class SmartLabel(QLabel):
    def __init__(self, parent=None, max_width=400, char_limit=200):
        super().__init__(parent=parent)
        self.max_width = max_width
        self.char_limit = char_limit
        self.setWordWrap(True)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setStyleSheet("background: rgba(255,255,255,0); border: none;")

    def setSmartText(self, text: str):
        metrics = QFontMetrics(self.font())
        text_width = metrics.horizontalAdvance(text)

        if len(text) <= self.char_limit and text_width < self.max_width:
            self.setWordWrap(False)
            self.setFixedWidth(text_width + 10)
        else:
            self.setWordWrap(True)
            self.setFixedWidth(self.max_width)

        self.setText(text)