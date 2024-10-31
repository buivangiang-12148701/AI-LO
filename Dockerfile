# Sử dụng Python 3.8 base image
FROM python:3.8-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy requirements và cài đặt dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Tạo các thư mục cần thiết
RUN mkdir -p data logs models

# Expose port
EXPOSE 8000

# Chạy ứng dụng
CMD ["uvicorn", "api.routes:app", "--host", "0.0.0.0", "--port", "8000"] 