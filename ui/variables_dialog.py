from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QHeaderView,
                             QMessageBox, QLineEdit, QLabel, QFormLayout,
                             QDialogButtonBox, QGroupBox, QWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.variable_manager import VariableManager, Variable


class VariablesDialog(QDialog):
    def __init__(self, variable_manager: VariableManager, parent=None):
        super().__init__(parent)
        self.variable_manager = variable_manager
        self.setWindowTitle("Управление переменными")
        self.setMinimumSize(600, 400)
        self.init_ui()
        self.load_variables()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Форма добавления переменной
        form_group = QGroupBox("Добавить/Изменить переменную")
        form_layout = QFormLayout(form_group)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Например: cluster_uid, ras_service")
        self.value_edit = QLineEdit()
        self.value_edit.setPlaceholderText("Значение переменной")
        self.comment_edit = QLineEdit()
        self.comment_edit.setPlaceholderText("Комментарий (необязательно)")

        form_layout.addRow("Имя переменной*:", self.name_edit)
        form_layout.addRow("Значение*:", self.value_edit)
        form_layout.addRow("Комментарий:", self.comment_edit)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Добавить")
        update_button = QPushButton("Обновить")
        clear_button = QPushButton("Очистить")

        add_button.clicked.connect(self.add_variable)
        update_button.clicked.connect(self.update_variable)
        clear_button.clicked.connect(self.clear_form)

        button_layout.addWidget(add_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(clear_button)
        button_layout.addStretch()

        form_layout.addRow("", button_layout)
        layout.addWidget(form_group)

        # Таблица переменных
        table_group = QGroupBox("Существующие переменные")
        table_layout = QVBoxLayout(table_group)

        self.table = QTableWidget(0, 4)  # Явно указываем 0 строк и 4 колонки
        self.table.setHorizontalHeaderLabels(["Имя", "Значение", "Комментарий", "Действия"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        table_layout.addWidget(self.table)
        layout.addWidget(table_group)

        # Кнопки закрытия
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def load_variables(self):
        """Безопасная загрузка переменных в таблицу"""
        try:
            variables = self.variable_manager.get_all_variables()
            self.table.setRowCount(len(variables))

            for row, variable in enumerate(variables):
                # Имя переменной
                name_item = QTableWidgetItem(variable.name)
                self.table.setItem(row, 0, name_item)

                # Значение (скрываем пароли)
                value_text = variable.value
                if any(keyword in variable.name.lower() for keyword in ['pwd', 'password', 'pass']):
                    value_text = "••••••••"
                value_item = QTableWidgetItem(value_text)
                self.table.setItem(row, 1, value_item)

                # Комментарий
                comment_item = QTableWidgetItem(variable.comment)
                self.table.setItem(row, 2, comment_item)

                # Кнопки действий
                action_widget = self.create_action_buttons(row)
                self.table.setCellWidget(row, 3, action_widget)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки переменных: {str(e)}")

    def create_action_buttons(self, row):
        """Создание кнопок действий для строки таблицы"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)

        edit_btn = QPushButton("Изменить")
        delete_btn = QPushButton("Удалить")
        use_btn = QPushButton("Использовать")

        # Сохраняем row в свойствах кнопок
        edit_btn.setProperty("row_index", row)
        delete_btn.setProperty("row_index", row)
        use_btn.setProperty("row_index", row)

        edit_btn.clicked.connect(self.edit_variable)
        delete_btn.clicked.connect(self.delete_variable)
        use_btn.clicked.connect(self.use_variable)

        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
        layout.addWidget(use_btn)

        return widget

    def add_variable(self):
        """Добавление новой переменной"""
        try:
            name = self.name_edit.text().strip()
            value = self.value_edit.text().strip()
            comment = self.comment_edit.text().strip()

            if not name or not value:
                QMessageBox.warning(self, "Ошибка", "Заполните имя и значение переменной")
                return

            is_valid, message = self.variable_manager.validate_variable_name(name)
            if not is_valid:
                QMessageBox.warning(self, "Ошибка", message)
                return

            self.variable_manager.set_variable(name, value, comment)
            self.load_variables()
            self.clear_form()
            QMessageBox.information(self, "Успех", f"Переменная '{name}' добавлена")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка добавления переменной: {str(e)}")

    def edit_variable(self):
        """Редактирование переменной"""
        try:
            button = self.sender()
            row = button.property("row_index")
            name = self.table.item(row, 0).text()
            variable = self.variable_manager.get_variable_with_comment(name)

            if variable:
                self.name_edit.setText(variable.name)
                self.value_edit.setText(variable.value)
                self.comment_edit.setText(variable.comment)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка редактирования переменной: {str(e)}")

    def update_variable(self):
        """Обновление переменной"""
        try:
            name = self.name_edit.text().strip()
            value = self.value_edit.text().strip()
            comment = self.comment_edit.text().strip()

            if not name or not value:
                QMessageBox.warning(self, "Ошибка", "Заполните имя и значение переменной")
                return

            self.variable_manager.set_variable(name, value, comment)
            self.load_variables()
            self.clear_form()
            QMessageBox.information(self, "Успех", f"Переменная '{name}' обновлена")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка обновления переменной: {str(e)}")

    def delete_variable(self):
        """Удаление переменной"""
        try:
            button = self.sender()
            row = button.property("row_index")
            name = self.table.item(row, 0).text()

            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Удалить переменную '{name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.variable_manager.remove_variable(name)
                self.load_variables()
                QMessageBox.information(self, "Успех", f"Переменная '{name}' удалена")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка удаления переменной: {str(e)}")

    def use_variable(self):
        """Использование переменной"""
        try:
            button = self.sender()
            row = button.property("row_index")
            name = self.table.item(row, 0).text()

            template = f"$({name})"
            QMessageBox.information(
                self,
                "Шаблон переменной",
                f"Шаблон для использования:\n\n{template}\n\nСкопируйте его в нужное поле."
            )

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка использования переменной: {str(e)}")

    def clear_form(self):
        """Очистка формы"""
        self.name_edit.clear()
        self.value_edit.clear()
        self.comment_edit.clear()