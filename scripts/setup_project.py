import subprocess
import os
import sys
from typing import List

class ProjectSetup:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    def setup_backend(self):
        """Setup backend environment"""
        os.chdir(os.path.join(self.root_dir, 'backend'))
        
        commands = [
            'python -m venv venv',
            'source venv/bin/activate' if os.name != 'nt' else r'.\venv\Scripts\activate',
            'pip install -r requirements.txt',
            'cp .env.example .env',
            'python scripts/init_db.py',
            'alembic upgrade head',
            'python scripts/seed_data.py'
        ]
        
        self._run_commands(commands)
        
    def setup_frontend(self):
        """Setup frontend environment"""
        os.chdir(os.path.join(self.root_dir, 'frontend'))
        
        commands = [
            'yarn install',
            'cp .env.example .env.local'
        ]
        
        self._run_commands(commands)
        
    def setup_monitoring(self):
        """Setup monitoring stack"""
        commands = [
            'docker-compose -f docker-compose.monitoring.yml up -d',
            './scripts/import_dashboards.sh'
        ]
        
        self._run_commands(commands)
        
    def _run_commands(self, commands: List[str]):
        """Run shell commands"""
        for cmd in commands:
            try:
                subprocess.run(cmd, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running command: {cmd}")
                print(f"Error: {str(e)}")
                sys.exit(1)

if __name__ == "__main__":
    setup = ProjectSetup()
    setup.setup_backend()
    setup.setup_frontend()
    setup.setup_monitoring() 