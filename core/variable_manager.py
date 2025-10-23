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


class VariableManager:
    """Менеджер для работы с переменными"""

    def __init__(self, config_file: str = "config/variables.json"):
        self.config_file = config_file
        self.variables: Dict[str, Variable] = {}
        self.load_variables()

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

    def set_variable(self, name: str, value: str, comment: str = ""):
        """Установка переменной"""
        self.variables[name] = Variable(name=name, value=value, comment=comment)
        self.save_variables()

    def get_variable(self, name: str) -> Optional[str]:
        """Получение значения переменной"""
        var = self.variables.get(name)
        return var.value if var else None

    def get_variable_with_comment(self, name: str) -> Optional[Variable]:
        """Получение переменной с комментарием"""
        return self.variables.get(name)

    def remove_variable(self, name: str):
        """Удаление переменной"""
        if name in self.variables:
            del self.variables[name]
            self.save_variables()

    def get_all_variables(self) -> List[Variable]:
        """Получение всех переменных"""
        return list(self.variables.values())

    def substitute_variables(self, text: str) -> str:
        """Подстановка переменных в текст используя синтаксис $(variable_name)"""
        if not text:
            return text

        def replace_match(match):
            var_name = match.group(1)
            return self.get_variable(var_name) or match.group(0)

        # Регулярное выражение для поиска $(variable_name)
        pattern = r'\$\(([^)]+)\)'
        return re.sub(pattern, replace_match, text)

    def validate_variable_name(self, name: str) -> Tuple[bool, str]:
        """Валидация имени переменной"""
        if not name:
            return False, "Имя переменной не может быть пустым"
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
            return False, "Имя переменной может содержать только буквы, цифры и подчеркивания"
        return True, ""