import logging
import os
from datetime import datetime
from typing import Optional

class RACLogger:
    def init(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self._setup_logging()
    
    def _setup_logging(self):
        """Настройка системы логирования"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        log_file = os.path.join(self.log_dir, f"rac_admin_{datetime.now().strftime('%Y%m%d')}.log")
        
        # Форматтер с временными метками
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Хендлер для файла
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        # Хендлер для консоли
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Настройка корневого логгера
        self.logger = logging.getLogger('RACAdmin')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def log_command(self, command: str, function: str = "SYSTEM"):
        """Логирование выполняемой команды"""
        self.logger.info(f"[{function}] Выполнение команды: {command}")
    
    def log_info(self, message: str, function: str = "SYSTEM"):
        """Логирование информационного сообщения"""
        self.logger.info(f"[{function}] {message}")
    
    def log_error(self, message: str, function: str = "SYSTEM"):
        """Логирование ошибки"""
        self.logger.error(f"[{function}] {message}")
    
    def log_warning(self, message: str, function: str = "SYSTEM"):
        """Логирование предупреждения"""
        self.logger.warning(f"[{function}] {message}")
