from ai_model import FoodAIModel
from food_crawler import VietnamFoodCrawler
import json
import logging

class SmartFoodChatbot:
    def __init__(self):
        self.ai_model = FoodAIModel()
        self.crawler = VietnamFoodCrawler()
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='logs/chatbot.log'
        )
        self.logger = logging.getLogger(__name__)

    def process_query(self, user_input: str) -> str:
        """Xử lý câu hỏi của người dùng"""
        try:
            # Dự đoán intent
            intent = self.ai_model.predict_intent(user_input)
            
            # Tìm thông tin trong database
            food_match, confidence = self.ai_model.find_best_match(user_input)
            
            if food_match and confidence > 0.5:
                return self._format_food_response(food_match, intent)
            else:
                # Nếu không tìm thấy trong database, crawl thêm dữ liệu
                self.logger.info(f"Crawling new data for query: {user_input}")
                self.crawler.run()
                
                # Thử tìm lại trong dữ liệu mới
                food_match, confidence = self.ai_model.find_best_match(user_input)
                if food_match and confidence > 0.5:
                    return self._format_food_response(food_match, intent)
                
                return "Xin lỗi, em chưa có thông tin về món ăn này. Em sẽ cập nhật và học hỏi thêm ạ."
                
        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            return "Xin lỗi, có lỗi xảy ra. Quý khách vui lòng thử lại sau ạ."

    def _format_food_response(self, food_data: dict, intent: str) -> str:
        """Format câu trả lời dựa trên intent"""
        if intent == 'món_ăn':
            return (f"Dạ, {food_data['name_vi']} là {food_data['description_vi']}. "
                   f"Món ăn thuộc danh mục {food_data['category']} "
                   f"và là đặc sản vùng {food_data['region']} ạ.")
                   
        elif intent == 'công_thức':
            steps = "\n".join([f"{step['step_number']}. {step['instruction']}" 
                             for step in food_data['recipe_steps']])
            return f"Dạ, công thức nấu {food_data['name_vi']} như sau:\n{steps}"
            
        elif intent == 'nguyên_liệu':
            ingredients = "\n".join([f"- {ing['name']}: {ing['unit']}" 
                                   for ing in food_data['ingredients']])
            return f"Dạ, nguyên liệu nấu {food_data['name_vi']} gồm có:\n{ingredients}"
            
        return f"Dạ, đây là thông tin về món {food_data['name_vi']}: {food_data['description_vi']}"

def main():
    chatbot = SmartFoodChatbot()
    print("Chatbot: Xin chào! Em là trợ lý ảo về ẩm thực Việt Nam. Em có thể giúp gì cho quý khách ạ?")
    
    while True:
        user_input = input("Khách: ")
        if user_input.lower() in ['tạm biệt', 'goodbye', 'bye']:
            print("Chatbot: Cảm ơn quý khách đã sử dụng dịch vụ. Chúc quý khách ngon miệng ạ!")
            break
            
        response = chatbot.process_query(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    main() 