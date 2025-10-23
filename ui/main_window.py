from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QPushButton, QTextEdit, QGridLayout, QScrollArea,
                            QSizePolicy, QMessageBox, QTabWidget, QSplitter)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
import sys
import os

from core.rac_commands import RACCommands
from core.logger import RACLogger
from core.command_executor import RACCommandExecutor
from ui.command_dialogs import CommandDialog

class MainWindow(QMainWindow):
    def init(self):
        super().init()
        self.rac_commands = RACCommands.get_all_commands()
        self.logger = RACLogger()
        self.command_executor = RACCommandExecutor("rac.exe", self.logger)
        
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("RAC Admin GUI - Администрирование кластеров 1С")
        self.setMinimumSize(1920, 1080)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QHBoxLayout(central_widget)
        
        # Сплиттер для резиновой компоновки
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Левая панель с кнопками
        left_panel = self.create_buttons_panel()
        splitter.addWidget(left_panel)
        
        # Правая панель с логами
        right_panel = self.create_logs_panel()
        splitter.addWidget(right_panel)
        
        # Установка пропорций
        splitter.setSizes([600, 1300])
        
        main_layout.addWidget(splitter)
    
    def create_buttons_panel(self) -> QWidget:
        """Создание панели с кнопками команд"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Заголовок
        title_label = QTextEdit()
        title_label.setHtml("<h2>Режимы администрирования RAC</h2>")
        title_label.setReadOnly(True)
        title_label.setMaximumHeight(60)
        layout.addWidget(title_label)
        
        # Scroll area для кнопок
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)
        
        # Создание кнопок для каждого режима
        modes = list(self.rac_commands.keys())
        row, col = 0, 0
        max_cols = 2
        
        for mode in modes:
            button = QPushButton(self.get_mode_display_name(mode))
            button.setMinimumHeight(50)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            button.setProperty("mode", mode)
            button.clicked.connect(self.on_mode_button_clicked)
            
            scroll_layout.addWidget(button, row, col)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        return panel
    
    def create_logs_panel(self) -> QWidget:
        """Создание панели с логами"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Заголовок
        title_label = QTextEdit()
        title_label.setHtml("<h2>Журнал выполнения команд</h2>")
        title_label.setReadOnly(True)
        title_label.setMaximumHeight(40)
        layout.addWidget(title_label)
        
        # Текстовое поле для логов
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setFont(QFont("Courier New", 9))
        
        # Кнопки управления логами
        log_controls_layout = QHBoxLayout()
        clear_button = QPushButton("Очистить логи")
        save_button = QPushButton("Сохранить логи")
        
        clear_button.clicked.connect(self.clear_logs)
        save_button.clicked.connect(self.save_logs)
        
        log_controls_layout.addWidget(clear_button)
        log_controls_layout.addWidget(save_button)
        log_controls_layout.addStretch()
        
        layout.addLayout(log_controls_layout)
        layout.addWidget(self.log_text_edit)
        
        return panel
    
    def get_mode_display_name(self, mode: str) -> str:
        """Получение отображаемого имени для режима"""
        names = {
            "help": "Справка",
            "agent": "Агент кластера",
            "cluster": "Кластер серверов", 
            "manager": "Менеджер кластера",
            "server": "Рабочий сервер",
            "process": "Рабочий процесс",
            "service": "Сервис менеджера",
            "infobase": "Информационная база",
            "connection": "Соединения",
            "session": "Сеансы",
            "lock": "Блокировки", 
            "rule": "Требования назначения",
            "profile": "Профили безопасности",
            "counter": "Счетчики ресурсов",
            "limit": "Ограничения ресурсов"
        }
        return names.get(mode, mode)
    
    def setup_connections(self):
        """Настройка соединений"""
        # Перенаправляем логи в текстовое поле
        import logging
        logging.getLogger('RACAdmin').handlers[1].setFormatter(
            logging.Formatter('%(message)s')
        )
    
    def on_mode_button_clicked(self):
        """Обработчик нажатия на кнопку режима"""
        button = self.sender()
        mode = button.property("mode")
        
        if mode in self.rac_commands:
            dialog = CommandDialog(mode, self.rac_commands[mode], self.command_executor, self.logger, self)
            dialog.command_executed.connect(self.on_command_executed)
            dialog.show()
    
    def on_command_executed(self, success: bool, command: str, output: str):
        """Обработчик выполнения команды"""
        if success:
            self.log_text_append(f"✅ Команда выполнена успешно: {command}")
            self.log_text_append(f"Вывод:\n{output}\n" + "="*80 + "\n")
        else:
            self.log_text_append(f"❌ Ошибка выполнения команды: {command}")
            self.log_text_append(f"Ошибка:\n{output}\n" + "="*80 + "\n")
    
    def log_text_append(self, text: str):
        """Добавление текста в лог"""
        self.log_text_append(text)
        # Автопрокрутка к низу
        cursor = self.log_text_edit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.log_text_edit.setTextCursor(cursor)
    
    def clear_logs(self):
        """Очистка логов"""
        self.log_text_edit.clear()
    
    def save_logs(self):
        """Сохранение логов в файл"""
        # Реализация сохранения логов
        pass
