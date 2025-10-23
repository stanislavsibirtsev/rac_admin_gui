import subprocess
import time
import psutil
from typing import Optional, Tuple


class ServiceManager:
    """Менеджер для управления службами Windows"""

    @staticmethod
    def get_service_status(service_name: str) -> Tuple[bool, Optional[str]]:
        """Получение статуса службы"""
        try:
            result = subprocess.run(
                ["sc", "query", service_name],
                capture_output=True,
                text=True,
                encoding='cp866'
            )

            if "RUNNING" in result.stdout:
                return True, "Запущена"
            elif "STOPPED" in result.stdout:
                return False, "Остановлена"
            else:
                return False, "Неизвестный статус"

        except subprocess.CalledProcessError:
            return False, "Служба не найдена"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"

    @staticmethod
    def start_service(service_name: str) -> Tuple[bool, str]:
        """Запуск службы"""
        try:
            result = subprocess.run(
                ["net", "start", service_name],
                capture_output=True,
                text=True,
                encoding='cp866',
                shell=True
            )

            if result.returncode == 0:
                return True, "Служба успешно запущена"
            else:
                return False, f"Ошибка запуска: {result.stderr}"

        except Exception as e:
            return False, f"Исключение при запуске: {str(e)}"

    @staticmethod
    def stop_service(service_name: str) -> Tuple[bool, str]:
        """Остановка службы"""
        try:
            result = subprocess.run(
                ["net", "stop", service_name],
                capture_output=True,
                text=True,
                encoding='cp866',
                shell=True
            )

            if result.returncode == 0:
                return True, "Служба успешно остановлена"
            else:
                return False, f"Ошибка остановки: {result.stderr}"

        except Exception as e:
            return False, f"Исключение при остановке: {str(e)}"

    @staticmethod
    def restart_service(service_name: str) -> Tuple[bool, str]:
        """Перезапуск службы"""
        success_stop, message_stop = ServiceManager.stop_service(service_name)
        if success_stop:
            time.sleep(2)  # Пауза между остановкой и запуском
            success_start, message_start = ServiceManager.start_service(service_name)
            return success_start, f"Остановка: {message_stop}\nЗапуск: {message_start}"
        else:
            return False, f"Ошибка перезапуска: {message_stop}"

    @staticmethod
    def is_service_exists(service_name: str) -> bool:
        """Проверка существования службы"""
        try:
            result = subprocess.run(
                ["sc", "query", service_name],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False