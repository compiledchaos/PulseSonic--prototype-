import dotenv
import os
import aiohttp
import asyncio
import threading
from app.utils.logger import get_logger

dotenv.load_dotenv()
logger = get_logger(__name__)


class JamendoApi:
    def __init__(self):
        self.client_id = os.getenv("JAMENDO_CLIENT_ID")
        self.namesearch = ""
        self.track_id = ""
        self.limit = 20
        self.track_info = None

    # ---------------------------
    # Async API calls (internal)
    # ---------------------------
    async def _fetch(self, url: str):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.json()
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    async def get_track_list_async(self):
        url = (
            f"https://api.jamendo.com/v3.0/tracks/"
            f"?client_id={self.client_id}&format=jsonpretty&limit={self.limit}&search={self.namesearch}"
        )
        data = await self._fetch(url)
        if not data:
            return None

        track_list = {t["id"]: t["name"] for t in data.get("results", [])}
        return track_list

    async def get_track_info_async(self):
        url = (
            f"https://api.jamendo.com/v3.0/tracks/"
            f"?client_id={self.client_id}&format=jsonpretty&id={self.track_id}"
        )
        data = await self._fetch(url)
        try:
            results = (data or {}).get("results", [])
            self.track_info = results[0] if results else None
        except Exception:
            self.track_info = None
        return self.track_info

    # ---------------------------
    # Threaded wrappers (safe for UI use)
    # ---------------------------
    def run_in_thread(self, coro, callback=None):
        """Run an async coroutine in a thread and call back with result."""

        def runner():
            try:
                result = asyncio.run(coro)
                if callback:
                    callback(result)
            except Exception as e:
                logger.error(f"Threaded API call failed: {e}")

        threading.Thread(target=runner, daemon=True).start()

    def get_track_list(self, callback=None):
        """Non-blocking wrapper for get_track_list_async"""
        self.run_in_thread(self.get_track_list_async(), callback)

    def get_track_info(self, callback=None):
        """Non-blocking wrapper for get_track_info_async"""
        self.run_in_thread(self.get_track_info_async(), callback)

    # ---------------------------
    # Accessors for track_info (synchronous getters)
    # ---------------------------
    def get_track(self):
        return (self.track_info or {}).get("audio") if self.track_info else None

    def get_track_cover(self):
        return (self.track_info or {}).get("album_image") if self.track_info else None

    def get_track_artist(self):
        return (self.track_info or {}).get("artist_name") if self.track_info else None

    def get_track_name(self):
        return (self.track_info or {}).get("name") if self.track_info else None
