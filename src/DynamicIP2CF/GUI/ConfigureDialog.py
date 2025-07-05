from PySide6.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt


class ConfigureDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("配置界面")
        self.resize(400, 300)

        self.layout = QVBoxLayout(self)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        self.buttonBox.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonBox, alignment=Qt.AlignBottom)


def main():
    app = QApplication()
    dialog = ConfigureDialog()
    dialog.show()
    exit(app.exec())


if __name__ == '__main__':
    main()