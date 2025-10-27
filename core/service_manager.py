import subprocess
import time
import psutil
from typing import Optional, Tuple
import os
import ctypes


class ServiceManager:
    """Менеджер для управления службами Windows с альтернативными методами"""

    @staticmethod
    def can_manage_services() -> bool:
        """Проверка возможности управления службами"""
        try:
            # Проверяем административные права через Windows API, без запуска команд в CMD
            # Если функция возвращает True, текущий пользователь имеет права администратора
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            # В случае ошибки считаем, что прав нет
            return False

    @staticmethod
    def get_service_status(service_name: str) -> Tuple[bool, Optional[str]]:
        """Получение статуса службы"""
        try:
            # Пробуем через sc query (работает без админских прав для чтения)
            result = subprocess.run(
                ["sc", "query", service_name],
                capture_output=True,
                text=True,
                encoding='cp866',
                timeout=10
            )

            if result.returncode == 0:
                if "RUNNING" in result.stdout:
                    return True, "Запущена"
                elif "STOPPED" in result.stdout:
                    return False, "Остановлена"
                else:
                    return False, "Неизвестный статус"
            else:
                return False, "Служба не найдена"

        except subprocess.TimeoutExpired:
            return False, "Таймаут запроса"
        except Exception as e:
            return False, f"Ошибка: {str(e)}"

    @staticmethod
    def start_service(service_name: str) -> Tuple[bool, str]:
        """Запуск службы с проверкой прав"""
        try:
            # Пробуем через net start
            result = subprocess.run(
                ["net", "start", service_name],
                capture_output=True,
                text=True,
                encoding='cp866',
                shell=True,
                timeout=30
            )

            if result.returncode == 0:
                return True, "Служба успешно запущена"
            elif "отказано в доступе" in result.stderr.lower() or "access is denied" in result.stderr.lower():
                return False, "Недостаточно прав для запуска службы. Запустите приложение от имени администратора."
            else:
                return False, f"Ошибка запуска: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, "Таймаут запуска службы"
        except Exception as e:
            return False, f"Исключение при запуске: {str(e)}"

    @staticmethod
    def stop_service(service_name: str) -> Tuple[bool, str]:
        """Остановка службы с проверкой прав"""
        try:
            result = subprocess.run(
                ["net", "stop", service_name],
                capture_output=True,
                text=True,
                encoding='cp866',
                shell=True,
                timeout=30
            )

            if result.returncode == 0:
                return True, "Служба успешно остановлена"
            elif "отказано в доступе" in result.stderr.lower() or "access is denied" in result.stderr.lower():
                return False, "Недостаточно прав для остановки службы. Запустите приложение от имени администратора."
            else:
                return False, f"Ошибка остановки: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, "Таймаут остановки службы"
        except Exception as e:
            return False, f"Исключение при остановке: {str(e)}"

    @staticmethod
    def restart_service(service_name: str) -> Tuple[bool, str]:
        """Перезапуск службы"""
        success_stop, message_stop = ServiceManager.stop_service(service_name)
        if success_stop:
            time.sleep(2)
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
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except:
            return False