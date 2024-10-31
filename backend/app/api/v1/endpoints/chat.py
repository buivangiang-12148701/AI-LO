from fastapi import APIRouter, Depends, BackgroundTasks
from app.core.cache import RedisCache
from app.services.chatbot import ChatbotService

router = APIRouter()

@router.post("/chat")
async def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    chatbot: ChatbotService = Depends(get_chatbot),
    cache: RedisCache = Depends(get_cache)
):
    # Try cache
    cache_key = f"chat:{request.message}"
    if cached := cache.get(cache_key):
        return cached
        
    # Process in background if complex query
    if is_complex_query(request.message):
        background_tasks.add_task(
            process_complex_query,
            request.message
        )
        return {
            "message": "Processing complex query",
            "status": "pending"
        }
        
    # Normal processing
    response = chatbot.process_query(request)
    cache.set(cache_key, response)
    return response 