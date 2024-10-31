from typing import Dict, List
import random

class FBChatbot:
    def __init__(self):
        self.menu_categories = {
            "món soup": {
                "phở": {
                    "description": "Món ăn truyền thống với nước dùng đặc trưng, bánh phở và các loại thịt",
                    "variants": ["Phở bò tái", "Phở gà", "Phở bò viên", "Phở đặc biệt"],
                    "price_range": "45.000đ - 85.000đ",
                    "best_seller": True
                },
                "bún bò huế": {
                    "description": "Bún bò cay cay với nước dùng đặc trưng xứ Huế, ăn kèm rau sống",
                    "variants": ["Bún bò gốc Huế", "Bún bò đặc biệt", "Bún bò giò heo"],
                    "price_range": "55.000đ - 75.000đ",
                    "spicy_level": "Cay vừa-mạnh"
                },
                "bún riêu": {
                    "description": "Bún với nước dùng cua đồng, cà chua và đậu phụ rán",
                    "variants": ["Bún riêu cua", "Bún riêu ốc", "Bún riêu đặc biệt"],
                    "price_range": "45.000đ - 65.000đ"
                }
            },
            "món chính": {
                "cơm tấm": {
                    "description": "Cơm với sườn nướng, bì, chả, trứng ốp la",
                    "variants": ["Cơm tấm sườn bì chả", "Cơm tấm đặc biệt", "Cơm tấm sườn nướng"],
                    "price_range": "45.000đ - 75.000đ",
                    "best_seller": True
                },
                "bún chả": {
                    "description": "Bún với chả viên và thịt nướng, nước mắm chua ngọt",
                    "variants": ["Bún chả Hà Nội", "Bún chả đặc biệt"],
                    "price_range": "55.000đ - 85.000đ",
                    "origin": "Hà Nội"
                }
            },
            "món ăn nhẹ": {
                "bánh mì": {
                    "description": "Bánh mì giòn với nhân đa dạng",
                    "variants": ["Bánh mì thịt", "Bánh mì gà", "Bánh mì chả", "Bánh mì đặc biệt"],
                    "price_range": "15.000đ - 35.000đ",
                    "best_seller": True
                },
                "gỏi cuốn": {
                    "description": "Cuốn tôm thịt với rau sống và bún",
                    "variants": ["Gỏi cuốn tôm thịt", "Gỏi cuốn chay"],
                    "price_range": "35.000đ - 55.000đ/2 cuốn",
                    "healthy_choice": True
                }
            }
        }

        self.responses = {
            "chào": [
                "Xin chào quý khách! Em có thể giúp gì cho quý khách ạ?",
                "Chào quý khách, rất vui được phục vụ quý khách!",
                "Kính chào quý khách, em có thể hỗ trợ gì ạ?"
            ],
            "menu": [
                f"Dạ, nhà hàng chúng em có các danh mục món ăn sau:\n" + 
                "\n".join([f"- {category.title()}" for category in self.menu_categories.keys()]) +
                "\nQuý khách muốn xem phần nào ạ?",
            ],
            "món soup": [
                self._format_category_menu("món soup")
            ],
            "món chính": [
                self._format_category_menu("món chính")
            ],
            "món ăn nhẹ": [
                self._format_category_menu("món ăn nhẹ")
            ],
            "đặc sản": [
                "Dạ, các món đặc sản của nhà hàng gồm có:\n" +
                "- Phở bò (Best seller)\n" +
                "- Bún chả Hà Nội (Món Bắc)\n" +
                "- Bún bò Huế (Món Trung)\n" +
                "- Cơm tấm (Món Nam)"
            ],
            "đặt bàn": [
                "Dạ, để đặt bàn quý khách vui lòng cho em biết:\n- Thời gian\n- Số người\n- Có yêu cầu đặc biệt không ạ?",
                "Em có thể giúp quý khách đặt bàn. Quý khách dự định dùng bữa vào thời gian nào ạ?"
            ],
            "giờ mở cửa": [
                "Nhà hàng mở cửa từ 7h00 - 22h00 các ngày trong tuần ạ",
                "Chúng em phục vụ từ 7h00 sáng đến 22h00 tối hàng ngày ạ"
            ]
        }
        
        self.default_responses = [
            "Xin lỗi quý khách, em chưa hiểu rõ yêu cầu. Quý khách có thể nói rõ hơn được không ạ?",
            "Dạ, quý khách có thể diễn đạt theo cách khác được không ạ?",
            "Em xin phép được kết nối với nhân viên để hỗ trợ quý khách tốt hơn ạ."
        ]

    def _format_category_menu(self, category: str) -> str:
        if category not in self.menu_categories:
            return "Xin lỗi, danh mục này không tồn tại."
        
        result = f"Dạ, đây là các món {category} của nhà hàng:\n"
        for dish, details in self.menu_categories[category].items():
            result += f"\n- {dish.title()}:\n"
            result += f"  + Mô tả: {details['description']}\n"
            result += f"  + Giá: {details['price_range']}\n"
            if "best_seller" in details and details["best_seller"]:
                result += "  + Best seller!\n"
        return result

    def process_input(self, user_input: str) -> str:
        user_input = user_input.lower()
        
        # Xử lý các từ khóa đặc biệt về món ăn
        for dish_category in self.menu_categories.keys():
            if dish_category in user_input:
                return self._format_category_menu(dish_category)
        
        # Xử lý các câu hỏi thông thường
        for keyword, responses in self.responses.items():
            if keyword in user_input:
                return random.choice(responses)
        
        return random.choice(self.default_responses)

def main():
    chatbot = FBChatbot()
    print("Chatbot: Xin chào! Em là trợ lý ảo của nhà hàng. Em có thể giúp gì cho quý khách?")
    
    while True:
        user_input = input("Khách: ")
        if user_input.lower() in ['tạm biệt', 'goodbye', 'bye']:
            print("Chatbot: Cảm ơn quý khách đã sử dụng dịch vụ. Chúc quý khách một ngày tốt lành!")
            break
            
        response = chatbot.process_input(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()