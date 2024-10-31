import subprocess
import sys
import os

def check_python_version():
    """Kiểm tra phiên bản Python"""
    if sys.version_info < (3, 8):
        print("Cần Python 3.8 trở lên để chạy ứng dụng!")
        sys.exit(1)

def install_requirements():
    """Cài đặt các thư viện cần thiết"""
    print("Đang cài đặt các thư viện cần thiết...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Đã cài đặt xong các thư viện!")
    except subprocess.CalledProcessError:
        print("Lỗi khi cài đặt thư viện!")
        sys.exit(1)

def setup_directories():
    """Tạo các thư mục cần thiết"""
    directories = ['data', 'logs', 'models']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Đã tạo thư mục {directory}")

def main():
    print("Bắt đầu thiết lập môi trường...")
    check_python_version()
    install_requirements()
    setup_directories()
    print("Đã hoàn tất thiết lập môi trường!")

if __name__ == "__main__":
    main() 