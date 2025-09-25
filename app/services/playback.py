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
                logger.info("Pausing track")
                self.player.pause()

    def resume(self):
        with self.lock:
            if self.player is not None:
                logger.info("Resuming track")
                self.player.pause()  # VLC toggle pause

    def stop(self):
        with self.lock:
            if self.player is not None:
                logger.info("Stopping track")
                self.player.stop()
                self.player = None
