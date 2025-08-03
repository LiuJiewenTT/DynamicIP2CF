import sys
from typing import Union, List, Tuple, Dict, TypedDict
import ipaddress

from PySide6.QtGui import QPixmap, QPalette, QResizeEvent, QShowEvent
from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, \
    QGridLayout, QLineEdit, QWidget, QTabWidget, QPushButton, QGroupBox, QRadioButton, QButtonGroup, QTextBrowser
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
        super().__init__(parent=parent)
        self.__init_layout()

    def __init_layout(self):

        self.gridLayout = QGridLayout(self)
        self.gridLayout.addWidget(QLabel(R.string.gui.configure_dialog.record_info_settings_tab.record_info_group.labels.api_token), 0, 0)
        self.gridLayout.addWidget(QLabel(R.string.gui.configure_dialog.record_info_settings_tab.record_info_group.labels.zone_id), 1, 0)
        self.gridLayout.addWidget(QLabel(R.string.gui.configure_dialog.record_info_settings_tab.record_info_group.labels.record_id), 2, 0)
        self.gridLayout.addWidget(QLabel(R.string.gui.configure_dialog.record_info_settings_tab.record_info_group.labels.domain_name), 3, 0)

        _, _, api_token, zone_id, record_id, domain_name = common.iniConfigManager.get_record_info().values()

        self.apiTokenEdit = QLineEdit()
        self.apiTokenEdit.setPlaceholderText(R.string.gui.configure_dialog.record_info_settings_tab.record_info_group.edits_help_texts.api_token)
        self.apiTokenEdit.setText(api_token)
        self.gridLayout.addWidget(self.apiTokenEdit, 0, 1)

        self.zoneIdEdit = QLineEdit()
        self.zoneIdEdit.setPlaceholderText(R.string.gui.configure_dialog.record_info_settings_tab.record_info_group.edits_help_texts.zone_id)
        self.zoneIdEdit.setText(zone_id)
        self.gridLayout.addWidget(self.zoneIdEdit, 1, 1)

        self.recordIdEdit = QLineEdit()
        self.recordIdEdit.setPlaceholderText(R.string.gui.configure_dialog.record_info_settings_tab.record_info_group.edits_help_texts.record_id)
        self.recordIdEdit.setText(record_id)
        self.gridLayout.addWidget(self.recordIdEdit, 2, 1)

        self.domainNameEdit = QLineEdit()
        self.domainNameEdit.setPlaceholderText(R.string.gui.configure_dialog.record_info_settings_tab.record_info_group.edits_help_texts.domain_name)
        self.domainNameEdit.setText(domain_name)
        self.gridLayout.addWidget(self.domainNameEdit, 3, 1)

    def apply_config_ini(self):
        record_tab = self
        dialog = self.parent().parent().parent()
        ip = dialog.current_selected_ip
        if ip is None:
            ip = ""
        ip_version = "" if not ip else ipaddress.ip_address(ip).version
        ip_version = "v4" if ip_version == 4 else "v6"
        record_info_list = [ip_version, ip, record_tab.apiTokenEdit.text(), record_tab.zoneIdEdit.text(), record_tab.recordIdEdit.text(), record_tab.domainNameEdit.text()]
        common.iniConfigManager.update_record_info(*record_info_list)


class MiscSettingsTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__init_layout()
        self.load_values()

    def __init_layout(self):
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(15)

        self.languageGroup = QGroupBox(parent=self, title=R.string.gui.configure_dialog.misc_settings_tab.language_group.language_settings)
        self.layout.addWidget(self.languageGroup)

        self.languageGroupLayout = QHBoxLayout(self.languageGroup)
        self.languageGroupLayout.setSpacing(15)
        self.languageGroup.setLayout(self.languageGroupLayout)

        self.languageComboBox = gui_utils.create_language_combo_box(self.languageGroup)
        self.initial_lang = gui_utils.get_language_name_from_locale(common.iniConfigManager.config.get("Language", "lang", fallback=""))
        if not self.initial_lang:
            self.languageComboBox.setCurrentIndex(0)
        else:
            self.languageComboBox.setCurrentText(self.initial_lang)
        self.languageComboBox.initial_index = self.languageComboBox.currentIndex()
        self.languageComboBox.currentIndexChanged.connect(lambda : self.languageHintRestartLabel.setText(R.string.gui.configure_dialog.misc_settings_tab.language_group.hint_restart_to_apply) if self.languageComboBox.currentIndex() != self.languageComboBox.initial_index else self.languageHintRestartLabel.setText(""))
        self.languageGroupLayout.addWidget(self.languageComboBox)

        self.languageHintRestartLabel = QLabel("", parent=self.languageGroup)
        self.languageGroupLayout.addWidget(self.languageHintRestartLabel)

        self.proxyGroup = QGroupBox(parent=self, title=R.string.gui.configure_dialog.misc_settings_tab.proxy_group.proxy_settings)
        self.layout.addWidget(self.proxyGroup)

        self.proxyGroupLayout = QHBoxLayout(self.proxyGroup)
        self.proxyGroupLayout.setSpacing(15)
        self.proxyGroup.setLayout(self.proxyGroupLayout)

        self.proxyModeRadioGroupBox = QGroupBox(parent=self.proxyGroup, title=R.string.gui.configure_dialog.misc_settings_tab.proxy_group.proxy_mode)
        self.proxyGroupLayout.addWidget(self.proxyModeRadioGroupBox)

        self.proxyModeRadioGroupBoxLayout = QVBoxLayout(self.proxyModeRadioGroupBox)
        self.proxyModeRadioGroupBoxLayout.setSpacing(15)
        self.proxyModeRadioGroupBox.setLayout(self.proxyModeRadioGroupBoxLayout)

        self.proxyModeNoProxyRadioButton = QRadioButton(R.string.gui.configure_dialog.misc_settings_tab.proxy_group.proxy_mode_off, parent=self.proxyModeRadioGroupBox)
        self.proxyModeAutoRadioButton = QRadioButton(R.string.gui.configure_dialog.misc_settings_tab.proxy_group.proxy_mode_auto, parent=self.proxyModeRadioGroupBox)
        self.proxyModeSystemRadioButton = QRadioButton(R.string.gui.configure_dialog.misc_settings_tab.proxy_group.proxy_mode_system, parent=self.proxyModeRadioGroupBox)
        self.proxyModeManualRadioButton = QRadioButton(R.string.gui.configure_dialog.misc_settings_tab.proxy_group.proxy_mode_manual, parent=self.proxyModeRadioGroupBox)

        # 创建一个按钮组来管理这些单选按钮
        self.proxyModeButtonGroup = QButtonGroup(self.proxyModeRadioGroupBox)
        self.proxyModeButtonGroup.addButton(self.proxyModeNoProxyRadioButton, id=0)
        self.proxyModeButtonGroup.addButton(self.proxyModeAutoRadioButton, id=1)
        self.proxyModeButtonGroup.addButton(self.proxyModeSystemRadioButton, id=2)
        self.proxyModeButtonGroup.addButton(self.proxyModeManualRadioButton, id=3)
        self.proxyModeButtonGroup.buttonClicked.connect(self.switch_proxy_mode)

        self.proxyModeRadioGroupBoxLayout.addWidget(self.proxyModeNoProxyRadioButton)
        self.proxyModeRadioGroupBoxLayout.addWidget(self.proxyModeAutoRadioButton)
        self.proxyModeRadioGroupBoxLayout.addWidget(self.proxyModeSystemRadioButton)
        self.proxyModeRadioGroupBoxLayout.addWidget(self.proxyModeManualRadioButton)

        self.proxyManualParamsGroup = QGroupBox(parent=self.proxyGroup, title=R.string.gui.configure_dialog.misc_settings_tab.proxy_group.manual_proxy_settings)
        self.proxyGroupLayout.addWidget(self.proxyManualParamsGroup)

        self.proxyManualParamsGroupLayout = QVBoxLayout(self.proxyManualParamsGroup)
        self.proxyManualParamsGroup.setLayout(self.proxyManualParamsGroupLayout)

        self.proxyManualParams_proxyUrlLabel = QLabel(R.string.gui.configure_dialog.misc_settings_tab.proxy_group.proxy_url, parent=self.proxyManualParamsGroup)
        self.proxyManualParams_proxyUrlEdit = QLineEdit(parent=self.proxyManualParamsGroup)

        self.proxyManualParams_proxyOverrideLabel = QLabel(R.string.gui.configure_dialog.misc_settings_tab.proxy_group.proxy_override, parent=self.proxyManualParamsGroup)
        self.proxyManualParams_proxyOverrideTextBrowser = QTextBrowser(parent=self.proxyManualParamsGroup)
        self.proxyManualParams_proxyOverrideTextBrowser.setMaximumHeight(100)

        self.proxyManualParamsGroupLayout.addWidget(self.proxyManualParams_proxyUrlLabel)
        self.proxyManualParamsGroupLayout.addWidget(self.proxyManualParams_proxyUrlEdit)
        self.proxyManualParamsGroupLayout.addWidget(self.proxyManualParams_proxyOverrideLabel)
        self.proxyManualParamsGroupLayout.addWidget(self.proxyManualParams_proxyOverrideTextBrowser)

        self.proxyManualParamsGroup.setDisabled(True)

    def load_values(self):
        proxy_mode, proxy_url, proxy_override = common.iniConfigManager.get_proxy_info().values()
        # print(f"proxy_mode: {proxy_mode}, proxy_url: {proxy_url}, proxy_override: {proxy_override}")

        if proxy_mode == "off":
            self.proxyModeButtonGroup.button(0).setChecked(True)
        elif proxy_mode == "auto":
            self.proxyModeButtonGroup.button(1).setChecked(True)
        elif proxy_mode == "system":
            self.proxyModeButtonGroup.button(2).setChecked(True)
        elif proxy_mode == "manual":
            self.proxyModeButtonGroup.button(3).setChecked(True)
            self.proxyManualParamsGroup.setDisabled(False)

        self.proxyManualParams_proxyUrlEdit.setText(proxy_url)
        self.proxyManualParams_proxyOverrideTextBrowser.setText(proxy_override)

    def switch_proxy_mode(self, button: QRadioButton):
        id = self.proxyModeButtonGroup.id(button)
        if id == 3:
            self.proxyManualParamsGroup.setDisabled(False)
        else:
            self.proxyManualParamsGroup.setDisabled(True)

    def apply_config_ini(self):
        language_selected = self.languageComboBox.currentText()
        language_locale = gui_utils.get_locale_from_language_name(language_selected)
        common.iniConfigManager.config.set("Language", "lang", language_locale)

        proxy_mode = ""
        proxy_mode_id = self.proxyModeButtonGroup.checkedId()
        proxy_url = self.proxyManualParams_proxyUrlEdit.text()
        proxy_override = self.proxyManualParams_proxyOverrideTextBrowser.toPlainText()
        if proxy_mode_id == 0:
            proxy_mode = "off"
        elif proxy_mode_id == 1:
            proxy_mode = "auto"
        elif proxy_mode_id == 2:
            proxy_mode = "system"
        elif proxy_mode_id == 3:
            proxy_mode = "manual"
        common.iniConfigManager.update_proxy_info(proxy_mode, proxy_url, proxy_override)


class AboutTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__init_layout()

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        if self.textLabel.minimumWidth() == 0:
            self.textLabel.setMinimumWidth(self.textLabel.width() + 20)
            self.textLabel.adjustSize()

    def __init_layout(self):
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(15)

        self.imageLabel = QLabel(self)
        pixmap = QPixmap(RsvP(R.image.program_icon))
        # scaled = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.imageLabel.setPixmap(scaled)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setFixedSize(150, 150)
        self.imageLabel.setPixmap(pixmap)
        self.layout.addWidget(self.imageLabel)

        self.rightDetailsLayout = QVBoxLayout(self)
        self.rightDetailsLayout.setSpacing(10)
        self.layout.addLayout(self.rightDetailsLayout)

        self.textLabel = QLabel(self)
        self.textLabel.setText(f"""
            <div style="line-height: 1.5;">
                {programinfo.programinfo_html_str1}
            </div>""")
        self.textLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)  # 启用点击超链接
        self.textLabel.setTextFormat(Qt.RichText)  # 解析HTML
        self.textLabel.setOpenExternalLinks(True)
        self.rightDetailsLayout.addWidget(self.textLabel)

        self.checkUpdatelayout = QHBoxLayout(self)
        self.checkUpdateButton = QPushButton(R.string.gui.configure_dialog.about_tab.check_update.check_update, self)
        self.checkUpdateButton.clicked.connect(self.check_update)
        self.checkUpdatelayout.addWidget(self.checkUpdateButton)
        self.rightDetailsLayout.addLayout(self.checkUpdatelayout)

        self.checkUpdateResultLabel = QLabel(self)
        self.checkUpdateResultLabel.setText("")
        self.checkUpdateResultLabel.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.checkUpdateResultLabel.setOpenExternalLinks(True)
        self.checkUpdateResultLabel.setWordWrap(True)
        self.checkUpdatelayout.addWidget(self.checkUpdateResultLabel)
        # 设置插件在布局的权重
        self.checkUpdatelayout.setStretchFactor(self.checkUpdateResultLabel, 1)

    def check_update(self):
        status, version_message, status_code, response_text = gui_utils.check_update_available()
        message: str
        if status:
            message = R.string.gui.configure_dialog.about_tab.check_update.found_update.format(new_version=version_message)
        else:
            if version_message == "":
                message = R.string.gui.configure_dialog.about_tab.check_update.check_failed.format(error_message=f"[{status_code}]: {response_text}")
            else:
                message = R.string.gui.configure_dialog.about_tab.check_update.is_latest
        self.checkUpdateResultLabel.setText(message)
        gui_utils.adjust_widget_size_recursively(self.checkUpdateResultLabel)


class ConfigureDialog(QDialog):

    current_selected_ip: Union[str, None] = None
    tabs: TypedDict("ConfigureDialog_tabsDict", {"RecordInfoSettingsTab": RecordInfoSettingsTab, "MiscSettingsTab": MiscSettingsTab, "AboutTab": AboutTab, str: QWidget}) = {}
    tabsTitle: Dict[str, str] = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        load_resource_manager()
        self.widget_pixmap_resize_pairs = []

        self.tabsTitle["RecordInfoSettingsTab"] = R.string.gui.configure_dialog.record_info_settings_tab.tab_title
        self.tabsTitle["MiscSettingsTab"] = R.string.gui.configure_dialog.misc_settings_tab.tab_title
        self.tabsTitle["AboutTab"] = R.string.gui.configure_dialog.about_tab.tab_title

        self.__init_layout()

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

        self.overlay.setGeometry(self.rect())
        new_size = self.rect().size()
        pair_count = len(self.widget_pixmap_resize_pairs)
        gui_utils.resize_widgets_pixmap([new_size,]*pair_count, self.widget_pixmap_resize_pairs)

    def __init_layout(self):
        self.setWindowTitle(R.string.gui.configure_dialog.window_title)
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
        self.overlay.setProperty("class-overlay", True)

        self.tabsWidget = QTabWidget(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.tabsWidget)
        self.layout.addStretch(1)

        self.tabs["RecordInfoSettingsTab"] = RecordInfoSettingsTab(parent=self.tabsWidget)
        self.tabs["MiscSettingsTab"] = MiscSettingsTab(parent=self.tabsWidget)
        self.tabs["AboutTab"] = AboutTab(parent=self.tabsWidget)

        for tab_name in self.tabs.keys():
            self.tabsWidget.addTab(self.tabs[tab_name], self.tabsTitle[tab_name])

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Apply | QDialogButtonBox.Cancel,
                                          parent=self)
        self.buttonBox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.on_apply)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox, alignment=Qt.AlignBottom)

    def accept(self):
        record_tab = self.tabs["RecordInfoSettingsTab"]
        record_tab.apply_config_ini()
        misc_settings_tab = self.tabs["MiscSettingsTab"]
        misc_settings_tab.apply_config_ini()
        common.iniConfigManager.update_config_file()
        super().accept()

    def on_apply(self):
        record_tab = self.tabs["RecordInfoSettingsTab"]
        record_tab.apply_config_ini()
        misc_settings_tab = self.tabs["MiscSettingsTab"]
        misc_settings_tab.apply_config_ini()
        super().accept()


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

    programinfo.init_program_info()

    app = QApplication()
    dialog = ConfigureDialog()
    dialog.show()
    retv = app.exec()
    exit(retv)


if __name__ == '__main__':
    main()
