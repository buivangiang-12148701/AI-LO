from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Vietnamese Food Chatbot"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Database
    DATABASE_URL: str = "sqlite:///./food_chatbot.db"
    
    # Redis Cache
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    
    # Model Settings
    MODEL_PATH: str = "models/food_ai_model.pkl"
    MODEL_CACHE_TTL: int = 3600  # 1 hour
    
    # Crawler Settings
    CRAWLER_DELAY: float = 1.0
    MAX_RETRIES: int = 3
    CONCURRENT_REQUESTS: int = 5

    class Config:
        case_sensitive = True

settings = Settings() 