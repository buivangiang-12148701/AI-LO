from typing import Optional, Any
import redis
from functools import lru_cache
import json
import hashlib

class CacheManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.local_cache = {}
        
    def get_cache_key(self, prefix: str, *args) -> str:
        """Tạo cache key từ các tham số"""
        key_parts = [prefix] + [str(arg) for arg in args]
        return hashlib.md5('_'.join(key_parts).encode()).hexdigest()

    async def get_or_set(
        self,
        key: str,
        func: callable,
        expire: int = 3600,
        force_refresh: bool = False
    ) -> Any:
        """Get từ cache hoặc tính toán và cache lại"""
        if not force_refresh:
            # Try local cache first
            if key in self.local_cache:
                return self.local_cache[key]
            
            # Try Redis cache
            cached = self.redis.get(key)
            if cached:
                self.local_cache[key] = json.loads(cached)
                return self.local_cache[key]

        # Calculate new value
        value = await func()
        
        # Cache value
        self._set_cache(key, value, expire)
        return value

    def _set_cache(self, key: str, value: Any, expire: int):
        """Set cache ở cả Redis và local"""
        try:
            # Cache in Redis
            self.redis.setex(
                key,
                expire,
                json.dumps(value)
            )
            # Cache locally
            self.local_cache[key] = value
        except Exception as e:
            logger.error(f"Cache error: {str(e)}")

    def invalidate(self, pattern: str):
        """Xóa cache theo pattern"""
        # Clear Redis cache
        for key in self.redis.scan_iter(pattern):
            self.redis.delete(key)
        
        # Clear local cache
        self.local_cache.clear() 