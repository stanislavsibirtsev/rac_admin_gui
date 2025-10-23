import logging
import os
import atexit
from datetime import datetime
from typing import Optional


class SafeLogHandler(logging.Handler):
    """Безопасный обработчик логов, который не ломает shutdown"""

    def __init__(self, log_file):
        super().__init__()
        self.log_file = log_file
        self.setFormatter(logging.Formatter('[%(asctime)s] [%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

    def emit(self, record):
        try:
            msg = self.format(record)
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(msg + '\n')
        except Exception:
            pass  # Игнорируем ошибки при закрытии


class RACLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self._setup_logging()

    def _setup_logging(self):
        """Настройка системы логирования без конфликтов с PyQt"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        log_file = os.path.join(self.log_dir, f"rac_admin_{datetime.now().strftime('%Y%m%d')}.log")

        # Создаем безопасный файловый обработчик
        file_handler = SafeLogHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Создаем консольный обработчик
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('[%(asctime)s] [%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        console_handler.setFormatter(console_formatter)

        # Настраиваем корневой логгер
        self.logger = logging.getLogger('RACAdmin')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Явно отключаем atexit для наших обработчиков
        file_handler.emit = lambda record: None
        console_handler.emit = lambda record: None

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