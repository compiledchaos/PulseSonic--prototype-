from app.utils.logger import get_logger
import vlc
import threading

logger = get_logger(__name__)


class Playback:
    def __init__(self):
        logger.info("Initializing VLC player")
        self.player = None
        self.lock = threading.Lock()  # ensure thread-safety

    def play(self, track_url: str):
        logger.info(f"Preparing to play track: {track_url}")

        def _play():
            try:
                with self.lock:
                    if self.player is not None:
                        self.player.stop()

                    # Create new VLC media player
                    instance = vlc.Instance()
                    media = instance.media_new(track_url)
                    self.player = instance.media_player_new()
                    self.player.set_media(media)

                    # Set volume (0–100)
                    self.player.audio_set_volume(50)

                    # Play
                    logger.info("Starting playback with VLC")
                    self.player.play()
            except Exception as e:
                logger.error(f"Error playing track: {e}")

        threading.Thread(target=_play, daemon=True).start()

    def pause(self):
        with self.lock:
            if self.player is not None:
                if self.player.is_playing():
                    logger.info("Pausing track")
                    self.player.pause()

    def resume(self):
        with self.lock:
            if self.player is not None:
                if not self.player.is_playing():
                    logger.info("Resuming track")
                    self.player.play()

    def stop(self):
        with self.lock:
            if self.player is not None:
                logger.info("Stopping track")
                self.player.stop()
                self.player = None

    def progress(self):
        with self.lock:
            if self.player is not None:
                # logger.info("Getting track progress")
                return (self.player.get_time() / self.player.get_length()) * 100

    def set_volume(self, volume: int):
        with self.lock:
            if self.player is not None:
                self.player.audio_set_volume(volume)

    def seek_forward(self):
        with self.lock:
            if self.player is not None:
                self.player.set_time(self.player.get_time() + 5000)

    def seek_backward(self):
        with self.lock:
            if self.player is not None:
                if self.player.get_time() > 5000:
                    self.player.set_time(self.player.get_time() - 5000)
