from typing import Generator
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.core.cache import RedisCache
from app.services.chatbot import ChatbotService

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

def get_cache() -> RedisCache:
    return RedisCache()

def get_chatbot(
    db: Session = Depends(get_db),
    cache: RedisCache = Depends(get_cache)
) -> ChatbotService:
    return ChatbotService(db, cache) 