from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import uvicorn
from core.chatbot import SmartFoodChatbot
import logging

# Khởi tạo FastAPI app
app = FastAPI(
    title="Vietnamese Food Chatbot API",
    description="API for Vietnamese Food Chatbot with AI capabilities",
    version="1.0.0"
)

# CORS middleware - Cập nhật origins cho phù hợp với domain của bạn
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # NextJS default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khởi tạo chatbot
chatbot = SmartFoodChatbot()

# Logging setup
logging.basicConfig(
    filename='logs/api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# API response models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    language: Optional[str] = "vi"

class ChatResponse(BaseModel):
    response: str
    confidence: float
    suggestions: List[str] = []
    metadata: Optional[Dict] = None

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Xử lý tin nhắn
        response = chatbot.process_query(request.message)
        
        # Tạo response
        return ChatResponse(
            response=response,
            confidence=0.9,
            suggestions=[
                "Xem menu",
                "Đặt bàn",
                "Món đặc sản"
            ]
        )
    except Exception as e:
        logging.error(f"Error processing chat request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dishes/search")
async def search_dishes(q: str):
    try:
        results = chatbot.search_dishes(q)
        return {
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        logging.error(f"Error searching dishes: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/menu")
async def get_menu():
    try:
        return {"categories": chatbot.get_menu_categories()}
    except Exception as e:
        logging.error(f"Error fetching menu: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/train")
async def train_model():
    try:
        success = chatbot.train_model()
        return {"status": "success" if success else "failed"}
    except Exception as e:
        logging.error(f"Error training model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api.routes:app", host="0.0.0.0", port=8000, reload=True) 