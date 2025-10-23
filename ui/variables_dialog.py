from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QHeaderView,
                             QMessageBox, QLineEdit, QLabel, QFormLayout,
                             QDialogButtonBox, QComboBox)
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

        self.table = QTableWidget()
        self.table.setColumnCount(4)
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
        variables = self.variable_manager.get_all_variables()
        self.table.setRowCount(len(variables))

        for row, variable in enumerate(variables):
            self.table.setItem(row, 0, QTableWidgetItem(variable.name))

            # Значение (скрываем пароли)
            value_item = QTableWidgetItem(variable.value)
            if any(keyword in variable.name.lower() for keyword in ['pwd', 'password', 'pass']):
                value_item.setText("••••••••")
            self.table.setItem(row, 1, value_item)

            self.table.setItem(row, 2, QTableWidgetItem(variable.comment))

            # Кнопки действий
            action_layout = QHBoxLayout()
            action_widget = QWidget()

            edit_btn = QPushButton("Изменить")
            delete_btn = QPushButton("Удалить")
            use_btn = QPushButton("Использовать")

            edit_btn.clicked.connect(lambda checked, r=row: self.edit_variable(r))
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_variable(r))
            use_btn.clicked.connect(lambda checked, r=row: self.use_variable(r))

            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addWidget(use_btn)
            action_layout.setContentsMargins(0, 0, 0, 0)

            action_widget.setLayout(action_layout)
            self.table.setCellWidget(row, 3, action_widget)

    def add_variable(self):
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

    def edit_variable(self, row):
        name = self.table.item(row, 0).text()
        variable = self.variable_manager.get_variable_with_comment(name)

        if variable:
            self.name_edit.setText(variable.name)
            self.value_edit.setText(variable.value)
            self.comment_edit.setText(variable.comment)

    def update_variable(self):
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

    def delete_variable(self, row):
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

    def use_variable(self, row):
        name = self.table.item(row, 0).text()
        variable = self.variable_manager.get_variable_with_comment(name)

        if variable:
            # Вставляем шаблон переменной в буфер обмена
            import pyperclip
            template = f"$({name})"
            pyperclip.copy(template)
            QMessageBox.information(self, "Успех", f"Шаблон '{template}' скопирован в буфер обмена")

    def clear_form(self):
        self.name_edit.clear()
        self.value_edit.clear()
        self.comment_edit.clear()