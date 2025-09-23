from .main_window_ui import Ui_mainWindow
from PySide6.QtWidgets import QMainWindow


class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
