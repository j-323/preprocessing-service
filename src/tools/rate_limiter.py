from aiolimiter import AsyncLimiter
from functools import wraps

limiter = AsyncLimiter(max_rate=5, time_period=1)

def rate_limit(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with limiter:
            return await func(*args, **kwargs)
    return wrapper