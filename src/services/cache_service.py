# src/services/cache_service.py

import json
import hashlib
from typing import Any, Dict, Optional

import aioredis
from src.config import settings
from src.core.exceptions import ServiceError

class CacheService:
    """
    Асинхронный сервис для кэширования результатов в Redis.
    Используется для сокращения повторных запросов к тяжёлым тулзам
    (например, InternetFetcher) и ускорения общей работы пайплайна.
    """

    def __init__(self, redis_url: Optional[str] = None):
        try:
            url = redis_url or settings.redis_url  # убедитесь, что в settings есть REDIS_URL
            # создаём клиент aioredis
            self.redis = aioredis.from_url(
                url,
                encoding="utf-8",
                decode_responses=True,
            )
        except Exception as e:
            raise ServiceError(f"CacheService initialization failed: {e}")

    def _make_key(self, prefix: str, text: str) -> str:
        """
        Генерируем ключ на основе префикса и md5-хеша текста.
        """
        fingerprint = hashlib.md5(text.encode("utf-8")).hexdigest()
        return f"{prefix}:{fingerprint}"

    async def get(self, prefix: str, text: str) -> Optional[Any]:
        """
        Попытаться достать значение из кэша.
        Возвращает распарсенный объект или None.
        """
        key = self._make_key(prefix, text)
        try:
            raw = await self.redis.get(key)
            if raw is None:
                return None
            return json.loads(raw)
        except Exception as e:
            raise ServiceError(f"CacheService.get failed: {e}")

    async def set(self, prefix: str, text: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Поставить в кэш произвольный объект (сериализуем в JSON).
        TTL берётся из settings.cache_ttl, если не передан.
        """
        key = self._make_key(prefix, text)
        try:
            payload = json.dumps(value)
            await self.redis.set(key, payload, ex=ttl or settings.cache_ttl)
        except Exception as e:
            raise ServiceError(f"CacheService.set failed: {e}")