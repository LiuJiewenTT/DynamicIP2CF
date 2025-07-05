from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QGridLayout, QLineEdit
from PySide6.QtCore import Qt

from DynamicIP2CF import common


class ConfigureDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__init_layout()

    def __init_layout(self):
        self.setWindowTitle("配置界面")
        # self.resize(400, 300)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(QLabel("API Token: "), 0, 0)
        self.gridLayout.addWidget(QLabel("Zone ID: "), 1, 0)
        self.gridLayout.addWidget(QLabel("Record ID: "), 2, 0)
        self.gridLayout.addWidget(QLabel("DNS Name: "), 3, 0)

        self.apiTokenEdit = QLineEdit()
        self.apiTokenEdit.setPlaceholderText("请输入API Token")
        self.gridLayout.addWidget(self.apiTokenEdit, 0, 1)

        self.zoneIdEdit = QLineEdit()
        self.zoneIdEdit.setPlaceholderText("请输入Zone ID")
        self.gridLayout.addWidget(self.zoneIdEdit, 1, 1)

        self.recordIdEdit = QLineEdit()
        self.recordIdEdit.setPlaceholderText("请输入Record ID")
        self.gridLayout.addWidget(self.recordIdEdit, 2, 1)

        self.dnsNameEdit = QLineEdit()
        self.dnsNameEdit.setPlaceholderText("请输入DNS Name")
        self.gridLayout.addWidget(self.dnsNameEdit, 3, 1)

        self.layout.addStretch(1)
        self.layout.addLayout(self.gridLayout)
        self.layout.addStretch(1)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Apply | QDialogButtonBox.Cancel, self)
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
        record_info_list = ["", "", self.apiTokenEdit.text(), self.zoneIdEdit.text(), self.recordIdEdit.text(), self.dnsNameEdit.text()]
        common.iniConfigManager.update_record_info(*record_info_list)


def main():
    common.iniConfigManager = common.IniConfigManager(common.config_ini_path)
    try:
        common.iniConfigManager.read_config_file()
    except FileNotFoundError as fe:
        common.iniConfigManager.generate_config_file()
        common.iniConfigManager.read_config_file()

    app = QApplication()
    dialog = ConfigureDialog()
    dialog.show()
    retv = app.exec()
    exit(retv)


if __name__ == '__main__':
    main()