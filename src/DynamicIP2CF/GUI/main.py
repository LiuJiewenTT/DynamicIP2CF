import ipaddress
from typing import List, Tuple, Union

from PySide6.QtWidgets import QApplication, QMainWindow, QFrame, QWidget, QListWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy, QGroupBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QShowEvent, QResizeEvent, QPixmap, QPalette, QBrush

import NetToolKit.local_info
import R
from DynamicIP2CF import common
from DynamicIP2CF.utils_toplevel import cf_update_ip
from DynamicIP2CF.GUI.MyQtHelper import MyQWindowHelper

from DynamicIP2CF.GUI import ConfigureDialog, utils as gui_utils


class MainWindow(MyQWindowHelper):

    window_shown = Signal()
    widget_pixmap_resize_pairs: List[Tuple[QWidget, QPixmap]]

    def __init__(self, parent=None):
        super().__init__()
        self.widget_pixmap_resize_pairs = []

        self.__init_layout()

        # Init listeners
        self.window_shown.connect(self.__init_shown)

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        self.window_shown.emit()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

        self.overlay.setGeometry(self.rect())
        new_size = self.rect().size()
        pair_count = len(self.widget_pixmap_resize_pairs)
        gui_utils.resize_widgets_pixmap([new_size,]*pair_count, self.widget_pixmap_resize_pairs)

    def __init_layout(self):
        self.setWindowTitle("{program_name} (Cloudflare DDNS更新工具)".format(program_name=common.program_name))
        self.resize(600, 300)
        self.setMinimumSize(600, 300)

        self.main_widget = QWidget()
        self.main_widget.setObjectName("MainWidget")
        self.setCentralWidget(self.main_widget)

        self.main_layout = QHBoxLayout(self.main_widget)

        # self.main_widget.setStyleSheet("""
        #     QWidget#MainWidget {{
        #         background-image: url("{main_window_bg}");
        #         background-repeat: no-repeat;
        #         background-position: center;
        #     }}
        #     """.format(main_window_bg=RsvP(R.image.main_window_bg)))
        self.main_window_bg_pixmap = QPixmap(RsvP(R.image.main_window_bg))
        self.main_window_bg_palette = QPalette()
        # self.main_window_bg_palette.setBrush(QPalette.Window, QBrush(self.main_window_bg_pixmap))
        self.main_widget.setPalette(self.main_window_bg_palette)
        self.widget_pixmap_resize_pairs.append((self.main_widget, self.main_window_bg_pixmap))
        self.main_widget.setAutoFillBackground(True)

        self.overlay = QLabel(self.main_widget)
        self.overlay.setStyleSheet("background-color: rgba(255, 255, 255, 180);")
        # self.overlay.setGeometry(self.main_widget.rect())
        # self.overlay.lower()  # 保证在文字下
        # self.overlay.show()

        # Left side list widget
        self.list_widget = QListWidget()
        self.list_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.list_widget.setFixedWidth(350)  # Adjust width to fit IPv6 address length
        self.main_layout.addWidget(self.list_widget)

        # Right side layout
        self.right_side_widget = QWidget()
        self.right_side_layout = QVBoxLayout(self.right_side_widget)
        self.right_side_layout.addStretch(1)
        self.main_layout.addWidget(self.right_side_widget)

        # Info Block
        # info_frame = QFrame()
        self.info_group = QGroupBox("信息")
        # info_frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        # info_frame.setLineWidth(1)
        self.info_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.info_group_layout = QVBoxLayout(self.info_group)
        self.right_side_layout.addWidget(self.info_group)

        # Status label
        self.status_widget = QWidget()
        self.status_layout = QHBoxLayout(self.status_widget)
        self.status_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.info_group_layout.addWidget(self.status_widget, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.status_label_title = QLabel("状态：", alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.status_layout.addWidget(self.status_label_title)
        self.status_label = QLabel("就绪", alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.status_layout.addWidget(self.status_label)

        # Result label
        self.result_widget = QWidget()
        self.result_layout = QHBoxLayout(self.result_widget)
        self.result_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.info_group_layout.addWidget(self.result_widget, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.result_label_title = QLabel("结果信息：", alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.result_layout.addWidget(self.result_label_title)
        self.result_label = QLabel("空", alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.result_layout.addWidget(self.result_label)

        # Configure button
        self.configure_button = QPushButton("配置")
        self.configure_button.clicked.connect(self.show_configure_dialog)
        self.right_side_layout.addWidget(self.configure_button)

        # Refresh IP list button
        self.refresh_ip_list_button = QPushButton("刷新本机外部IP")
        self.refresh_ip_list_button.clicked.connect(self.refresh_ip_list)
        self.right_side_layout.addWidget(self.refresh_ip_list_button)

        # Update IP button
        self.update_ip_button = QPushButton("更新IP到DNS")
        self.update_ip_button.clicked.connect(self.update_ip)
        self.right_side_layout.addWidget(self.update_ip_button)

    def __init_shown(self):
        self.refresh_ip_list()

    def update_status(self, status: str):
        self.status_label.setText(status)
        gui_utils.adjust_widget_size_recursively(self.status_label)

    def update_result(self, result: str):
        self.result_label.setText(result)
        gui_utils.adjust_widget_size_recursively(self.result_label)

    def get_selected_ip(self) -> Union[str, None]:
        if self.list_widget.count() == 0:
            return None

        # 获取选中的条目
        selected_items = self.list_widget.selectedItems()
        if len(selected_items) == 0:
            return None
        return selected_items[0].text()

    def get_ip_list(self) -> List[str]:
        return NetToolKit.local_info.get_all_local_ip_non_local()

    def show_configure_dialog(self):
        dialog = ConfigureDialog.ConfigureDialog(parent=self)
        dialog.current_selected_ip = self.get_selected_ip()
        # dialog.exec()   # 阻塞运行
        dialog.show()   # 非阻塞运行

    def refresh_ip_list(self):
        ip_list = self.get_ip_list()
        self.list_widget.clear()
        for ip in ip_list:
            self.list_widget.addItem(ip)

    def update_ip(self):
        self.update_result("空")
        self.update_status("获取IP中...")
        ip_str = self.get_selected_ip()
        if ip_str is None:
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
        retv = None
        update_error = None
        try:
            retv = cf_update_ip(*record_info.values())
        except Exception as e:
            print(e)
            update_error = e
        if retv:
            self.update_result("更新IP到DNS成功")
        else:
            if update_error is not None:
                self.update_result("更新IP到DNS失败：{error}".format(error=str(update_error)))
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

    global Rsv, RsvP
    common.resource_manager = common.ResourceManager()
    common.post_init_resource_manager()
    # common.Rsv = common.resource_manager.get_res_path
    # common.RsvP = common.resource_manager.get_res_path_p
    from DynamicIP2CF.common import Rsv, RsvP

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
