from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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
        self.status_label = QLabel("Status: Ready", alignment=Qt.AlignCenter)
        right_side_layout.addWidget(self.status_label)

        # Update IP button
        self.update_ip_button = QPushButton("更新IP")
        self.update_ip_button.clicked.connect(self.update_ip)
        right_side_layout.addWidget(self.update_ip_button)

    def update_ip(self):
        ip_info = self.get_ip_info()
        print(ip_info)

    def get_ip_info(self):
        # Dummy function to simulate IP info retrieval
        return {"IPv6": "2001:0db8:85a3:0000:0000:8a2e:0370:7334", "Status": "Updated"}


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
