from fastapi import HTTPException, status
from typing import Optional

class ChatbotException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: Optional[str] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

class ModelNotFoundError(ChatbotException):
    def __init__(self):
        super().__init__(
            status_code=status_code.HTTP_404_NOT_FOUND,
            detail="AI model not found or not loaded",
            error_code="MODEL_NOT_FOUND"
        )

class DatabaseError(ChatbotException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status_code.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="DATABASE_ERROR"
        )

class CrawlerError(ChatbotException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status_code.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="CRAWLER_ERROR"
        ) 