import ipaddress
from typing import List

from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, Signal

import NetToolKit.local_info
from DynamicIP2CF import common
from DynamicIP2CF.utils_toplevel import cf_update_ip


class MainWindow(QMainWindow):
    window_shown = Signal()

    def __init__(self):
        super().__init__()
        self.__init_layout()

        # Init listeners
        self.window_shown.connect(self.__init_shown)

    def showEvent(self, event):
        super().showEvent(event)
        self.window_shown.emit()

    def __init_layout(self):
        self.setWindowTitle("IP Status GUI")
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)

        # Left side list widget
        self.list_widget = QListWidget()
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.list_widget.setFixedWidth(400)  # Adjust width to fit IPv6 address length
        main_layout.addWidget(self.list_widget)

        # Right side layout
        right_side_widget = QWidget()
        right_side_layout = QVBoxLayout(right_side_widget)
        main_layout.addWidget(right_side_widget)

        # Status label
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        right_side_layout.addWidget(status_widget, alignment=Qt.AlignCenter)
        self.status_label_title = QLabel("状态：", alignment=Qt.AlignRight)
        status_layout.addWidget(self.status_label_title)
        self.status_label = QLabel("就绪", alignment=Qt.AlignLeft)
        status_layout.addWidget(self.status_label)

        # Refresh IP list button
        self.refresh_ip_list_button = QPushButton("刷新本机外部IP")
        self.refresh_ip_list_button.clicked.connect(self.refresh_ip_list)
        right_side_layout.addWidget(self.refresh_ip_list_button)

        # Update IP button
        self.update_ip_button = QPushButton("更新IP到DNS")
        self.update_ip_button.clicked.connect(self.update_ip)
        right_side_layout.addWidget(self.update_ip_button)

    def __init_shown(self):
        self.refresh_ip_list()

    def refresh_ip_list(self):
        ip_list = self.get_ip_list()
        self.list_widget.clear()
        for ip in ip_list:
            self.list_widget.addItem(ip)

    def update_status(self, status):
        self.status_label.setText(f"Status: {status}")

    def get_selected_ip(self):
        if self.list_widget.count() == 0:
            return ""

        # 获取选中的条目
        selected_items = self.list_widget.selectedItems()
        if len(selected_items) == 0:
            return ""
        return selected_items[0].text()

    def update_ip(self):
        ip_str = self.get_selected_ip()
        if not ip_str:
            # 没有可用IP
            return

        record_info = common.iniConfigManager.get_record_info()
        record_info['ip'] = ip_str
        ip = ipaddress.ip_address(record_info['ip'])
        if ip.version == 6:
            record_info['ip_version'] = 'v6'
        else:
            record_info['ip_version'] = 'v4'
        cf_update_ip(*record_info.values())
        pass

    def get_ip_list(self) -> List[str]:
        return NetToolKit.local_info.get_all_local_ip_non_local()


def main():
    common.iniConfigManager = common.IniConfigManager(common.config_ini_path)
    common.iniConfigManager.read_config_file()

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
