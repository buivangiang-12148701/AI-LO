import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_schema import Base, Dish, Ingredient, RecipeStep
import re
import unicodedata

class FoodDataProcessor:
    def __init__(self):
        self.engine = create_engine('sqlite:///vietnam_food.db')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def normalize_vietnamese(self, text: str) -> str:
        """Chuẩn hóa văn bản tiếng Việt"""
        text = unicodedata.normalize('NFKC', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def clean_data(self):
        """Làm sạch dữ liệu trong database"""
        dishes = self.session.query(Dish).all()
        
        for dish in dishes:
            dish.name_vi = self.normalize_vietnamese(dish.name_vi)
            dish.description_vi = self.normalize_vietnamese(dish.description_vi)
            
        self.session.commit()

    def export_training_data(self):
        """Xuất dữ liệu để training AI"""
        dishes = self.session.query(Dish).all()
        
        training_data = []
        for dish in dishes:
            training_data.append({
                'text': f"{dish.name_vi}. {dish.description_vi}",
                'intent': 'food_info',
                'entities': [
                    {'start': 0, 'end': len(dish.name_vi), 'label': 'DISH_NAME'},
                ]
            })
            
        return training_data

if __name__ == "__main__":
    processor = FoodDataProcessor()
    processor.clean_data() 