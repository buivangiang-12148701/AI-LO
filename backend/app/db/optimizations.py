from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from typing import List, Dict

class QueryOptimizer:
    def __init__(self, session: Session):
        self.session = session

    def optimize_query(self, query):
        """Tối ưu query với các hint"""
        return query.with_hints(
            Dish,
            "USE INDEX (idx_dish_name_vi)"
        )

    def batch_insert(self, objects: List[Any], batch_size: int = 1000):
        """Insert dữ liệu theo batch"""
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i + batch_size]
            self.session.bulk_save_objects(batch)
            self.session.commit()

    def create_indexes(self):
        """Tạo các index cần thiết"""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_dish_name_vi ON dishes(name_vi)",
            "CREATE INDEX IF NOT EXISTS idx_dish_category ON dishes(category)",
            "CREATE INDEX IF NOT EXISTS idx_ingredient_name ON ingredients(name_vi)"
        ]
        
        for index in indexes:
            self.session.execute(text(index))
        self.session.commit() 