from app.utils.logger import get_logger
import pygame
import requests
import os

logger = get_logger(__name__)


class Playback:
    def __init__(self):
        logger.info("Initializing mixer")
        pygame.mixer.init()

    def play(self, track_url: str):
        logger.info("Playing track")

        track = requests.get(track_url)

        with open("app/temp_storage/track.mp3", "wb") as f:
            f.write(track.content)

        try:
            logger.info("Loading track")

            # Set the volume
            pygame.mixer.music.set_volume(0.5)

            # Load an MP3 or WAV
            pygame.mixer.music.load("app/temp_storage/track.mp3")

            # Play it
            logger.info("Playing track")
            pygame.mixer.music.play()
        except Exception as e:
            logger.error(f"Error playing track: {e}")

    def pause(self):
        logger.info("Pausing track")
        pygame.mixer.music.pause()

    def resume(self):
        logger.info("Resuming track")
        pygame.mixer.music.unpause()

    def stop(self):
        logger.info("Stopping track")
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        os.remove("app/temp_storage/track.mp3")
        logger.info("Track stopped")
