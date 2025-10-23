import subprocess
import os
from typing import Tuple, List
from .logger import RACLogger
from .variable_manager import VariableManager


class RACCommandExecutor:
    def __init__(self, rac_path: str, logger: RACLogger, variable_manager: VariableManager):
        self.rac_path = rac_path
        self.logger = logger
        self.variable_manager = variable_manager

    def execute_command(self, args: List[str], host: str = "localhost", port: int = 1545) -> Tuple[bool, str]:
        """Выполнение RAC команды с подстановкой переменных и правильной обработкой кавычек"""
        try:
            # Сначала строим аргументы с подстановкой переменных
            substituted_args = []
            for arg in args:
                # Подставляем переменные
                substituted_arg = self.variable_manager.substitute_variables(arg)
                substituted_args.append(substituted_arg)

            full_command = [self.rac_path] + substituted_args + [f"{host}:{port}"]
            command_str = " ".join(full_command)

            self.logger.log_command(command_str, "RAC_EXECUTOR")

            # Для выполнения используем исходные substituted_args (без shell=True)
            # subprocess сам правильно обработает аргументы
            result = subprocess.run(
                [self.rac_path] + substituted_args + [f"{host}:{port}"],
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

        return args