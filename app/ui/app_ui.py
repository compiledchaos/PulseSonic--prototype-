from .main_window_ui import Ui_mainWindow
from PySide6.QtWidgets import QMainWindow
from app.services.jamendo_api import JamendoApi
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt, QMetaObject, Q_ARG
from PySide6.QtCore import Slot
from app.services.playback import Playback
import asyncio
from app.utils.logger import get_logger
import json

logger = get_logger(__name__)


class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.jamendo_api = JamendoApi()
        self.ui.setupUi(self)
        self.playback = Playback()

        self.ui.search_view.search_b.clicked.connect(self.do_search)
        self.ui.search_view.search_results.itemClicked.connect(self.start_playback)
        self.ui.playing_view.pause.clicked.connect(self.resume_playback)
        self.ui.playing_view.play.clicked.connect(self.pause_playback)
        # self.ui.playing_view.stop.clicked.connect(self.stop_playback)

    def do_search(self):
        logger.info("Starting search")
        query = self.ui.search_view.search_bar.text()
        logger.info(f"Searching for: {query}")
        self.ui.search_view.search_results.clear()
        logger.info("Clearing search results")
        self.jamendo_api.namesearch = query
        logger.info("Setting search query")

        # Run in background (threaded wrapper)
        self.jamendo_api.get_track_list(callback=self.handle_results)

    def handle_results(self, result):
        if not result:
            return
        QMetaObject.invokeMethod(
            self,
            "populate_results",
            Qt.QueuedConnection,
            Q_ARG(str, json.dumps(result)),
        )

    @Slot(str)
    def populate_results(self, result_json):
        tracks = json.loads(result_json)
        self.ui.search_view.search_results.clear()
        for track_id, name in tracks.items():
            item = QListWidgetItem(name)
            item.setData(Qt.UserRole, track_id)
            self.ui.search_view.search_results.addItem(item)

    def start_playback(self, item):
        logger.info("Starting playback")
        self.jamendo_api.track_id = item.data(Qt.UserRole)
        logger.info(f"Starting playback for track: {self.jamendo_api.track_id}")
        self.jamendo_api.get_track_info()
        self.playback.play(self.jamendo_api.get_track())
        self.ui.playing_view.set_cover_url(self.jamendo_api.get_track_cover())
        self.ui.playing_view.track_name.setText(self.jamendo_api.get_track_name())
        self.ui.playing_view.artist_name.setText(self.jamendo_api.get_track_artist())
        self.ui.playing_view.progressBar.setValue(0)

    def pause_playback(self):
        self.playback.pause()

    def resume_playback(self):
        self.playback.resume()

    def stop_playback(self):
        self.playback.stop()
