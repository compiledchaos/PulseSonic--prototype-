from .main_window_ui import Ui_mainWindow
from PySide6.QtWidgets import QMainWindow
from app.services.jamendo_api import JamendoApi
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt
from app.services.playback import Playback


class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.jamendo_api = JamendoApi()
        self.ui.setupUi(self)
        self.playback = Playback()

        self.ui.search_view.search_b.clicked.connect(self.search)
        self.ui.search_view.search_results.itemClicked.connect(self.start_playback)
        self.ui.playing_view.pause.clicked.connect(self.resume_playback)
        self.ui.playing_view.play.clicked.connect(self.pause_playback)
        # self.ui.playing_view.stop.clicked.connect(self.stop_playback)

    def search(self):
        self.jamendo_api.namesearch = self.ui.search_view.search_bar.text()
        self.ui.search_view.search_results.clear()
        for x, y in self.jamendo_api.get_track_list().items():
            item = QListWidgetItem(y)
            item.setData(Qt.UserRole, x)
            self.ui.search_view.search_results.addItem(item)
        self.ui.search_view.retranslateUi()

    def start_playback(self, item):
        self.stop_playback()
        self.jamendo_api.track_id = item.data(Qt.UserRole)
        self.ui.playing_view.set_cover_url(self.jamendo_api.get_track_cover())
        self.ui.playing_view.track_name.setText(self.jamendo_api.get_track_name())
        self.ui.playing_view.artist_name.setText(self.jamendo_api.get_track_artist())
        self.ui.playing_view.progressBar.setValue(0)
        self.playback.play(self.jamendo_api.get_track())

    def pause_playback(self):
        self.playback.pause()

    def resume_playback(self):
        self.playback.resume()

    def stop_playback(self):
        self.playback.stop()
