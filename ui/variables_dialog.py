from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QHeaderView,
                             QMessageBox, QLineEdit, QLabel, QFormLayout,
                             QDialogButtonBox, QGroupBox, QWidget, QApplication,
                             QTabWidget)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

from core.variable_manager import VariableManager, Variable


class VariablesDialog(QDialog):
    def __init__(self, variable_manager: VariableManager, parent=None):
        super().__init__(parent)
        self.variable_manager = variable_manager
        self.current_editing_name = None
        self.setWindowTitle("Управление переменными")
        self.setMinimumSize(700, 500)
        self.init_ui()
        self.load_variables()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Вкладки для разделения зарезервированных и пользовательских переменных
        self.tab_widget = QTabWidget()

        # Вкладка пользовательских переменных
        user_tab = QWidget()
        user_layout = QVBoxLayout(user_tab)
        user_layout.addWidget(self.create_user_variables_section())
        self.tab_widget.addTab(user_tab, "Пользовательские переменные")

        # Вкладка системных переменных
        system_tab = QWidget()
        system_layout = QVBoxLayout(system_tab)
        system_layout.addWidget(self.create_system_variables_section())
        self.tab_widget.addTab(system_tab, "Системные переменные")

        layout.addWidget(self.tab_widget)

        # Кнопки закрытия
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def create_user_variables_section(self):
        """Создание секции пользовательских переменных"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Форма добавления переменной
        form_group = QGroupBox("Добавить/Изменить пользовательскую переменную")
        form_layout = QFormLayout(form_group)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Например: cluster_uid, server_ip")
        self.name_edit.textChanged.connect(self.on_name_changed)

        self.value_edit = QLineEdit()
        self.value_edit.setPlaceholderText("Значение переменной")

        self.comment_edit = QLineEdit()
        self.comment_edit.setPlaceholderText("Комментарий (необязательно)")

        form_layout.addRow("Имя переменной*:", self.name_edit)
        form_layout.addRow("Значение*:", self.value_edit)
        form_layout.addRow("Комментарий:", self.comment_edit)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.update_button = QPushButton("Обновить")
        self.clear_button = QPushButton("Очистить")

        self.add_button.clicked.connect(self.add_variable)
        self.update_button.clicked.connect(self.update_variable)
        self.clear_button.clicked.connect(self.clear_form)

        self.update_button.setEnabled(False)

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.clear_button)
        button_layout.addStretch()

        form_layout.addRow("", button_layout)
        layout.addWidget(form_group)

        # Таблица пользовательских переменных
        table_group = QGroupBox("Пользовательские переменные")
        table_layout = QVBoxLayout(table_group)

        self.user_table = QTableWidget(0, 4)
        self.user_table.setHorizontalHeaderLabels(["Имя", "Значение", "Комментарий", "Действия"])
        self.user_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.user_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.user_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.user_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        table_layout.addWidget(self.user_table)
        layout.addWidget(table_group)

        return widget

    def create_system_variables_section(self):
        """Создание секции системных переменных"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Форма редактирования системных переменных
        form_group = QGroupBox("Редактирование системных переменных")
        form_layout = QFormLayout(form_group)

        self.sys_name_edit = QLineEdit()
        self.sys_name_edit.setReadOnly(True)
        self.sys_name_edit.setStyleSheet("background-color: #f0f0f0;")

        self.sys_value_edit = QLineEdit()
        self.sys_value_edit.setPlaceholderText("Значение системной переменной")

        self.sys_comment_edit = QLineEdit()
        self.sys_comment_edit.setReadOnly(True)
        self.sys_comment_edit.setStyleSheet("background-color: #f0f0f0;")

        form_layout.addRow("Имя переменной:", self.sys_name_edit)
        form_layout.addRow("Значение*:", self.sys_value_edit)
        form_layout.addRow("Назначение:", self.sys_comment_edit)

        button_layout = QHBoxLayout()
        self.sys_update_button = QPushButton("Обновить значение")
        self.sys_clear_button = QPushButton("Очистить")

        self.sys_update_button.clicked.connect(self.update_system_variable)
        self.sys_clear_button.clicked.connect(self.clear_system_form)

        button_layout.addWidget(self.sys_update_button)
        button_layout.addWidget(self.sys_clear_button)
        button_layout.addStretch()

        form_layout.addRow("", button_layout)
        layout.addWidget(form_group)

        # Таблица системных переменных
        table_group = QGroupBox("Системные переменные")
        table_layout = QVBoxLayout(table_group)

        self.system_table = QTableWidget(0, 4)
        self.system_table.setHorizontalHeaderLabels(["Имя", "Значение", "Назначение", "Действия"])
        self.system_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.system_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.system_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.system_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        # Подключаем обработчик клика по таблице системных переменных
        self.system_table.cellClicked.connect(self.on_system_cell_clicked)

        table_layout.addWidget(self.system_table)
        layout.addWidget(table_group)

        return widget

    def load_variables(self):
        """Загрузка переменных в таблицы"""
        self.load_user_variables()
        self.load_system_variables()

    def load_user_variables(self):
        """Загрузка пользовательских переменных в таблицу"""
        try:
            variables = self.variable_manager.get_user_variables()
            self.user_table.setRowCount(len(variables))

            for row, variable in enumerate(variables):
                # Имя переменной
                name_item = QTableWidgetItem(variable.name)
                self.user_table.setItem(row, 0, name_item)

                # Значение (скрываем пароли)
                value_text = variable.value
                if any(keyword in variable.name.lower() for keyword in ['pwd', 'password', 'pass']):
                    value_text = "••••••••"
                value_item = QTableWidgetItem(value_text)
                self.user_table.setItem(row, 1, value_item)

                # Комментарий
                comment_item = QTableWidgetItem(variable.comment)
                self.user_table.setItem(row, 2, comment_item)

                # Кнопки действий
                action_widget = self.create_user_action_buttons(row, variable.name)
                self.user_table.setCellWidget(row, 3, action_widget)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки пользовательских переменных: {str(e)}")

    def load_system_variables(self):
        """Загрузка системных переменных в таблицу"""
        try:
            variables = self.variable_manager.get_reserved_variables()
            self.system_table.setRowCount(len(variables))

            for row, variable in enumerate(variables):
                # Имя переменной
                name_item = QTableWidgetItem(variable.name)
                name_item.setBackground(QColor(240, 240, 240))
                self.system_table.setItem(row, 0, name_item)

                # Значение
                value_item = QTableWidgetItem(variable.value)
                self.system_table.setItem(row, 1, value_item)

                # Комментарий
                comment_item = QTableWidgetItem(variable.comment)
                comment_item.setBackground(QColor(240, 240, 240))
                self.system_table.setItem(row, 2, comment_item)

                # Кнопка использования
                use_widget = self.create_system_use_button(row, variable.name)
                self.system_table.setCellWidget(row, 3, use_widget)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки системных переменных: {str(e)}")

    def create_user_action_buttons(self, row, var_name):
        """Создание кнопок действий для пользовательских переменных"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)

        edit_btn = QPushButton("Изменить")
        delete_btn = QPushButton("Удалить")
        use_btn = QPushButton("Использовать")

        edit_btn.setProperty("row_index", row)
        delete_btn.setProperty("row_index", row)
        use_btn.setProperty("row_index", row)

        edit_btn.clicked.connect(lambda: self.edit_user_variable(row))
        delete_btn.clicked.connect(lambda: self.delete_user_variable(row))
        use_btn.clicked.connect(lambda: self.use_variable(var_name))

        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
        layout.addWidget(use_btn)

        return widget

    def create_system_use_button(self, row, var_name):
        """Создание кнопки использования для системных переменных"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)

        use_btn = QPushButton("Использовать")
        use_btn.setProperty("row_index", row)
        use_btn.clicked.connect(lambda: self.use_variable(var_name))

        layout.addWidget(use_btn)
        return widget

    def on_system_cell_clicked(self, row, column):
        """Обработчик клика по ячейке системной таблицы"""
        try:
            if column != 3:  # Не обрабатываем клик по кнопке "Использовать"
                name = self.system_table.item(row, 0).text()
                value = self.system_table.item(row, 1).text()
                comment = self.system_table.item(row, 2).text()

                self.sys_name_edit.setText(name)
                self.sys_value_edit.setText(value)
                self.sys_comment_edit.setText(comment)

        except Exception as e:
            print(f"Ошибка при выборе системной переменной: {e}")

    def on_name_changed(self):
        """Обработчик изменения имени переменной - проверка на существование"""
        name = self.name_edit.text().strip()

        if not name:
            self.add_button.setEnabled(False)
            self.update_button.setEnabled(False)
            return

        # Проверяем валидность имени
        is_valid, message = self.variable_manager.validate_variable_name(name)
        if not is_valid:
            self.add_button.setEnabled(False)
            self.update_button.setEnabled(False)
            return

        # Проверяем, существует ли уже переменная с таким именем
        existing_var = self.variable_manager.get_variable_with_comment(name)

        if existing_var:
            if existing_var.reserved:
                # Зарезервированная переменная - можно только обновить значение
                self.add_button.setEnabled(False)
                self.update_button.setEnabled(True)
            else:
                # Пользовательская переменная - можно обновить
                self.add_button.setEnabled(False)
                self.update_button.setEnabled(True)
        else:
            # Новая переменная - можно добавить
            self.add_button.setEnabled(True)
            self.update_button.setEnabled(False)

    def add_variable(self):
        """Добавление новой пользовательской переменной"""
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

            # Проверяем, не существует ли уже переменная
            if self.variable_manager.get_variable(name):
                QMessageBox.warning(self, "Ошибка", f"Переменная '{name}' уже существует")
                return

            self.variable_manager.set_variable(name, value, comment)
            self.load_variables()
            self.clear_form()
            QMessageBox.information(self, "Успех", f"Переменная '{name}' добавлена")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка добавления переменной: {str(e)}")

    def edit_user_variable(self, row):
        """Редактирование пользовательской переменной"""
        try:
            name = self.user_table.item(row, 0).text()
            variable = self.variable_manager.get_variable_with_comment(name)

            if variable and not variable.reserved:
                self.current_editing_name = name
                self.name_edit.setText(variable.name)
                self.value_edit.setText(variable.value)
                self.comment_edit.setText(variable.comment)

                # Активируем режим обновления
                self.add_button.setEnabled(False)
                self.update_button.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка редактирования переменной: {str(e)}")

    def update_variable(self):
        """Обновление пользовательской переменной"""
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

    def delete_user_variable(self, row):
        """Удаление пользовательской переменной"""
        try:
            name = self.user_table.item(row, 0).text()

            reply = QMessageBox.question(
                self,
                "Подтверждение удаления",
                f"Удалить переменную '{name}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                if self.variable_manager.remove_variable(name):
                    self.load_variables()
                    self.clear_form()
                    QMessageBox.information(self, "Успех", f"Переменная '{name}' удалена")
                else:
                    QMessageBox.warning(self, "Ошибка", "Не удалось удалить переменную")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка удаления переменной: {str(e)}")

    def update_system_variable(self):
        """Обновление системной переменной"""
        try:
            name = self.sys_name_edit.text().strip()
            value = self.sys_value_edit.text().strip()

            if not name or not value:
                QMessageBox.warning(self, "Ошибка", "Заполните значение переменной")
                return

            # Для системных переменных можно менять только значение
            existing_var = self.variable_manager.get_variable_with_comment(name)
            if existing_var and existing_var.reserved:
                self.variable_manager.set_variable(name, value, existing_var.comment, reserved=True)
                self.load_variables()
                self.clear_system_form()
                QMessageBox.information(self, "Успех", f"Системная переменная '{name}' обновлена")
            else:
                QMessageBox.warning(self, "Ошибка", "Нельзя изменить несистемную переменную в этом разделе")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка обновления системной переменной: {str(e)}")

    def use_variable(self, var_name):
        """Использование переменной - с возможностью копирования"""
        try:
            template = f"$({var_name})"

            # Создаем диалог с полем для копирования
            copy_dialog = QDialog(self)
            copy_dialog.setWindowTitle("Копирование шаблона переменной")
            copy_dialog.setMinimumWidth(400)

            layout = QVBoxLayout(copy_dialog)

            # Инструкция
            instruction = QLabel(f"Шаблон для переменной '{var_name}':")
            layout.addWidget(instruction)

            # Поле с шаблоном (можно копировать)
            template_edit = QLineEdit(template)
            template_edit.selectAll()
            template_edit.setFont(QFont("Courier New", 10))
            layout.addWidget(template_edit)

            # Кнопки
            button_layout = QHBoxLayout()
            copy_button = QPushButton("📋 Копировать")
            close_button = QPushButton("Закрыть")

            copy_button.clicked.connect(lambda: self.copy_to_clipboard(template, copy_dialog))
            close_button.clicked.connect(copy_dialog.accept)

            button_layout.addWidget(copy_button)
            button_layout.addWidget(close_button)
            layout.addLayout(button_layout)

            # Фокусируемся на поле ввода для удобного копирования
            template_edit.setFocus()

            copy_dialog.exec()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка использования переменной: {str(e)}")

    def copy_to_clipboard(self, text: str, dialog: QDialog):
        """Копирование текста в буфер обмена"""
        try:
            import pyperclip
            pyperclip.copy(text)
            QMessageBox.information(dialog, "Успех", "Шаблон скопирован в буфер обмена!")
            dialog.accept()
        except ImportError:
            # Если pyperclip не установлен, используем QClipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            QMessageBox.information(dialog, "Успех", "Шаблон скопирован в буфер обмена!")
            dialog.accept()
        except Exception as e:
            QMessageBox.critical(dialog, "Ошибка", f"Не удалось скопировать: {str(e)}")

    def clear_form(self):
        """Очистка формы пользовательских переменных"""
        self.name_edit.clear()
        self.value_edit.clear()
        self.comment_edit.clear()
        self.current_editing_name = None
        self.add_button.setEnabled(False)
        self.update_button.setEnabled(False)

    def clear_system_form(self):
        """Очистка формы системных переменных"""
        self.sys_name_edit.clear()
        self.sys_value_edit.clear()
        self.sys_comment_edit.clear()