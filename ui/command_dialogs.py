from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QWidget, QFormLayout, QLineEdit, QComboBox,
                             QCheckBox, QPushButton, QTextEdit, QGroupBox,
                             QMessageBox, QScrollArea, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.rac_commands import RacCommand, CommandParam, ParamType
from core.command_executor import RACCommandExecutor
from core.logger import RACLogger


class TabData:
    """Класс для хранения данных вкладки"""

    def __init__(self):
        self.param_widgets = {}
        self.preview_text = None
        self.command = None


class CommandDialog(QDialog):
    command_executed = pyqtSignal(bool, str, str)  # success, command, output

    def __init__(self, mode: str, commands: list, executor: RACCommandExecutor,
                 logger: RACLogger, parent=None):
        super().__init__(parent)
        self.mode = mode
        self.commands = commands
        self.executor = executor
        self.logger = logger

        # Список для хранения данных вкладок
        self.tabs_data = []

        self.setWindowTitle(f"RAC {mode} - Команды администрирования")
        self.setMinimumSize(800, 600)
        self.setModal(False)

        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout(self)

        # Вкладки для команд
        self.tab_widget = QTabWidget()

        for i, command in enumerate(self.commands):
            tab_data = TabData()
            tab_data.command = command
            self.tabs_data.append(tab_data)

            tab = self.create_command_tab(command, i)
            self.tab_widget.addTab(tab, command.command)

        layout.addWidget(self.tab_widget)

        # Подключаем сигнал переключения вкладок
        self.tab_widget.currentChanged.connect(self.on_tab_changed)

    def on_tab_changed(self, index):
        """Обработчик переключения вкладок"""
        if 0 <= index < len(self.tabs_data):
            self.update_command_preview(index)

    def create_command_tab(self, command: RacCommand, tab_index: int) -> QWidget:
        """Создание вкладки для команды"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Описание команды
        desc_label = QLabel(f"<b>Описание:</b> {command.description}")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

        # Scroll area для параметров
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QFormLayout(scroll_widget)

        # Поля для параметров
        tab_data = self.tabs_data[tab_index]

        for param in command.parameters:
            widget = self.create_param_widget(param, tab_index)
            tab_data.param_widgets[param.name] = widget
            label_text = f"{param.name}{'*' if param.required else ''}"
            scroll_layout.addRow(f"<b>{label_text}:</b>", widget)
            if param.description:
                help_label = QLabel(f"<i>{param.description}</i>")
                help_label.setWordWrap(True)
                scroll_layout.addRow("", help_label)

        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Группа предпросмотра команды
        preview_group = QGroupBox("Предпросмотр команды")
        preview_layout = QVBoxLayout(preview_group)

        preview_text = QTextEdit()
        preview_text.setReadOnly(True)
        preview_text.setMaximumHeight(100)
        preview_text.setFont(QFont("Courier New", 9))
        preview_layout.addWidget(preview_text)

        layout.addWidget(preview_group)

        # Кнопки
        button_layout = QHBoxLayout()

        preview_button = QPushButton("Обновить предпросмотр")
        execute_button = QPushButton("Выполнить команду")

        preview_button.clicked.connect(lambda: self.update_command_preview(tab_index))
        execute_button.clicked.connect(lambda: self.execute_command(tab_index))

        button_layout.addWidget(preview_button)
        button_layout.addWidget(execute_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        # Сохраняем ссылку на preview_text
        tab_data.preview_text = preview_text

        # Первоначальное обновление предпросмотра
        self.update_command_preview(tab_index)

        return tab

    def create_param_widget(self, param: CommandParam, tab_index: int):
        """Создание виджета для параметра"""
        if param.param_type == ParamType.BOOLEAN:
            widget = QCheckBox()
        elif param.param_type == ParamType.ENUM:
            widget = QComboBox()
            widget.addItem("")  # Пустой элемент
            for value in param.enum_values:
                widget.addItem(value)
        elif param.param_type == ParamType.PASSWORD:
            widget = QLineEdit()
            widget.setEchoMode(QLineEdit.EchoMode.Password)
        else:
            widget = QLineEdit()
            if param.default_value:
                widget.setText(str(param.default_value))

        # Сохраняем тип параметра и индекс вкладки в свойстве виджета
        widget.setProperty("param_type", param.param_type)
        widget.setProperty("tab_index", tab_index)

        # Подключаем обновление предпросмотра при изменении
        if hasattr(widget, 'textChanged'):
            widget.textChanged.connect(self.on_parameter_changed)
        elif hasattr(widget, 'stateChanged'):
            widget.stateChanged.connect(self.on_parameter_changed)
        elif hasattr(widget, 'currentTextChanged'):
            widget.currentTextChanged.connect(self.on_parameter_changed)

        return widget

    def on_parameter_changed(self):
        """Обработчик изменения параметра"""
        widget = self.sender()
        if widget:
            tab_index = widget.property("tab_index")
            if tab_index is not None and 0 <= tab_index < len(self.tabs_data):
                self.update_command_preview(tab_index)

    def update_command_preview(self, tab_index: int):
        """Обновление предпросмотра команды для указанной вкладки с подстановкой переменных"""
        if tab_index < 0 or tab_index >= len(self.tabs_data):
            return

        tab_data = self.tabs_data[tab_index]
        command = tab_data.command

        if not command or not tab_data.preview_text:
            return

        params = self.get_current_parameters(tab_index)
        args = self.executor.build_command_args(self.mode, command.command, params)

        # Формируем команду с подстановкой переменных
        command_str = "rac " + " ".join(args)

        # Подставляем переменные для отображения
        command_str_with_vars = self.executor.variable_manager.substitute_variables(command_str)

        # Форматируем вывод: показываем и исходную команду, и команду с подстановкой
        if command_str != command_str_with_vars:
            display_text = f"Исходная команда:\n{command_str}\n\nКоманда с подстановкой переменных:\n{command_str_with_vars}"
        else:
            display_text = command_str

        tab_data.preview_text.setPlainText(display_text)

    def get_current_parameters(self, tab_index: int) -> dict:
        """Получение текущих значений параметров для указанной вкладки"""
        if tab_index < 0 or tab_index >= len(self.tabs_data):
            return {}

        tab_data = self.tabs_data[tab_index]
        command = tab_data.command
        params = {}

        if not command:
            return params

        for param in command.parameters:
            widget = tab_data.param_widgets.get(param.name)
            if widget:
                if param.param_type == ParamType.BOOLEAN:
                    if widget.isChecked():
                        params[param.name] = True
                elif param.param_type == ParamType.ENUM:
                    value = widget.currentText()
                    if value:
                        params[param.name] = value
                else:
                    value = widget.text().strip()
                    if value:
                        params[param.name] = value

        return params

    def execute_command(self, tab_index: int):
        """Выполнение команды для указанной вкладки"""
        if tab_index < 0 or tab_index >= len(self.tabs_data):
            return

        tab_data = self.tabs_data[tab_index]
        command = tab_data.command

        if not command:
            return

        params = self.get_current_parameters(tab_index)

        # Проверка обязательных параметров
        missing_required = []
        for param in command.parameters:
            if param.required and param.name not in params:
                missing_required.append(param.name)

        if missing_required:
            QMessageBox.warning(
                self,
                "Не заполнены обязательные параметры",
                f"Заполните обязательные параметры: {', '.join(missing_required)}"
            )
            return

        # Подтверждение выполнения
        args = self.executor.build_command_args(self.mode, command.command, params)
        command_str = "rac " + " ".join(args)

        reply = QMessageBox.question(
            self,
            "Подтверждение выполнения",
            f"Выполнить команду:\n\n{command_str}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, output = self.executor.execute_command(args)
            self.command_executed.emit(success, command_str, output)

            if success:
                QMessageBox.information(self, "Успех", "Команда выполнена успешно")
            else:
                QMessageBox.critical(self, "Ошибка", f"Ошибка выполнения команды:\n{output}")