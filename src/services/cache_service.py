import json
import hashlib
import asyncio
import logging
from typing import Any, Optional

import aioredis
from aioredis import Redis
from src.config import settings
from src.core.exceptions import ServiceError

logger = logging.getLogger(__name__)

class CacheService:
    """
    Асинхронный Redis-кэшер с метриками попаданий/промахов и безопасным восстановлением соединения.
    """

    def __init__(self, redis_url: Optional[str] = None):
        url = redis_url or settings.redis_url
        self._url = url
        self._redis: Optional[Redis] = None
        self._lock = asyncio.Lock()
        self.hits = 0
        self.misses = 0

    async def _get_redis(self) -> Redis:
        if self._redis is None:
            async with self._lock:
                if self._redis is None:
                    try:
                        self._redis = aioredis.from_url(
                            self._url,
                            encoding="utf-8",
                            decode_responses=True,
                            max_connections=10,
                        )
                    except Exception as e:
                        logger.error("CacheService: невозможно подключиться к Redis", exc_info=e)
                        raise ServiceError(f"Redis init failed: {e}")
        return self._redis

    def _make_key(self, prefix: str, text: str) -> str:
        fingerprint = hashlib.md5(text.encode("utf-8")).hexdigest()
        return f"{prefix}:{fingerprint}"

    async def get(self, prefix: str, text: str) -> Optional[Any]:
        key = self._make_key(prefix, text)
        try:
            redis = await self._get_redis()
            raw = await redis.get(key)
            if raw is None:
                self.misses += 1
                return None
            self.hits += 1
            return json.loads(raw)
        except Exception as e:
            logger.warning("CacheService.get error, пропускаем кэш", exc_info=e)
            return None

    async def set(self, prefix: str, text: str, value: Any, ttl: Optional[int] = None) -> None:
        key = self._make_key(prefix, text)
        try:
            redis = await self._get_redis()
            payload = json.dumps(value)
            expire = ttl or settings.cache_ttl
            await redis.set(key, payload, ex=expire)
        except Exception as e:
            logger.warning("CacheService.set error, не удалось сохранить в кэш", exc_info=e)
