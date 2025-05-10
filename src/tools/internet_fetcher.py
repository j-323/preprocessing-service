import httpx
from datetime import datetime
from src.tools.base import BaseTool
from src.tools.backoff import retry_on_exception
from src.tools.cache import cache_result
from src.tools.rate_limiter import rate_limit
from src.models.domain import InternetMetadata
from src.config import settings
from src.core.exceptions import ToolError

class InternetFetcher(BaseTool):
    name = "internet_fetcher"
    URL = "https://api.perplexity.ai/search"

    @retry_on_exception
    @cache_result()
    @rate_limit
    async def fetch(self, text: str) -> dict:
        headers = {"Authorization": f"Bearer {settings.perplexity_api_key}"}
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(self.URL, headers=headers, params={"q": text, "limit": 3})
            r.raise_for_status()
            return r.json()

    async def run(self, text: str, metadata: dict) -> tuple[str, dict]:
        try:
            data = await self.fetch(text)
            meta = InternetMetadata(source="perplexity", fetched_at=datetime.utcnow(), data=data).dict()
            metadata.setdefault("internet", []).append(meta)
            return text, metadata
        except Exception as e:
            raise ToolError(f"{self.name} failed: {e}")