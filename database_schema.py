from sqlalchemy import create_engine, Column, Integer, String, Text, Float, Boolean, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Bảng liên kết nhiều-nhiều giữa món ăn và nguyên liệu
dish_ingredient = Table('dish_ingredient', Base.metadata,
    Column('dish_id', Integer, ForeignKey('dishes.id')),
    Column('ingredient_id', Integer, ForeignKey('ingredients.id'))
)

class Dish(Base):
    __tablename__ = 'dishes'
    
    id = Column(Integer, primary_key=True)
    name_vi = Column(String(200), nullable=False)  # Tên tiếng Việt
    name_en = Column(String(200))  # Tên tiếng Anh
    description_vi = Column(Text)  # Mô tả tiếng Việt
    description_en = Column(Text)  # Mô tả tiếng Anh
    region = Column(String(50))  # Vùng miền
    category = Column(String(50))  # Phân loại món ăn
    cooking_time = Column(Integer)  # Thời gian nấu (phút)
    difficulty = Column(String(20))  # Độ khó
    calories = Column(Float)  # Calories
    price_range = Column(String(50))  # Khoảng giá
    is_vegetarian = Column(Boolean, default=False)
    image_url = Column(String(500))  # URL hình ảnh
    
    ingredients = relationship('Ingredient', secondary=dish_ingredient, back_populates='dishes')
    recipe_steps = relationship('RecipeStep', back_populates='dish')
    
class Ingredient(Base):
    __tablename__ = 'ingredients'
    
    id = Column(Integer, primary_key=True)
    name_vi = Column(String(100), nullable=False)
    name_en = Column(String(100))
    description_vi = Column(Text)
    description_en = Column(Text)
    category = Column(String(50))  # Phân loại nguyên liệu
    unit = Column(String(20))  # Đơn vị tính
    
    dishes = relationship('Dish', secondary=dish_ingredient, back_populates='ingredients')

class RecipeStep(Base):
    __tablename__ = 'recipe_steps'
    
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'))
    step_number = Column(Integer)
    instruction_vi = Column(Text, nullable=False)
    instruction_en = Column(Text)
    
    dish = relationship('Dish', back_populates='recipe_steps') 