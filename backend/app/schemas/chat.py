from pydantic import BaseModel
from typing import List, Optional, Dict

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    language: Optional[str] = "vi"

class ChatResponse(BaseModel):
    response: str
    confidence: float
    suggestions: List[str] = []
    metadata: Optional[Dict] = None

    class Config:
        schema_extra = {
            "example": {
                "response": "Dạ, phở là món ăn truyền thống của Việt Nam...",
                "confidence": 0.95,
                "suggestions": ["Xem menu", "Đặt bàn", "Món đặc sản"],
                "metadata": {
                    "dish_type": "món soup",
                    "region": "Bắc"
                }
            }
        } 