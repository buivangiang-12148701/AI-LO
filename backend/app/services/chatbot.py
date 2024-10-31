from typing import Dict, Tuple, Optional, List
from app.services.base import BaseService
from app.services.ai_model import AIModel
from app.core.exceptions import ModelNotFoundError, DatabaseError
from app.models.dish import Dish
from app.schemas.chat import ChatRequest, ChatResponse

class ChatbotService(BaseService):
    def __init__(self, db: Session, cache: Optional[RedisCache] = None):
        super().__init__(db, cache)
        self.model = AIModel()
        self._load_model()

    def _load_model(self):
        """Load AI model"""
        try:
            self.model.load()
        except Exception as e:
            self._log_error(e, "Failed to load AI model")
            raise ModelNotFoundError()

    def process_query(self, request: ChatRequest) -> ChatResponse:
        """Process user query"""
        try:
            # Try to get from cache first
            cache_key = self._get_cache_key("chat", request.message)
            if self.cache:
                cached_response = self.cache.get(cache_key)
                if cached_response:
                    return ChatResponse(**cached_response)

            # Predict intent
            intent = self.model.predict_intent(request.message)
            
            # Get response based on intent
            response, confidence = self._get_response(request.message, intent)
            
            # Create response object
            chat_response = ChatResponse(
                response=response,
                confidence=confidence,
                suggestions=self._get_suggestions(intent),
                metadata={"intent": intent}
            )

            # Cache the response
            if self.cache:
                self.cache.set(cache_key, chat_response.dict())

            return chat_response

        except ModelNotFoundError:
            raise
        except Exception as e:
            self._log_error(e, "Error processing query")
            raise DatabaseError("Failed to process query")

    def _get_response(self, query: str, intent: str) -> Tuple[str, float]:
        """Get response based on intent"""
        try:
            if intent == "món_ăn":
                return self._get_dish_info(query)
            elif intent == "công_thức":
                return self._get_recipe(query)
            elif intent == "đặt_bàn":
                return self._handle_booking(query)
            else:
                return self._get_general_response(query)
        except Exception as e:
            self._log_error(e, "Error getting response")
            raise

    def _get_dish_info(self, query: str) -> Tuple[str, float]:
        """Get dish information"""
        dish = self.db.query(Dish).filter(
            Dish.name_vi.ilike(f"%{query}%")
        ).first()

        if dish:
            response = (
                f"Dạ, {dish.name_vi} là {dish.description_vi}. "
                f"Món ăn thuộc danh mục {dish.category} "
                f"và là đặc sản vùng {dish.region} ạ."
            )
            return response, 0.9
        return "Xin lỗi, em chưa có thông tin về món này.", 0.5

    def _get_suggestions(self, intent: str) -> List[str]:
        """Get context-aware suggestions"""
        suggestions = {
            "món_ăn": ["Xem menu", "Món đặc sản", "Món mới"],
            "công_thức": ["Công thức phở", "Cách nấu bún bò", "Hướng dẫn nấu ăn"],
            "đặt_bàn": ["Đặt bàn", "Xem giờ mở cửa", "Liên hệ"],
            "default": ["Xem menu", "Đặt bàn", "Món đặc sản"]
        }
        return suggestions.get(intent, suggestions["default"])

    def train_model(self, training_data: List[Dict]) -> bool:
        """Train model with new data"""
        try:
            success = self.model.train(training_data)
            if success and self.cache:
                self.cache.delete_pattern("chat:*")  # Clear chat cache
            return success
        except Exception as e:
            self._log_error(e, "Error training model")
            return False 