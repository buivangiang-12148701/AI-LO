# Vietnamese Food Chatbot 🍜

Chatbot thông minh về ẩm thực Việt Nam với khả năng tự học và cập nhật thông tin tự động. Hỗ trợ trả lời các câu hỏi về món ăn, công thức nấu và văn hóa ẩm thực Việt Nam.

## Author

**VG-PA**

- GitHub: [@buivangiang-12148701](https://github.com/buivangiang-12148701)
- Email: **\*\*\*\***\*\*\*\***\*\*\*\***@gmail.com

## 📋 Tính Năng Chính

- 💬 Chat tự nhiên bằng tiếng Việt
- 🔍 Tìm kiếm thông tin món ăn
- 📝 Xem công thức nấu ăn chi tiết
- 🌟 Gợi ý món ăn theo vùng miền
- 🤖 Tự động cập nhật dữ liệu mới
- 📱 Giao diện thân thiện, responsive

## 🚀 Hướng Dẫn Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.8+
- Node.js 14+
- Docker & Docker Compose (tùy chọn)
- Git

### Cách 1: Sử Dụng Script Tự Động (Khuyến nghị)

1. Clone repository:
   bash
   git clone https://github.com/buivangiang-12148701/AI-LO.git
   cd vietnamese-food-chatbot
3. Chạy script cài đặt:
   bash
   python install.py

Script sẽ tự động:

- Kiểm tra và cài đặt các yêu cầu hệ thống
- Tạo môi trường ảo Python
- Cài đặt dependencies
- Thiết lập database
- Cấu hình môi trường

### Cách 2: Cài Đặt Thủ Công

1. **Backend**:
   bash
   Tạo và kích hoạt môi trường ảo
   python -m venv venv
   source venv/bin/activate # Linux/Mac
   hoặc
   bash
   Tạo và kích hoạt môi trường ảo
   python -m venv venv
   source venv/bin/activate # Linux/Mac
   hoặc
   .\venv\Scripts\activate # Windows
   Cài đặt dependencies
   cd backend
   pip install -r requirements.txt
   Tạo file .env
   cp .env.example .env
   Khởi tạo database
   python scripts/init_db.py
   alembic upgrade head

2. **Frontend**:

bash
cd frontend
Cài đặt dependencies
npm install
Tạo file .env.local
cp .env.example .env.local

### Cách 3: Sử Dụng Docker

bash
Build và chạy containers
docker-compose up -d
Kiểm tra logs
docker-compose logs -f

## 💻 Chạy Ứng Dụng

### Development Mode

1. **Backend**:

bash
cd backend
uvicorn app.main:app --reload

Backend API sẽ chạy tại: http://localhost:8000

2. **Frontend**:

bash
cd frontend
npm run dev

Frontend sẽ chạy tại: http://localhost:3000

### Production Mode

1. **Backend**:

bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 2. **Frontend**:

bash
cd frontend
npm run build
npm start

## 🔧 Cấu Hình

### Backend (.env)

env
API_V1_STR=/api/v1
DATABASE_URL=sqlite:///./food_chatbot.db
REDIS_HOST=localhost
REDIS_PORT=6379

### Frontend (.env.local)

env
NEXT_PUBLIC_API_URL=http://localhost:8000

## 📚 API Documentation

Truy cập Swagger UI: http://localhost:8000/docs

Các endpoint chính:

- POST `/api/v1/chat`: Chat với bot
- GET `/api/v1/menu`: Lấy danh sách menu
- GET `/api/v1/dishes/search`: Tìm kiếm món ăn

## 🧪 Testing

### Backend Tests

bash
cd backend
pytest

bash
cd frontend
npm test

## 📊 Monitoring

1. Truy cập Grafana: http://localhost:3000

   - Username: admin
   - Password: secret

2. Import dashboards từ `monitoring/grafana/dashboards/`

## 🔍 Debug Mode

### Backend

bash
Bật debug logs
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload --log-level debug

### Frontend

bash
Bật development tools
npm run dev -- --debug

## 🛠 Maintenance

### Cập Nhật Dữ Liệu

bash
python scripts/update_data.py

### Backup Database

bash
python scripts/backup_db.py

### Clear Cache

## 🔒 Security

- API được bảo vệ bởi rate limiting
- CORS được cấu hình chặt chẽ
- Input validation cho tất cả endpoints
- Sanitization cho user input

## 🚀 Deployment

### Using Docker (Recommended)

git clone https://github.com/buivangiang-12148701/AI-LO.git
cd vietnamese-food-chatbot 2. Chạy script cài đặt:
bash
python install.py
Script sẽ tự động:

- Kiểm tra và cài đặt các yêu cầu hệ thống
- Tạo môi trường ảo Python
- Cài đặt dependencies
- Thiết lập database
- Cấu hình môi trường

### Cách 2: Cài Đặt Thủ Công

1. **Backend**:
   bash
   Tạo và kích hoạt môi trường ảo
   python -m venv venv
   source venv/bin/activate # Linux/Mac
   hoặc
   .\venv\Scripts\activate # Windows
   Cài đặt dependencies
   cd backend
   pip install -r requirements.txt
   Tạo file .env
   cp .env.example .env
   Khởi tạo database
   python scripts/init_db.py
   alembic upgrade head
2. **Frontend**:
   bash
   cd frontend
   Cài đặt dependencies
   npm install
   Tạo file .env.local
   cp .env.example .env.local

### Cách 3: Sử Dụng Docker

bash
Build và chạy containers
docker-compose up -d
Kiểm tra logs
docker-compose logs -f

## 💻 Chạy Ứng Dụng

### Development Mode

1. **Backend**:
   bash
   cd backend
   uvicorn app.main:app --reload
   Backend API sẽ chạy tại: http://localhost:8000

2. **Frontend**:
   bash
   cd frontend
   npm run dev
   Frontend sẽ chạy tại: http://localhost:3000

### Production Mode

1. **Backend**:
   bash
   cd backend
   uvicorn app.main:app --host 0.0.0.0 --port 8000
2. **Frontend**:
   bash
   cd frontend
   npm run build
   npm start

## 🔧 Cấu Hình

### Backend (.env)

env
API_V1_STR=/api/v1
DATABASE_URL=sqlite:///./food_chatbot.db
REDIS_HOST=localhost
REDIS_PORT=6379

### Frontend (.env.local)

env
NEXT_PUBLIC_API_URL=http://localhost:8000

## 📚 API Documentation

Truy cập Swagger UI: http://localhost:8000/docs

Các endpoint chính:

- POST `/api/v1/chat`: Chat với bot
- GET `/api/v1/menu`: Lấy danh sách menu
- GET `/api/v1/dishes/search`: Tìm kiếm món ăn

## 🧪 Testing

### Backend Tests

bash
cd backend
pytest
Tests
bash
cd frontend
npm test

## 📊 Monitoring

1. Truy cập Grafana: http://localhost:3000

   - Username: admin
   - Password: secret

2. Import dashboards từ `monitoring/grafana/dashboards/`

## 🔍 Debug Mode

### Backend

bash
Bật debug logs
export LOG_LEVEL=DEBUG
uvicorn app.main:app --reload --log-level debug

### Frontend

bash
Bật development tools
npm run dev -- --debug

## 🛠 Maintenance

### Cập Nhật Dữ Liệu

bash
python scripts/update_data.py

### Backup Database

bash
python scripts/backup_db.py

### Clear Cache

bash
python scripts/clear_cache.py

## 🔒 Security

- API được bảo vệ bởi rate limiting
- CORS được cấu hình chặt chẽ
- Input validation cho tất cả endpoints
- Sanitization cho user input

## 🚀 Deployment

### Using Docker (Recommended)

bash
docker-compose -f docker-compose.prod.yml up -d

### Manual Deployment

Xem hướng dẫn chi tiết trong `docs/deployment.md`

## 📁 Cấu Trúc Thư Mục

vietnamese_food_chatbot/
├── backend/ # Backend service
│ ├── app/ # Core application
│ │ ├── api/ # API endpoints
│ │ ├── core/ # Core functionality
│ │ ├── models/ # Database models
│ │ ├── schemas/ # Pydantic schemas
│ │ └── services/ # Business logic
│ ├── tests/ # Backend tests
│ └── alembic/ # Database migrations
├── frontend/ # Frontend application
│ ├── src/ # Source code
│ │ ├── components/ # React components
│ │ ├── hooks/ # Custom hooks
│ │ ├── store/ # Redux store
│ │ └── services/ # API services
│ └── tests/ # Frontend tests
├── data/ # Data storage
├── docs/ # Documentation
└── monitoring/ # Monitoring configuration

## 🔄 Workflow

1. **Development**:

   - Backend: FastAPI + SQLAlchemy
   - Frontend: Next.js + Redux
   - Database: SQLite (dev) / PostgreSQL (prod)
   - Cache: Redis

2. **Testing**:

   - Unit Tests: pytest, Jest
   - Integration Tests
   - E2E Tests

3. **Deployment**:
   - Docker containers
   - CI/CD pipeline
   - Monitoring with Grafana

## 📈 Performance

- Response time < 200ms
- Cache hit ratio > 80%
- Concurrent users support: 1000+
- Auto-scaling enabled

## 🔜 Roadmap

- [ ] Multi-language support
- [ ] Voice interface
- [ ] Image recognition
- [ ] Mobile app
- [ ] API marketplace

## 💡 Best Practices

- Clean Architecture
- SOLID Principles
- Test-Driven Development
- Continuous Integration
- Documentation as Code

## 🤝 Contributing

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📝 License

Copyright © 2024 VG-PA (**\*\*\*\***\*\*\*\***\*\*\*\***@gmail.com)

MIT License - Xem [LICENSE.md](LICENSE.md)

## 📫 Support & Contact

- **Author**: VG-PA
- **Email**: **\*\*\*\***\*\*\*\***\*\*\*\***@gmail.com
- **GitHub**: [@buivangiang-12148701](https://github.com/buivangiang-12148701)
- **Issues**: [GitHub Issues](https://github.com/buivangiang-12148701/vietnamese-food-chatbot/issues)

## 🙏 Acknowledgments

- [Cooky.vn](https://cooky.vn) cho dữ liệu món ăn
- [MonNgon.vn](https://monngon.vn) cho công thức nấu ăn
- Cộng đồng ẩm thực Việt Nam
