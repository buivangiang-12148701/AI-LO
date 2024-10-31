from typing import Optional
from sqlalchemy.orm import Session
from app.core.logging import logger
from app.core.cache import RedisCache

class BaseService:
    def __init__(self, db: Session, cache: Optional[RedisCache] = None):
        self.db = db
        self.cache = cache
        self.logger = logger

    def _get_cache_key(self, prefix: str, key: str) -> str:
        """Generate cache key"""
        return f"{prefix}:{key}"

    def _log_error(self, error: Exception, message: str):
        """Log error with context"""
        self.logger.error(f"{message}: {str(error)}")
        raise error 