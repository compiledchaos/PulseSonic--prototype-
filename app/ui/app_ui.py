from .main_window_ui import Ui_mainWindow
from PySide6.QtWidgets import QMainWindow
from app.services.jamendo_api import JamendoApi
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt, QMetaObject, Q_ARG, QThread, QObject, Signal
from PySide6.QtCore import Slot
from app.services.playback import Playback
from app.utils.logger import get_logger
import json

logger = get_logger(__name__)


class ProgressWorker(QObject):
    progress = Signal(float)

    def __init__(self, playback):
        super().__init__()
        self.playback = playback
        self._running = True

    @Slot()
    def run(self):
        while self._running:
            try:
                if (
                    self.playback.player is not None
                    and self.playback.player.is_playing()
                ):
                    value = self.playback.progress() or 0
                    # clamp
                    value = max(0, min(100, value))
                    self.progress.emit(value)
                QThread.msleep(100)

            except Exception:
                QThread.msleep(200)

    def stop(self):
        self._running = False


class AppMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.jamendo_api = JamendoApi()
        self.ui.setupUi(self)
        self.playback = Playback()
        self._progress_thread = None
        self._progress_worker = None

        # Wire up signals
        self.ui.search_view.search_b.clicked.connect(self.do_search)
        self.ui.search_view.search_results.itemClicked.connect(self.start_playback)
        self.ui.playing_view.pause.clicked.connect(self.resume_playback)
        self.ui.playing_view.play.clicked.connect(self.pause_playback)
        self.ui.playing_view.volume.valueChanged.connect(self.set_volume)
        self.ui.playing_view.forward.clicked.connect(self.forward)
        self.ui.playing_view.backward.clicked.connect(self.backward)

    def set_volume(self, value: int):
        self.playback.set_volume(value)

    def forward(self):
        self.playback.seek_forward()

    def backward(self):
        self.playback.seek_backward()

    def do_search(self):
        logger.info("Starting search")
        query = self.ui.search_view.search_bar.text()
        logger.info(f"Searching for: {query}")
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
    def populate_results(self, result_json: str):
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
        # Fetch track info in background; update UI when ready
        self.jamendo_api.get_track_info(callback=self.on_track_info_ready)

    def on_track_info_ready(self, info):
        # Marshal back to UI thread with a slot
        QMetaObject.invokeMethod(
            self,
            "apply_track_info",
            Qt.QueuedConnection,
            Q_ARG(str, json.dumps(info or {})),
        )

    @Slot(str)
    def apply_track_info(self, info_json: str):
        try:
            info = json.loads(info_json) if info_json else {}
        except Exception:
            info = {}
        if not info:
            return
        # Update UI
        self.ui.playing_view.track_name.setText(info.get("name", ""))
        self.ui.playing_view.artist_name.setText(info.get("artist_name", ""))
        cover = info.get("album_image")
        if cover:
            self.ui.playing_view.set_cover_url(cover)
        # Start playback
        audio_url = info.get("audio")
        if audio_url:
            self.playback.play(audio_url)
            self.start_progress_worker()
        self.ui.playing_view.progressBar.setValue(0)

    def pause_playback(self):
        self.playback.pause()

    def resume_playback(self):
        self.playback.resume()

    def stop_playback(self):
        # self.stop_progress_worker()
        self.playback.stop()
        self.ui.playing_view.progressBar.setValue(0)

    def start_progress_worker(self):
        # stop previous if any
        self.stop_progress_worker()
        self._progress_thread = QThread()
        self._progress_worker = ProgressWorker(self.playback)
        self._progress_worker.moveToThread(self._progress_thread)
        self._progress_thread.started.connect(self._progress_worker.run)
        self._progress_worker.progress.connect(self.update_progress)
        self._progress_thread.start()

    def stop_progress_worker(self):
        if self._progress_worker is not None:
            try:
                self._progress_worker.stop()
            except Exception:
                pass
        if self._progress_thread is not None:
            self._progress_thread.quit()
            self._progress_thread.wait()
        self._progress_worker = None
        self._progress_thread = None

    @Slot(float)
    def update_progress(self, value: float):
        self.ui.playing_view.progressBar.setValue(int(value))
