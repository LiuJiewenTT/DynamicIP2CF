from typing import List, Tuple

from PySide6.QtCore import QSize
from PySide6.QtGui import Qt, QPixmap, QPalette, QBrush
from PySide6.QtWidgets import QWidget


def resize_widget_pixmap(size: QSize, pair: Tuple[QWidget, QPixmap]):
    parentWidget: QWidget
    pixmap: QPixmap
    parentWidget, pixmap = pair
    scaled_pixmap = pixmap.scaled(size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    palette: QPalette = parentWidget.palette()
    palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
    parentWidget.setPalette(palette)


def resize_widgets_pixmap(sizes: List[QSize], pairs: List[Tuple[QWidget, QPixmap]]):
    for size, pair in zip(sizes, pairs):
        resize_widget_pixmap(size, pair)
