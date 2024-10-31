from pydantic import BaseModel, validator, constr
from typing import Optional, List
import re

class ChatInput(BaseModel):
    message: constr(min_length=1, max_length=500)
    session_id: Optional[str]
    language: Optional[str] = "vi"
    
    @validator('message')
    def validate_message(cls, v):
        # Remove special characters
        v = re.sub(r'[^\w\s]', '', v)
        return v.strip()
        
    @validator('language')
    def validate_language(cls, v):
        allowed = ['vi', 'en']
        if v not in allowed:
            raise ValueError(f'Language must be one of: {allowed}')
        return v

class DishInput(BaseModel):
    name: constr(min_length=1, max_length=200)
    description: Optional[str]
    category: Optional[str]
    ingredients: List[str]
    
    @validator('category')
    def validate_category(cls, v):
        allowed = ['món soup', 'món chính', 'món ăn nhẹ', 'món tráng miệng']
        if v and v not in allowed:
            raise ValueError(f'Category must be one of: {allowed}')
        return v 