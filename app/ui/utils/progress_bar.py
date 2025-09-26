from PySide6.QtCore import QThread, QObject, Signal, Slot


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
            except Exception:
                pass
            # Keep sleep outside try so exceptions don't delay stopping
            QThread.msleep(100)

    def stop(self):
        self._running = False
