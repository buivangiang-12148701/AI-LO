from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name_vi = Column(String(200), nullable=False)
    name_en = Column(String(200))
    description_vi = Column(Text)
    description_en = Column(Text)
    region = Column(String(50))
    category = Column(String(50))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    calories = Column(Float)
    price_range = Column(String(50))
    is_vegetarian = Column(Boolean, default=False)
    image_url = Column(String(500))

    ingredients = relationship("Ingredient", secondary="dish_ingredient")
    recipe_steps = relationship("RecipeStep", back_populates="dish") 