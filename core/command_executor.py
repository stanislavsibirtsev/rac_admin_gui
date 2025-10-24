import subprocess
import os
from typing import Tuple, List
from .logger import RACLogger
from .variable_manager import VariableManager


class RACCommandExecutor:
    def __init__(self, logger: RACLogger, variable_manager: VariableManager):
        self.logger = logger
        self.variable_manager = variable_manager

    def get_rac_path(self) -> str:
        """Получение пути к RAC из переменных"""
        rac_path = self.variable_manager.get_variable("rac_path")
        if not rac_path:
            rac_path = "rac.exe"
            self.variable_manager.set_variable("rac_path", rac_path, "Путь к утилите RAC", reserved=True)

        return rac_path

    def execute_command(self, args: List[str]) -> Tuple[bool, str]:
        """Выполнение RAC команды с подстановкой переменных"""
        try:
            # Получаем актуальный путь к RAC
            rac_path = self.get_rac_path()

            # Проверяем существование файла RAC
            if not os.path.exists(rac_path):
                return False, f"Файл RAC не найден: {rac_path}. Проверьте путь в настройках."

            # Подставляем переменные в аргументы
            substituted_args = []
            for arg in args:
                substituted_arg = self.variable_manager.substitute_variables(arg)
                substituted_args.append(substituted_arg)

            # Формируем полную команду
            full_command = [rac_path] + substituted_args
            command_str = " ".join(full_command)

            self.logger.log_command(command_str, "RAC_EXECUTOR")

            # Выполняем команду
            result = subprocess.run(
                full_command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                check=True,
                timeout=30
            )
            return True, result.stdout

        except subprocess.CalledProcessError as e:
            error_msg = f"Ошибка выполнения команды: {e.stderr}"
            self.logger.log_error(error_msg, "RAC_EXECUTOR")
            return False, error_msg
        except subprocess.TimeoutExpired:
            error_msg = "Таймаут выполнения команды"
            self.logger.log_error(error_msg, "RAC_EXECUTOR")
            return False, error_msg
        except FileNotFoundError:
            error_msg = f"Файл RAC не найден: {self.get_rac_path()}. Проверьте путь в настройках."
            self.logger.log_error(error_msg, "RAC_EXECUTOR")
            return False, error_msg
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {str(e)}"
            self.logger.log_error(error_msg, "RAC_EXECUTOR")
            return False, error_msg

    def build_command_args(self, mode: str, command: str, parameters: dict) -> List[str]:
        """Построение аргументов команды из параметров с учетом переменных"""
        args = [mode]

        # Добавляем подкоманды если есть
        if " " in command:
            sub_commands = command.split(" ")
            args.extend(sub_commands)
        else:
            args.append(command)

        # Добавляем параметры
        for key, value in parameters.items():
            if value is not None and value != "":
                if isinstance(value, bool) and value:
                    args.append(f"--{key}")
                elif not isinstance(value, bool):
                    # Подставляем переменные в значение
                    substituted_value = self.variable_manager.substitute_variables(str(value))

                    # Если значение содержит пробелы и не в кавычках, обрамляем в кавычки
                    final_value = substituted_value
                    if ' ' in substituted_value and not (
                            substituted_value.startswith('"') and substituted_value.endswith('"')):
                        final_value = f'"{substituted_value}"'

                    args.append(f"--{key}={final_value}")

        # Особый случай: host и port добавляются как отдельный аргумент в конце
        host = parameters.get('host', '')
        port = parameters.get('port', '')

        if host and port:
            args.append(f"{host}:{port}")
        elif host:
            args.append(host)
        elif port:
            args.append(f"localhost:{port}")
        else:
            # Если не указаны, используем значения по умолчанию из переменных
            default_host = self.variable_manager.get_variable("default_host") or "localhost"
            default_port = self.variable_manager.get_variable("default_port") or "1545"
            args.append(f"{default_host}:{default_port}")

        return args

    def test_rac_connection(self) -> Tuple[bool, str]:
        """Тестирование подключения к RAC"""
        try:
            rac_path = self.get_rac_path()

            if not os.path.exists(rac_path):
                return False, f"Файл RAC не найден: {rac_path}"

            result = subprocess.run(
                [rac_path, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return True, f"RAC подключен успешно: {result.stdout.strip()}"
            else:
                return False, f"Ошибка выполнения RAC: {result.stderr}"

        except Exception as e:
            return False, f"Ошибка тестирования RAC: {str(e)}"