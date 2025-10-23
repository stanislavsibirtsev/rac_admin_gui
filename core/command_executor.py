import subprocess
import os
from typing import Tuple, List
from .logger import RACLogger

class RACCommandExecutor:
    def __init__(self, rac_path: str, logger: RACLogger):
        self.rac_path = rac_path
        self.logger = logger
    
    def execute_command(self, args: List[str], host: str = "localhost", port: int = 1545) -> Tuple[bool, str]:
        """Выполнение RAC команды"""
        full_command = [self.rac_path] + args + [f"{host}:{port}"]
        command_str = " ".join(full_command)
        
        self.logger.log_command(command_str, "RAC_EXECUTOR")
        
        try:
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
        except Exception as e:
            error_msg = f"Неожиданная ошибка: {str(e)}"
            self.logger.log_error(error_msg, "RAC_EXECUTOR")
            return False, error_msg
    
    def build_command_args(self, mode: str, command: str, parameters: dict) -> List[str]:
        """Построение аргументов команды из параметров"""
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
                    args.append(f"--{key}={value}")
        
        return args
