import requests
import dotenv
import os
from app.utils.logger import get_logger

dotenv.load_dotenv()

logger = get_logger(__name__)


class JamendoApi:
    def __init__(self):
        self.client_id = os.getenv("JAMENDO_CLIENT_ID")
        self.namesearch = ""
        self.track_id = ""
        self.limit = 5

    def get_track_list(self):
        logger.info("Getting track list")

        try:
            r = requests.get(
                f"https://api.jamendo.com/v3.0/tracks/?client_id={self.client_id}&format=jsonpretty&limit={self.limit}&namesearch={self.namesearch}&",
            )
            track_list = {}
            for x in range(0, len(r.json()["results"])):
                track_list[r.json()["results"][x]["id"]] = r.json()["results"][x][
                    "name"
                ]
            return track_list
        except Exception as e:
            logger.error(f"Error getting track list: {e}")
            return None

    def get_track(self):
        logger.info("Getting track")

        try:
            r = requests.get(
                f"https://api.jamendo.com/v3.0/tracks/?client_id={self.client_id}&format=jsonpretty&id={self.track_id}&",
            )

            try:
                return r.json()["results"][0]["audio"]
            except Exception as e:
                logger.error(f"Error getting track: {e}")
                return None

        except Exception as e:
            logger.error(f"Error getting track: {e}")
            return None

    def get_track_cover(self):
        logger.info("Getting track cover")

        try:
            r = requests.get(
                f"https://api.jamendo.com/v3.0/tracks/?client_id={self.client_id}&format=jsonpretty&id={self.track_id}&",
            )

            try:
                return r.json()["results"][0]["album_image"]
            except Exception as e:
                logger.error(f"Error getting track cover: {e}")
                return None
        except Exception as e:
            logger.error(f"Error getting track cover: {e}")
            return None

    def get_track_artist(self):
        logger.info("Getting track artist")

        try:
            r = requests.get(
                f"https://api.jamendo.com/v3.0/tracks/?client_id={self.client_id}&format=jsonpretty&id={self.track_id}&",
            )

            try:
                return r.json()["results"][0]["artist_name"]
            except Exception as e:
                logger.error(f"Error getting track artist: {e}")
                return None
        except Exception as e:
            logger.error(f"Error getting track artist: {e}")
            return None

    def get_track_name(self):
        logger.info("Getting track name")

        try:
            r = requests.get(
                f"https://api.jamendo.com/v3.0/tracks/?client_id={self.client_id}&format=jsonpretty&id={self.track_id}&",
            )

            try:
                return r.json()["results"][0]["name"]
            except Exception as e:
                logger.error(f"Error getting track name: {e}")
                return None
        except Exception as e:
            logger.error(f"Error getting track name: {e}")
            return None
