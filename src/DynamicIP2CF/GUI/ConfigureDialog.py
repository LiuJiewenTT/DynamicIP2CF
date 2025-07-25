import sys
from typing import Union, List, Tuple, Dict
import ipaddress

from PySide6.QtGui import QPixmap, QPalette, QResizeEvent
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, \
    QGridLayout, QLineEdit, QWidget, QTabWidget
from PySide6.QtCore import Qt

import R
from DynamicIP2CF import common
from DynamicIP2CF import programinfo
from DynamicIP2CF.GUI import utils as gui_utils


def load_resource_manager():
    global Rsv, RsvP
    if "Rsv" not in globals() or "RsvP" not in globals():
        module = sys.modules["DynamicIP2CF.common"]
        if hasattr(module, "RsvP"):
            from DynamicIP2CF.common import Rsv, RsvP
        else:
            raise Exception("Resource manager not initialized")
    else:
        # print("Rsv and RsvP found.")
        pass


class RecordInfoSettingsTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__init_layout()

    def __init_layout(self):

        self.gridLayout = QGridLayout(self)
        self.gridLayout.addWidget(QLabel("API Token: "), 0, 0)
        self.gridLayout.addWidget(QLabel("Zone ID: "), 1, 0)
        self.gridLayout.addWidget(QLabel("Record ID: "), 2, 0)
        self.gridLayout.addWidget(QLabel("DNS Name: "), 3, 0)

        _, _, api_token, zone_id, record_id, dns_name = common.iniConfigManager.get_record_info().values()

        self.apiTokenEdit = QLineEdit()
        self.apiTokenEdit.setPlaceholderText("请输入API Token")
        self.apiTokenEdit.setText(api_token)
        self.gridLayout.addWidget(self.apiTokenEdit, 0, 1)

        self.zoneIdEdit = QLineEdit()
        self.zoneIdEdit.setPlaceholderText("请输入Zone ID")
        self.zoneIdEdit.setText(zone_id)
        self.gridLayout.addWidget(self.zoneIdEdit, 1, 1)

        self.recordIdEdit = QLineEdit()
        self.recordIdEdit.setPlaceholderText("请输入Record ID")
        self.recordIdEdit.setText(record_id)
        self.gridLayout.addWidget(self.recordIdEdit, 2, 1)

        self.dnsNameEdit = QLineEdit()
        self.dnsNameEdit.setPlaceholderText("请输入DNS Name")
        self.dnsNameEdit.setText(dns_name)
        self.gridLayout.addWidget(self.dnsNameEdit, 3, 1)


class MiscSettingsTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__init_layout()

    def __init_layout(self):
        pass


class AboutTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__init_layout()

    def __init_layout(self):
        self.layout = QHBoxLayout(self)

        self.imageLabel = QLabel(self)
        pixmap = QPixmap(RsvP(R.image.program_icon))
        # scaled = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.imageLabel.setPixmap(scaled)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setFixedSize(150, 150)
        self.imageLabel.setPixmap(pixmap)
        self.layout.addWidget(self.imageLabel)

        self.textLabel = QLabel(self)
        self.textLabel.setText(programinfo.programinfo_str1)
        self.layout.addWidget(self.textLabel)


class ConfigureDialog(QDialog):

    current_selected_ip: Union[str, None] = None
    tabs: Dict[str, QWidget] = {}
    tabsTitle: Dict[str, str] = {}

    def __init__(self, parent=None):
        super().__init__(parent)

        load_resource_manager()
        self.widget_pixmap_resize_pairs = []

        self.tabsTitle["RecordInfoSettingsTab"] = "记录信息设置"
        self.tabsTitle["MiscSettingsTab"] = "其他设置"
        self.tabsTitle["AboutTab"] = "关于"

        self.__init_layout()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

        self.overlay.setGeometry(self.rect())
        new_size = self.rect().size()
        pair_count = len(self.widget_pixmap_resize_pairs)
        gui_utils.resize_widgets_pixmap([new_size,]*pair_count, self.widget_pixmap_resize_pairs)

    def __init_layout(self):
        self.setWindowTitle("配置界面")
        # self.resize(400, 300)

        style_string = ""
        with open(RsvP(R.qss.global_qss), "r", encoding="utf-8") as f:
            style_string = f.read()
        self.setStyleSheet(style_string)

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        # set spacing between widgets
        self.layout.setSpacing(15)
        # set margin of the layout
        self.layout.setContentsMargins(40, 20, 40, 20)

        self.window_bg_pixmap = QPixmap(RsvP(R.image.main_window_bg))
        self.window_bg_palette = QPalette()
        self.setPalette(self.window_bg_palette)
        self.widget_pixmap_resize_pairs.append((self, self.window_bg_pixmap))
        self.setAutoFillBackground(True)

        self.overlay = QLabel(self)
        # self.overlay.setStyleSheet("background-color: rgba(255, 255, 255, 180);")

        self.tabsWidget = QTabWidget(self)
        # self.tabsWidget.setStyleSheet("background-color: rgba(0, 255, 255, 70);")
        self.layout.addStretch(1)
        self.layout.addWidget(self.tabsWidget)
        self.layout.addStretch(1)

        self.tabs["RecordInfoSettingsTab"] = RecordInfoSettingsTab(self)
        self.tabs["MiscSettingsTab"] = MiscSettingsTab(self)
        self.tabs["AboutTab"] = AboutTab(self)

        for tab_name in self.tabs.keys():
            self.tabsWidget.addTab(self.tabs[tab_name], self.tabsTitle[tab_name])

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Apply | QDialogButtonBox.Cancel,
                                          self)
        self.buttonBox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.on_apply)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox, alignment=Qt.AlignBottom)

    def accept(self):
        self.apply_config_ini()
        common.iniConfigManager.update_config_file()
        super().accept()

    def on_apply(self):
        self.apply_config_ini()
        super().accept()

    def apply_config_ini(self):
        ip = self.current_selected_ip
        if ip is None:
            ip = ""
        ip_version = "" if not ip else ipaddress.ip_address(ip).version
        ip_version = "v4" if ip_version == 4 else "v6"
        record_info_list = [ip_version, ip, self.apiTokenEdit.text(), self.zoneIdEdit.text(), self.recordIdEdit.text(), self.dnsNameEdit.text()]
        common.iniConfigManager.update_record_info(*record_info_list)


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
    from DynamicIP2CF.common import Rsv, RsvP

    app = QApplication()
    dialog = ConfigureDialog()
    dialog.show()
    retv = app.exec()
    exit(retv)


if __name__ == '__main__':
    main()