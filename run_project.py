import os
import subprocess
import time
import logging
from typing import List, Dict
import json

class ProjectRunner:
    def __init__(self):
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Thiết lập logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('project_setup.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def setup_environment(self) -> bool:
        """Bước 1: Cài đặt môi trường"""
        try:
            self.logger.info("Bước 1: Bắt đầu cài đặt môi trường...")
            
            # Chạy setup.py
            subprocess.run([sys.executable, "setup.py"], check=True)
            
            self.logger.info("✓ Hoàn thành cài đặt môi trường")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"✗ Lỗi khi cài đặt môi trường: {str(e)}")
            return False

    def collect_data(self) -> bool:
        """Bước 2: Thu thập dữ liệu"""
        try:
            self.logger.info("Bước 2: Bắt đầu thu thập dữ liệu...")
            
            # Chạy crawler
            from food_crawler import VietnamFoodCrawler
            crawler = VietnamFoodCrawler()
            crawler.run()
            crawler.export_to_json()
            
            self.logger.info("✓ Hoàn thành thu thập dữ liệu")
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Lỗi khi thu thập dữ liệu: {str(e)}")
            return False

    def train_model(self) -> bool:
        """Bước 3: Training AI model"""
        try:
            self.logger.info("Bước 3: Bắt đầu training model...")
            
            # Tạo training data mẫu
            training_data = self._create_sample_training_data()
            
            # Training model
            from ai_model import FoodAIModel
            model = FoodAIModel()
            model.train(training_data)
            
            self.logger.info("✓ Hoàn thành training model")
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Lỗi khi training model: {str(e)}")
            return False

    def _create_sample_training_data(self) -> List[Dict]:
        """Tạo dữ liệu training mẫu"""
        training_data = [
            {
                "text": "cho tôi xem món phở",
                "intent": "món_ăn"
            },
            {
                "text": "cách nấu bún bò huế",
                "intent": "công_thức"
            },
            {
                "text": "nguyên liệu nấu phở",
                "intent": "nguyên_liệu"
            },
            {
                "text": "đặt bàn tối nay",
                "intent": "đặt_bàn"
            },
            {
                "text": "giá món này bao nhiêu",
                "intent": "giá_cả"
            },
            # Thêm nhiều mẫu training khác...
        ]
        return training_data

    def start_chatbot(self) -> bool:
        """Bước 4: Khởi động chatbot"""
        try:
            self.logger.info("Bước 4: Khởi động chatbot...")
            
            from smart_chatbot import SmartFoodChatbot
            chatbot = SmartFoodChatbot()
            
            print("\n" + "="*50)
            print("Chatbot đã sẵn sàng phục vụ!")
            print("Gõ 'tạm biệt' để thoát")
            print("="*50 + "\n")
            
            while True:
                user_input = input("Khách: ")
                if user_input.lower() in ['tạm biệt', 'goodbye', 'bye']:
                    print("Chatbot: Cảm ơn quý khách đã sử dụng dịch vụ. Chúc quý khách ngon miệng ạ!")
                    break
                    
                response = chatbot.process_query(user_input)
                print("Chatbot:", response)
            
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Lỗi khi chạy chatbot: {str(e)}")
            return False

    def run_all(self):
        """Chạy tất cả các bước"""
        steps = [
            (self.setup_environment, "Cài đặt môi trường"),
            (self.collect_data, "Thu thập dữ liệu"),
            (self.train_model, "Training model"),
            (self.start_chatbot, "Khởi động chatbot")
        ]
        
        print("\n=== BẮT ĐẦU KHỞI ĐỘNG HỆ THỐNG ===\n")
        
        for step_func, step_name in steps:
            print(f"\n>> Đang thực hiện: {step_name}...")
            success = step_func()
            
            if not success:
                print(f"\n✗ Lỗi khi {step_name.lower()}!")
                print("Dừng quá trình thiết lập!")
                return
            
            print(f"✓ Hoàn thành: {step_name}")
            time.sleep(1)

if __name__ == "__main__":
    import sys
    
    runner = ProjectRunner()
    
    if len(sys.argv) > 1:
        # Chạy một bước cụ thể
        step = sys.argv[1]
        if step == "setup":
            runner.setup_environment()
        elif step == "data":
            runner.collect_data()
        elif step == "train":
            runner.train_model()
        elif step == "chat":
            runner.start_chatbot()
        else:
            print("Bước không hợp lệ! Các bước có thể chạy: setup, data, train, chat")
    else:
        # Chạy tất cả các bước
        runner.run_all() 