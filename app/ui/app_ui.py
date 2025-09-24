from .main_window_ui import Ui_mainWindow
from PySide6.QtWidgets import QMainWindow


class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.ui.search_view.search_results.itemClicked.connect(self.set_cover_url)

    def set_cover_url(
        self,
        url="https://usercontent.jamendo.com?type=album&id=529594&width=300&trackid=2058127",
    ):
        self.ui.playing_view.set_cover_url(
            "https://usercontent.jamendo.com?type=album&id=529594&width=300&trackid=2058127"
        )
