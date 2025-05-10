import asyncio
from src.core.pipeline import Pipeline
from src.services.embed_service import EmbedService
from src.services.search_service import SearchService
from src.models.domain import EmbedRequest, SearchRequest
from src.logger import logger

class PreprocessingAgent:
    def __init__(self, pipeline: Pipeline = None):
        self.pipeline = pipeline or Pipeline()
        self.embed_svc = EmbedService()
        self.search_svc = SearchService()

    async def preprocess_and_embed(self, track_id: int, raw_text: str):
        clean, meta = await self.pipeline.run(raw_text, {"track_id": track_id})
        req = EmbedRequest(track_id=track_id, clean_text=clean, metadata=meta)
        logger.info("Embedding", track_id=track_id)
        return self.embed_svc.embed(req)

    def search_similar(self, query_text: str, top_k: int = 5):
        req = SearchRequest(query_text=query_text, top_k=top_k)
        logger.info("Searching", query=query_text, top_k=top_k)
        return self.search_svc.search(req)

    def run_sync(self, track_id: int, raw_text: str):
        return asyncio.get_event_loop().run_until_complete(
            self.preprocess_and_embed(track_id, raw_text)
        )