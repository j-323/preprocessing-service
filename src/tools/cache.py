from aiocache import cached, Cache
from src.config import settings

def cache_result(ttl: int = settings.cache_ttl):
    return cached(ttl=ttl, cache=Cache.MEMORY)