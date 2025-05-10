import asyncio
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from src.tools.base import BaseTool
from src.models.domain import SpotifyFeatures
from src.config import settings
from src.core.exceptions import ToolError

class SpotifyFeaturesTool(BaseTool):
    name = "spotify_features"

    def __init__(self):
        auth = SpotifyClientCredentials(
            client_id=settings.spotify_client_id,
            client_secret=settings.spotify_client_secret
        )
        self.client = Spotify(client_credentials_manager=auth)

    async def run(self, text: str, metadata: dict) -> tuple[str, dict]:
        track_id = metadata.get("track_id")
        if not track_id:
            return text, metadata
        try:
            loop = asyncio.get_event_loop()
            feat = await loop.run_in_executor(None, lambda: self.client.audio_features([track_id])[0])
            sf = SpotifyFeatures(
                tempo=feat["tempo"],
                key=feat["key"],
                mode=feat["mode"],
                time_signature=feat["time_signature"],
                loudness=feat["loudness"]
            ).dict()
            metadata["spotify_features"] = sf
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")