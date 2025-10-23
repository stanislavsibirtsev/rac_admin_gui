from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                            QWidget, QFormLayout, QLineEdit, QComboBox, 
                            QCheckBox, QPushButton, QTextEdit, QGroupBox,
                            QMessageBox, QScrollArea, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.rac_commands import RacCommand, CommandParam, ParamType
from core.command_executor import RACCommandExecutor
from core.logger import RACLogger

class CommandDialog(QDialog):
    command_executed = pyqtSignal(bool, str, str)  # success, command, output
    
    def init(self, mode: str, commands: list, executor: RACCommandExecutor, 
                 logger: RACLogger, parent=None):
        super().init(parent)
        self.mode = mode
        self.commands = commands
        self.executor = executor
        self.logger = logger
        
        self.setWindowTitle(f"RAC {mode} - Команды администрирования")
        self.setMinimumSize(800, 600)
        self.setModal(False)  # Не блокирующее окно
        
        self.init_ui()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout(self)
        
        # Вкладки для команд
        self.tab_widget = QTabWidget()
        
        for command in self.commands:
            tab = self.create_command_tab(command)
            self.tab_widget.addTab(tab, command.command)
        
        layout.addWidget(self.tab_widget)
    
    def create_command_tab(self, command: RacCommand) -> QWidget:
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
        self.param_widgets = {}
        
        for param in command.parameters:
            widget = self.create_param_widget(param)
            self.param_widgets[param.name] = widget
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
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMaximumHeight(100)
        self.preview_text.setFont(QFont("Courier New", 9))
        preview_layout.addWidget(self.preview_text)
        
        layout.addWidget(preview_group)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        preview_button = QPushButton("Обновить предпросмотр")
        execute_button = QPushButton("Выполнить команду")
        
        preview_button.clicked.connect(lambda: self.update_command_preview(command))
        execute_button.clicked.connect(lambda: self.execute_command(command))
        
        button_layout.addWidget(preview_button)
        button_layout.addWidget(execute_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Первоначальное обновление предпросмотра
        self.update_command_preview(command)
        return tab
    
    def create_param_widget(self, param: CommandParam):
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
        
        # Сохраняем тип параметра в свойстве виджета
        widget.setProperty("param_type", param.param_type)
        
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
        current_tab = self.tab_widget.currentWidget()
        if current_tab:
            # Находим команду для текущей вкладки
            tab_index = self.tab_widget.currentIndex()
            if tab_index < len(self.commands):
                command = self.commands[tab_index]
                self.update_command_preview(command)
    
    def update_command_preview(self, command: RacCommand):
        """Обновление предпросмотра команды"""
        params = self.get_current_parameters(command)
        args = self.executor.build_command_args(self.mode, command.command, params)
        command_str = "rac " + " ".join(args)
        self.preview_text.setPlainText(command_str)
    
    def get_current_parameters(self, command: RacCommand) -> dict:
        """Получение текущих значений параметров"""
        params = {}
        
        for param in command.parameters:
            widget = self.param_widgets.get(param.name)
            if widget:
                if param.param_type == ParamType.BOOLEAN:
                    params[param.name] = widget.isChecked()
                elif param.param_type == ParamType.ENUM:
                    value = widget.currentText()
                    if value:
                        params[param.name] = value
                else:
                    value = widget.text().strip()
                    if value:
                        params[param.name] = value
        
        return params
    
    def execute_command(self, command: RacCommand):
        """Выполнение команды"""
        params = self.get_current_parameters(command)
        
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
