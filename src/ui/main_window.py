"""Main window UI skeleton."""

from PySide6.QtWidgets import QLabel, QMainWindow, QWidget, QVBoxLayout


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Claude Temp Cleaner")
        root = QWidget()
        layout = QVBoxLayout(root)
        layout.addWidget(QLabel("UI scaffold ready"))
        self.setCentralWidget(root)
