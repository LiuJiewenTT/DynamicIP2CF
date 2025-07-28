from typing import List, Tuple

import requests
from PySide6.QtCore import QSize
from PySide6.QtGui import Qt, QPixmap, QPalette, QBrush
from PySide6.QtWidgets import QWidget

from DynamicIP2CF import programinfo


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


def adjust_widget_size_recursively(widget: QWidget):
    while widget is not None:
        widget.adjustSize()
        widget = widget.parentWidget()


# 版本号比较，例如：v1.2.3 > v1.2.2
def compare_version(version1: str, version2: str) -> int:
    """
    比较两个版本号的大小，返回1表示version1大于version2，-1表示version1小于version2，0表示相等。
    :param version1:
    :param version2:
    :return: 1, 0, -1
    """
    v1 = version1.split('.')
    v2 = version2.split('.')
    for i in range(max(len(v1), len(v2))):
        n1 = int(v1[i]) if i < len(v1) else 0
        n2 = int(v2[i]) if i < len(v2) else 0
        if n1 > n2:
            return 1
        elif n1 < n2:
            return -1
    return 0


def fetch_newest_version_info() -> Tuple[str, int, str]:
    """
    获取最新版本信息
    :return: 最新版本信息，状态码，响应详细信息
    """
    # 使用Github API获取最新版本的tag信息

    fetch_url = programinfo.product_check_update_url
    response = requests.get(fetch_url)
    if response.status_code == 200:
        data = response.json()
        tag_name = data['tag_name']
        return tag_name, 200, ''
    else:
        return '', response.status_code, response.text


def check_update_available() -> Tuple[bool, str, int, str]:
    """
    检查是否有新版本可用
    :return: 是否有新版本可用，最新版本号，状态码，响应详细信息
    """
    current_version = programinfo.program_version_str
    newest_version, status_code, response_text = fetch_newest_version_info()
    if newest_version == '' or status_code != 200:
        return False, '', status_code, response_text
    else:
        return compare_version(newest_version, current_version) > 0, newest_version, status_code, response_text

