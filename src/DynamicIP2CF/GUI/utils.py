from typing import List, Tuple, Dict, Union, Callable
from urllib.parse import urlparse

import requests
from PySide6.QtCore import QSize
from PySide6.QtGui import Qt, QPixmap, QPalette, QBrush
from PySide6.QtWidgets import QWidget, QComboBox

import R
from DynamicIP2CF import programinfo
from NetToolKit.local_info import host_matches_override


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


def fetch_newest_version_info(proxies: Union[Dict[str, str], None]=None, proxy_override: Union[List[str], None]=None) -> Tuple[str, int, str]:
    """
    获取最新版本信息
    :return: 最新版本信息，状态码，响应详细信息
    """
    # 使用Github API获取最新版本的tag信息

    fetch_url = programinfo.product_check_update_url
    parsed = urlparse(fetch_url)
    host = parsed.hostname.lower()

    session = requests.Session()

    if proxies and not host_matches_override(host, proxy_override):
        used_proxies = proxies
    else:
        used_proxies = None  # 禁止用代理
        session.trust_env = False
    response = session.get(fetch_url, proxies=used_proxies)
    if response.status_code == 200:
        data = response.json()
        tag_name = data['tag_name']
        return tag_name, 200, ''
    else:
        return '', response.status_code, response.text


def check_update_available(proxies=None, proxy_override=None) -> Tuple[bool, str, int, str]:
    """
    检查是否有新版本可用
    :return: 是否有新版本可用，最新版本号，状态码，响应详细信息
    """
    current_version = programinfo.program_version_str
    newest_version, status_code, response_text = fetch_newest_version_info(proxies=proxies, proxy_override=proxy_override)
    if newest_version == '' or status_code != 200:
        return False, '', status_code, response_text
    else:
        return compare_version(newest_version, current_version) > 0, newest_version, status_code, response_text


language_names_from_locales: Dict[str, str] = {
    'zh_CN': '简体中文',
    'en_US': 'English (US)'
}


def get_language_name_from_locale(locale: str) -> str:
    return language_names_from_locales.get(locale, locale)


def get_locale_from_language_name(language_name: str) -> str:
    for locale, name in language_names_from_locales.items():
        if name == language_name:
            return locale
    return ""


def create_language_combo_box(parent):
    func_1: Callable[[str], str] = lambda x: get_language_name_from_locale(x)

    language_combo_box = QComboBox(parent)
    language_combo_box.addItem(R.string.gui.configure_dialog.misc_settings_tab.language_group.language_use_default)
    language_combo_box.addItem(func_1('zh_CN'))
    language_combo_box.addItem(func_1('en_US'))
    return language_combo_box
