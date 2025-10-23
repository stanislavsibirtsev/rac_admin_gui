import json
import os
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class Variable:
    name: str
    value: str
    comment: str = ""
    reserved: bool = False  # Флаг зарезервированной переменной


class VariableManager:
    """Менеджер для работы с переменными с поддержкой зарезервированных переменных"""

    def __init__(self, config_file: str = "config/variables.json"):
        self.config_file = config_file
        self.variables: Dict[str, Variable] = {}
        self.load_variables()
        self.initialize_reserved_variables()

    def initialize_reserved_variables(self):
        """Инициализация зарезервированных переменных"""
        reserved_vars = {
            "rac_path": {
                "value": "rac.exe",
                "comment": "Путь к утилите RAC (rac.exe)",
                "reserved": True
            },
            "ras_service": {
                "value": "1C:Enterprise 8.3 Remote Server",
                "comment": "Имя службы RAS",
                "reserved": True
            },
            "default_host": {
                "value": "localhost",
                "comment": "Хост по умолчанию",
                "reserved": True
            },
            "default_port": {
                "value": "1545",
                "comment": "Порт по умолчанию",
                "reserved": True
            }
        }

        for name, config in reserved_vars.items():
            if name not in self.variables:
                self.variables[name] = Variable(
                    name=name,
                    value=config["value"],
                    comment=config["comment"],
                    reserved=config["reserved"]
                )

        self.save_variables()

    def load_variables(self):
        """Загрузка переменных из файла"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.variables = {
                        name: Variable(**var_data)
                        for name, var_data in data.items()
                    }
        except Exception as e:
            print(f"Ошибка загрузки переменных: {e}")
            self.variables = {}

    def save_variables(self):
        """Сохранение переменных в файл"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(
                    {name: asdict(var) for name, var in self.variables.items()},
                    f,
                    ensure_ascii=False,
                    indent=2
                )
        except Exception as e:
            print(f"Ошибка сохранения переменных: {e}")

    def set_variable(self, name: str, value: str, comment: str = "", reserved: bool = False):
        """Установка переменной"""
        # Для зарезервированных переменных обновляем только значение
        if name in self.variables and self.variables[name].reserved:
            self.variables[name].value = value
        else:
            self.variables[name] = Variable(
                name=name,
                value=value,
                comment=comment,
                reserved=reserved
            )
        self.save_variables()

    def get_variable(self, name: str) -> Optional[str]:
        """Получение значения переменной"""
        var = self.variables.get(name)
        return var.value if var else None

    def get_variable_with_comment(self, name: str) -> Optional[Variable]:
        """Получение переменной с комментарием"""
        return self.variables.get(name)

    def remove_variable(self, name: str):
        """Удаление переменной (нельзя удалять зарезервированные)"""
        var = self.variables.get(name)
        if var and not var.reserved:
            del self.variables[name]
            self.save_variables()
            return True
        return False

    def get_all_variables(self) -> List[Variable]:
        """Получение всех переменных"""
        return list(self.variables.values())

    def get_reserved_variables(self) -> List[Variable]:
        """Получение зарезервированных переменных"""
        return [var for var in self.variables.values() if var.reserved]

    def get_user_variables(self) -> List[Variable]:
        """Получение пользовательских переменных"""
        return [var for var in self.variables.values() if not var.reserved]

    def substitute_variables(self, text: str) -> str:
        """Подстановка переменных в текст используя синтаксис $(variable_name)
        Автоматически обрамляет в кавычки значения с пробелами"""
        if not text:
            return text

        def replace_match(match):
            var_name = match.group(1)
            value = self.get_variable(var_name)

            if value is None:
                return match.group(0)  # Оставляем как есть, если переменная не найдена

            # Если значение содержит пробелы, обрамляем в кавычки
            if ' ' in value and not (value.startswith('"') and value.endswith('"')):
                return f'"{value}"'
            else:
                return value

        # Регулярное выражение для поиска $(variable_name)
        pattern = r'\$\(([^)]+)\)'
        return re.sub(pattern, replace_match, text)

    def validate_variable_name(self, name: str) -> Tuple[bool, str]:
        """Валидация имени переменной"""
        if not name:
            return False, "Имя переменной не может быть пустым"
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
            return False, "Имя переменной может содержать только буквы, цифры и подчеркивания"

        # Проверяем, не является ли имя зарезервированным (если оно уже существует)
        existing_var = self.variables.get(name)
        if existing_var and existing_var.reserved:
            return False, f"Имя '{name}' зарезервировано системой"

        return True, ""