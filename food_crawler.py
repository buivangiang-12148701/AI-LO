import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_schema import Base, Dish, Ingredient, RecipeStep
import logging
import time
from typing import List, Dict
import re
from urllib.parse import urljoin
import json

class VietnamFoodCrawler:
    def __init__(self):
        self.engine = create_engine('sqlite:///vietnam_food.db')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='crawler.log'
        )
        self.logger = logging.getLogger(__name__)

    def crawl_cooky_vn(self):
        """Crawler cho trang Cooky.vn"""
        base_url = "https://cooky.vn/mon-ngon"
        pages = 5  # Số trang cần crawl
        
        try:
            for page in range(1, pages + 1):
                url = f"{base_url}?page={page}"
                response = requests.get(url, headers=self.headers)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                recipes = soup.find_all('div', class_='recipe-item')
                
                for recipe in recipes:
                    # Lấy link chi tiết món ăn
                    recipe_link = recipe.find('a')['href']
                    recipe_url = urljoin(base_url, recipe_link)
                    
                    # Crawl trang chi tiết
                    recipe_data = self._crawl_cooky_recipe_detail(recipe_url)
                    if recipe_data:
                        self._save_dish(recipe_data)
                
                time.sleep(1)  # Tránh request quá nhanh
                
        except Exception as e:
            self.logger.error(f"Lỗi khi crawl Cooky.vn: {str(e)}")

    def _crawl_cooky_recipe_detail(self, url: str) -> Dict:
        """Crawl chi tiết món ăn từ Cooky.vn"""
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Lấy thông tin chi tiết
            name = soup.find('h1', class_='recipe-title').text.strip()
            description = soup.find('div', class_='recipe-description').text.strip()
            
            # Lấy nguyên liệu
            ingredients = []
            ingredient_items = soup.find_all('div', class_='ingredient-item')
            for item in ingredient_items:
                ingredients.append({
                    'name': item.find('span', class_='name').text.strip(),
                    'amount': item.find('span', class_='amount').text.strip()
                })
            
            # Lấy các bước nấu
            steps = []
            step_items = soup.find_all('div', class_='step-item')
            for i, step in enumerate(step_items, 1):
                steps.append({
                    'step_number': i,
                    'instruction': step.find('div', class_='step-desc').text.strip()
                })
            
            return {
                'name_vi': name,
                'description_vi': description,
                'ingredients': ingredients,
                'recipe_steps': steps,
                'image_url': soup.find('img', class_='recipe-image')['src'],
                'category': self._detect_category(name, description),
                'region': self._detect_region(name, description)
            }
            
        except Exception as e:
            self.logger.error(f"Lỗi khi crawl chi tiết món ăn {url}: {str(e)}")
            return None

    def crawl_monngon_vn(self):
        """Crawler cho MonNgon.vn"""
        base_url = "https://monngon.com.vn/cong-thuc"
        try:
            response = requests.get(base_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            recipes = soup.find_all('article', class_='recipe-item')
            for recipe in recipes:
                recipe_url = recipe.find('a')['href']
                recipe_data = self._crawl_monngon_recipe_detail(recipe_url)
                if recipe_data:
                    self._save_dish(recipe_data)
                time.sleep(1)
                
        except Exception as e:
            self.logger.error(f"Lỗi khi crawl MonNgon.vn: {str(e)}")

    def crawl_esheep_vn(self):
        """Crawler cho ESheep Kitchen"""
        base_url = "https://esheepkitchen.com/"
        # Tương tự như các hàm crawl trên...

    def _detect_category(self, name: str, description: str) -> str:
        """Phát hiện danh mục món ăn dựa trên tên và mô tả"""
        text = f"{name} {description}".lower()
        
        categories = {
            'món soup': ['phở', 'bún', 'soup', 'canh', 'cháo'],
            'món chính': ['cơm', 'xào', 'kho', 'nướng', 'chiên'],
            'món ăn nhẹ': ['bánh', 'chè', 'salad', 'gỏi'],
            'món tráng miệng': ['chè', 'bánh ngọt', 'kem', 'pudding']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                return category
                
        return 'khác'

    def _detect_region(self, name: str, description: str) -> str:
        """Phát hiện vùng miền của món ăn"""
        text = f"{name} {description}".lower()
        
        regions = {
            'Bắc': ['hà nội', 'bắc bộ', 'nam định', 'hải phòng'],
            'Trung': ['huế', 'đà nẵng', 'quảng nam', 'miền trung'],
            'Nam': ['sài gòn', 'miền nam', 'cần thơ', 'mekong']
        }
        
        for region, keywords in regions.items():
            if any(keyword in text for keyword in keywords):
                return region
                
        return 'không xác định'

    def _save_dish(self, dish_data: Dict):
        """Lưu thông tin món ăn vào database"""
        try:
            # Tạo món ăn mới
            dish = Dish(
                name_vi=dish_data['name_vi'],
                description_vi=dish_data['description_vi'],
                image_url=dish_data.get('image_url', ''),
                category=dish_data.get('category', 'khác'),
                region=dish_data.get('region', 'không xác định')
            )
            self.session.add(dish)
            self.session.flush()  # Để lấy dish.id
            
            # Lưu nguyên liệu
            for ing_data in dish_data.get('ingredients', []):
                ingredient = Ingredient(
                    name_vi=ing_data['name'],
                    unit=self._extract_unit(ing_data['amount'])
                )
                self.session.add(ingredient)
                dish.ingredients.append(ingredient)
            
            # Lưu các bước nấu
            for step_data in dish_data.get('recipe_steps', []):
                step = RecipeStep(
                    dish_id=dish.id,
                    step_number=step_data['step_number'],
                    instruction_vi=step_data['instruction']
                )
                self.session.add(step)
            
            self.session.commit()
            self.logger.info(f"Đã lưu món ăn: {dish_data['name_vi']}")
            
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Lỗi khi lưu món ăn: {str(e)}")

    def _extract_unit(self, amount_str: str) -> str:
        """Trích xuất đơn vị đo từ chuỗi số lượng"""
        units = ['g', 'kg', 'ml', 'l', 'muỗng', 'chén', 'củ', 'quả', 'cái']
        amount_str = amount_str.lower()
        
        for unit in units:
            if unit in amount_str:
                return unit
        return 'không xác định'

    def run(self):
        """Chạy tất cả các crawler"""
        self.logger.info("Bắt đầu crawl dữ liệu...")
        
        self.crawl_cooky_vn()
        self.crawl_monngon_vn()
        self.crawl_esheep_vn()
        
        self.logger.info("Hoàn thành crawl dữ liệu!")
        
    def export_to_json(self, filename: str = 'vietnam_food_data.json'):
        """Xuất dữ liệu đã crawl ra file JSON"""
        try:
            dishes = self.session.query(Dish).all()
            data = []
            
            for dish in dishes:
                dish_data = {
                    'name_vi': dish.name_vi,
                    'description_vi': dish.description_vi,
                    'category': dish.category,
                    'region': dish.region,
                    'ingredients': [
                        {'name': ing.name_vi, 'unit': ing.unit}
                        for ing in dish.ingredients
                    ],
                    'recipe_steps': [
                        {
                            'step_number': step.step_number,
                            'instruction': step.instruction_vi
                        }
                        for step in dish.recipe_steps
                    ]
                }
                data.append(dish_data)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            self.logger.info(f"Đã xuất dữ liệu ra file {filename}")
            
        except Exception as e:
            self.logger.error(f"Lỗi khi xuất dữ liệu: {str(e)}")

if __name__ == "__main__":
    crawler = VietnamFoodCrawler()
    crawler.run()
    crawler.export_to_json() 