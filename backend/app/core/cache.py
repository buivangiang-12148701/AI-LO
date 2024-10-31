from functools import lru_cache
import redis
from typing import Optional, Any
import json
import pickle
from app.core.config import settings

class RedisCache:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Redis get error: {str(e)}")
            return None
            
    def set(self, key: str, value: Any, expire: int = 3600):
        """Set value to cache"""
        try:
            self.redis_client.setex(
                key,
                expire,
                json.dumps(value)
            )
        except Exception as e:
            logger.error(f"Redis set error: {str(e)}")

    def delete(self, key: str):
        """Delete key from cache"""
        try:
            self.redis_client.delete(key)
        except Exception as e:
            logger.error(f"Redis delete error: {str(e)}")

# Model cache for heavy computations
class ModelCache:
    def __init__(self, maxsize=128):
        self.cache = lru_cache(maxsize=maxsize)
        
    def __call__(self, func):
        return self.cache(func) 