import os
import sys
import subprocess
import platform
import shutil
from typing import List, Dict
import json
import logging

class ProjectInstaller:
    def __init__(self):
        self.logger = self._setup_logger()
        self.os_type = platform.system().lower()
        self.requirements = {
            'python': '3.8',
            'node': '14.0.0',
            'docker': '20.10.0'
        }

    def _setup_logger(self) -> logging.Logger:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('installation.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def ask_user(self, question: str, default: bool = True) -> bool:
        """Hỏi người dùng yes/no"""
        while True:
            choice = input(f"{question} [Y/n]: ").lower() or ('y' if default else 'n')
            if choice in ['y', 'n']:
                return choice == 'y'
            print("Vui lòng chọn 'y' hoặc 'n'")

    def check_system_requirements(self) -> bool:
        """Kiểm tra yêu cầu hệ thống"""
        print("\n=== Kiểm tra yêu cầu hệ thống ===")
        
        # Kiểm tra Python version
        python_version = platform.python_version()
        print(f"Python version: {python_version}")
        if python_version < self.requirements['python']:
            print(f"Cần Python {self.requirements['python']}+ để chạy ứng dụng")
            return False

        # Kiểm tra Node.js
        try:
            node_version = subprocess.check_output(['node', '-v']).decode().strip()
            print(f"Node.js version: {node_version}")
        except:
            print("Không tìm thấy Node.js")
            if self.ask_user("Bạn có muốn cài đặt Node.js không?"):
                self._install_nodejs()
            else:
                return False

        # Kiểm tra Docker
        try:
            docker_version = subprocess.check_output(['docker', '-v']).decode()
            print(f"Docker version: {docker_version}")
        except:
            print("Không tìm thấy Docker")
            if self.ask_user("Bạn có muốn cài đặt Docker không?"):
                self._install_docker()
            else:
                return False

        return True

    def setup_virtual_environment(self) -> bool:
        """Tạo và kích hoạt môi trường ảo"""
        print("\n=== Thiết lập môi trường ảo Python ===")
        try:
            if not os.path.exists('venv'):
                subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
            
            # Kích hoạt venv
            if self.os_type == 'windows':
                activate_script = os.path.join('venv', 'Scripts', 'activate')
            else:
                activate_script = os.path.join('venv', 'bin', 'activate')
            
            if self.os_type == 'windows':
                os.system(f'call {activate_script}')
            else:
                os.system(f'source {activate_script}')
                
            return True
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo môi trường ảo: {str(e)}")
            return False

    def install_backend_dependencies(self) -> bool:
        """Cài đặt dependencies cho backend"""
        print("\n=== Cài đặt dependencies cho Backend ===")
        try:
            if self.ask_user("Bạn có muốn cài đặt dependencies cho Backend không?"):
                subprocess.run([
                    'pip', 'install', '-r', 'backend/requirements.txt'
                ], check=True)
            return True
        except Exception as e:
            self.logger.error(f"Lỗi khi cài đặt backend dependencies: {str(e)}")
            return False

    def install_frontend_dependencies(self) -> bool:
        """Cài đặt dependencies cho frontend"""
        print("\n=== Cài đặt dependencies cho Frontend ===")
        try:
            if self.ask_user("Bạn có muốn cài đặt dependencies cho Frontend không?"):
                os.chdir('frontend')
                subprocess.run(['npm', 'install'], check=True)
                os.chdir('..')
            return True
        except Exception as e:
            self.logger.error(f"Lỗi khi cài đặt frontend dependencies: {str(e)}")
            return False

    def setup_database(self) -> bool:
        """Thiết lập database"""
        print("\n=== Thiết lập Database ===")
        try:
            if self.ask_user("Bạn có muốn khởi tạo database không?"):
                # Chạy migrations
                os.chdir('backend')
                subprocess.run(['alembic', 'upgrade', 'head'], check=True)
                os.chdir('..')
            return True
        except Exception as e:
            self.logger.error(f"Lỗi khi thiết lập database: {str(e)}")
            return False

    def setup_docker(self) -> bool:
        """Thiết lập Docker"""
        print("\n=== Thiết lập Docker ===")
        try:
            if self.ask_user("Bạn có muốn build Docker images không?"):
                subprocess.run(['docker-compose', 'build'], check=True)
            return True
        except Exception as e:
            self.logger.error(f"Lỗi khi thiết lập Docker: {str(e)}")
            return False

    def setup_monitoring(self) -> bool:
        """Thiết lập monitoring"""
        print("\n=== Thiết lập Monitoring ===")
        try:
            if self.ask_user("Bạn có muốn thiết lập monitoring không?"):
                subprocess.run([
                    'docker-compose',
                    '-f', 'docker-compose.monitoring.yml',
                    'up', '-d'
                ], check=True)
            return True
        except Exception as e:
            self.logger.error(f"Lỗi khi thiết lập monitoring: {str(e)}")
            return False

    def create_env_files(self) -> bool:
        """Tạo các file .env"""
        print("\n=== Tạo file .env ===")
        try:
            # Backend .env
            if not os.path.exists('backend/.env'):
                shutil.copy('backend/.env.example', 'backend/.env')
                print("Đã tạo backend/.env")

            # Frontend .env
            if not os.path.exists('frontend/.env.local'):
                shutil.copy('frontend/.env.example', 'frontend/.env.local')
                print("Đã tạo frontend/.env.local")

            return True
        except Exception as e:
            self.logger.error(f"Lỗi khi tạo file .env: {str(e)}")
            return False

    def run_tests(self) -> bool:
        """Chạy tests"""
        print("\n=== Chạy Tests ===")
        try:
            if self.ask_user("Bạn có muốn chạy tests không?"):
                # Backend tests
                os.chdir('backend')
                subprocess.run(['pytest'], check=True)
                os.chdir('..')

                # Frontend tests
                os.chdir('frontend')
                subprocess.run(['npm', 'test'], check=True)
                os.chdir('..')
            return True
        except Exception as e:
            self.logger.error(f"Lỗi khi chạy tests: {str(e)}")
            return False

    def install(self):
        """Chạy toàn bộ quá trình cài đặt"""
        print("\n=== BẮT ĐẦU CÀI ĐẶT DỰ ÁN ===\n")
        
        steps = [
            (self.check_system_requirements, "Kiểm tra yêu cầu hệ thống"),
            (self.setup_virtual_environment, "Thiết lập môi trường ảo"),
            (self.install_backend_dependencies, "Cài đặt Backend dependencies"),
            (self.install_frontend_dependencies, "Cài đặt Frontend dependencies"),
            (self.setup_database, "Thiết lập Database"),
            (self.create_env_files, "Tạo file .env"),
            (self.setup_docker, "Thiết lập Docker"),
            (self.setup_monitoring, "Thiết lập Monitoring"),
            (self.run_tests, "Chạy Tests")
        ]

        for step_func, step_name in steps:
            print(f"\n>> Đang thực hiện: {step_name}...")
            if not step_func():
                print(f"\n✗ Lỗi khi {step_name.lower()}!")
                if not self.ask_user("Bạn có muốn tiếp tục không?"):
                    print("Đã dừng quá trình cài đặt!")
                    return
            print(f"✓ Hoàn thành: {step_name}")

        print("\n=== CÀI ĐẶT HOÀN TẤT ===")
        print("\nĐể chạy ứng dụng:")
        print("1. Backend: cd backend && uvicorn app.main:app --reload")
        print("2. Frontend: cd frontend && npm run dev")
        print("3. Docker: docker-compose up")

if __name__ == "__main__":
    installer = ProjectInstaller()
    installer.install() 