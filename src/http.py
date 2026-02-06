from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import aiohttp


@dataclass
class CacheEntry:
    value: Any
    expires_at: float


class SimpleCache:
    def __init__(self) -> None:
        self._entries: Dict[str, CacheEntry] = {}

    def get(self, key: str) -> Optional[Any]:
        entry = self._entries.get(key)
        if not entry:
            return None
        if entry.expires_at < time.time():
            self._entries.pop(key, None)
            return None
        return entry.value

    def set(self, key: str, value: Any, ttl: int) -> None:
        self._entries[key] = CacheEntry(value=value, expires_at=time.time() + ttl)


class RateLimiter:
    def __init__(self, rate_per_second: float) -> None:
        self._interval = 1 / rate_per_second
        self._lock = asyncio.Lock()
        self._last_called = 0.0

    async def throttle(self) -> None:
        async with self._lock:
            now = time.time()
            wait_time = self._interval - (now - self._last_called)
            if wait_time > 0:
                await asyncio.sleep(wait_time)
            self._last_called = time.time()


class HttpClient:
    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()
        self._cache = SimpleCache()
        self._rate_limiter = RateLimiter(rate_per_second=5)

    async def get_json(self, url: str, params: Optional[Dict[str, Any]] = None, ttl: int = 5) -> Any:
        cache_key = f"GET:{url}:{params}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached
        await self._rate_limiter.throttle()
        for attempt in range(3):
            try:
                async with self._session.get(url, params=params, timeout=10) as response:
                    response.raise_for_status()
                    payload = await response.json()
                    self._cache.set(cache_key, payload, ttl)
                    return payload
            except Exception:
                if attempt == 2:
                    raise
                await asyncio.sleep(0.5 * (attempt + 1))
        raise RuntimeError("Unreachable")

    async def post_json(self, url: str, payload: Dict[str, Any], ttl: int = 5) -> Any:
        cache_key = f"POST:{url}:{payload}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            return cached
        await self._rate_limiter.throttle()
        for attempt in range(3):
            try:
                async with self._session.post(url, json=payload, timeout=10) as response:
                    response.raise_for_status()
                    data = await response.json()
                    self._cache.set(cache_key, data, ttl)
                    return data
            except Exception:
                if attempt == 2:
                    raise
                await asyncio.sleep(0.5 * (attempt + 1))
        raise RuntimeError("Unreachable")

    async def close(self) -> None:
        await self._session.close()
