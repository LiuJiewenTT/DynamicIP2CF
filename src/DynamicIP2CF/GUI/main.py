import ipaddress
from typing import List

from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QWidget, QListWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QGroupBox
from PySide6.QtCore import Qt, Signal

import NetToolKit.local_info
from DynamicIP2CF import common
from DynamicIP2CF.utils_toplevel import cf_update_ip
from DynamicIP2CF.GUI.MyQtHelper import MyQWindowHelper

from DynamicIP2CF.GUI import ConfigureDialog


class MainWindow(MyQWindowHelper):
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
        self.setWindowTitle("{program_name} (Cloudflare DDNS更新工具)".format(program_name=common.program_name))
        self.resize(600, 300)

        main_widget = QWidget()
        main_widget.setObjectName("MainWidget")
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)

        main_widget.setStyleSheet("""
        QWidget#MainWidget {
                                background-image: url("M:/Mine/R.jpg");
                                background-repeat: no-repeat;
                                background-position: center;
                                background-size: cover;
                                }
                             """)
        main_widget.setAutoFillBackground(True)

        # Left side list widget
        self.list_widget = QListWidget()
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.list_widget.setFixedWidth(350)  # Adjust width to fit IPv6 address length
        main_layout.addWidget(self.list_widget)

        # Right side layout
        right_side_widget = QWidget()
        right_side_layout = QVBoxLayout(right_side_widget)
        right_side_layout.addStretch(1)
        main_layout.addWidget(right_side_widget)

        # Info Block
        # info_frame = QFrame()
        info_frame = QGroupBox("信息")
        # info_frame.setFrameStyle(QFrame.Box | QFrame.Sunken)
        # info_frame.setLineWidth(1)
        info_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        info_frame_layout = QVBoxLayout(info_frame)
        right_side_layout.addWidget(info_frame)

        # Status label
        status_widget = QWidget()
        status_layout = QHBoxLayout(status_widget)
        status_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        info_frame_layout.addWidget(status_widget, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.status_label_title = QLabel("状态：", alignment=Qt.AlignLeft | Qt.AlignBottom)
        status_layout.addWidget(self.status_label_title)
        self.status_label = QLabel("就绪", alignment=Qt.AlignLeft | Qt.AlignBottom)
        status_layout.addWidget(self.status_label)

        # Result label
        result_widget = QWidget()
        result_layout = QHBoxLayout(result_widget)
        result_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        info_frame_layout.addWidget(result_widget, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.result_label_title = QLabel("结果信息：", alignment=Qt.AlignLeft | Qt.AlignBottom)
        result_layout.addWidget(self.result_label_title)
        self.result_label = QLabel("空", alignment=Qt.AlignLeft | Qt.AlignBottom)
        result_layout.addWidget(self.result_label)

        # Configure button
        self.configure_button = QPushButton("配置")
        self.configure_button.clicked.connect(self.show_configure_dialog)
        right_side_layout.addWidget(self.configure_button)

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

    def update_status(self, status: str):
        self.status_label.setText(status)

    def update_result(self, result: str):
        self.result_label.setText(result)

    def get_selected_ip(self):
        if self.list_widget.count() == 0:
            return ""

        # 获取选中的条目
        selected_items = self.list_widget.selectedItems()
        if len(selected_items) == 0:
            return ""
        return selected_items[0].text()

    def get_ip_list(self) -> List[str]:
        return NetToolKit.local_info.get_all_local_ip_non_local()

    def show_configure_dialog(self):
        ConfigureDialog.ConfigureDialog().exec()

    def refresh_ip_list(self):
        ip_list = self.get_ip_list()
        self.list_widget.clear()
        for ip in ip_list:
            self.list_widget.addItem(ip)

    def update_ip(self):
        self.update_status("获取IP中...")
        ip_str = self.get_selected_ip()
        if not ip_str:
            # 没有可用IP
            self.update_result("没有选择IP")
            self.update_status("就绪")
            return

        record_info = common.iniConfigManager.get_record_info()
        record_info['ip'] = ip_str
        ip = ipaddress.ip_address(record_info['ip'])
        if ip.version == 6:
            record_info['ip_version'] = 'v6'
        else:
            record_info['ip_version'] = 'v4'

        self.update_status("更新IP到DNS中...")
        retv = cf_update_ip(*record_info.values())
        if retv:
            self.update_result("更新IP到DNS成功")
        else:
            self.update_result("更新IP到DNS失败")
        self.update_status("就绪")
        pass


def main():
    common.iniConfigManager = common.IniConfigManager(common.config_ini_path)
    try:
        common.iniConfigManager.read_config_file()
    except FileNotFoundError as fe:
        common.iniConfigManager.generate_config_file()
        common.iniConfigManager.read_config_file()

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
