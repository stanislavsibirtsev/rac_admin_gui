from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTextEdit, QGridLayout, QScrollArea,
                             QSizePolicy, QMessageBox, QTabWidget, QSplitter,
                             QGroupBox, QLabel, QLineEdit)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon
import sys
import os

from core.rac_commands import RACCommands
from core.logger import RACLogger
from core.command_executor import RACCommandExecutor
from core.service_manager import ServiceManager
from core.variable_manager import VariableManager
from ui.command_dialogs import CommandDialog
from ui.variables_dialog import VariablesDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.rac_commands = RACCommands.get_all_commands()
        self.logger = RACLogger()
        self.variable_manager = VariableManager()
        self.command_executor = RACCommandExecutor("rac.exe", self.logger, self.variable_manager)
        self.service_manager = ServiceManager()

        # Настройки по умолчанию
        self.ras_service_name = "1C:Enterprise 8.3 Remote Server"

        self.init_ui()
        self.setup_connections()
        self.start_service_monitor()

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

        # Панель управления службой
        service_panel = self.create_service_panel()
        layout.addWidget(service_panel)

        # Кнопка управления переменными
        vars_button = QPushButton("📊 Управление переменными")
        vars_button.setMinimumHeight(40)
        vars_button.clicked.connect(self.open_variables_dialog)
        layout.addWidget(vars_button)

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

    def create_service_panel(self) -> QWidget:
        """Создание панели управления службой RAS"""
        panel = QGroupBox("Управление службой RAS")
        layout = QVBoxLayout(panel)

        # Статус службы
        status_layout = QHBoxLayout()
        self.service_status_label = QLabel("Проверка...")
        self.service_status_indicator = QLabel("⚫")
        self.service_status_indicator.setFont(QFont("Arial", 16))

        status_layout.addWidget(self.service_status_indicator)
        status_layout.addWidget(self.service_status_label)
        status_layout.addStretch()

        # Поле для имени службы
        service_name_layout = QHBoxLayout()
        service_name_layout.addWidget(QLabel("Имя службы:"))
        self.service_name_edit = QLineEdit(self.ras_service_name)
        service_name_layout.addWidget(self.service_name_edit)

        # Кнопки управления
        buttons_layout = QHBoxLayout()
        self.start_service_btn = QPushButton("▶ Запуск")
        self.stop_service_btn = QPushButton("⏹ Остановка")
        self.restart_service_btn = QPushButton("🔄 Перезапуск")
        self.refresh_status_btn = QPushButton("🔄 Обновить")

        self.start_service_btn.clicked.connect(self.start_ras_service)
        self.stop_service_btn.clicked.connect(self.stop_ras_service)
        self.restart_service_btn.clicked.connect(self.restart_ras_service)
        self.refresh_status_btn.clicked.connect(self.check_service_status)

        buttons_layout.addWidget(self.start_service_btn)
        buttons_layout.addWidget(self.stop_service_btn)
        buttons_layout.addWidget(self.restart_service_btn)
        buttons_layout.addWidget(self.refresh_status_btn)

        layout.addLayout(service_name_layout)
        layout.addLayout(status_layout)
        layout.addLayout(buttons_layout)

        # Первоначальная проверка статуса
        self.check_service_status()

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
            "help": "📖 Справка",
            "agent": "🖥 Агент кластера",
            "cluster": "🏢 Кластер серверов",
            "manager": "👨‍💼 Менеджер кластера",
            "server": "⚙ Рабочий сервер",
            "process": "🔄 Рабочий процесс",
            "service": "🔧 Сервис менеджера",
            "infobase": "🗄 Информационная база",
            "connection": "🔗 Соединения",
            "session": "👥 Сеансы",
            "lock": "🔒 Блокировки",
            "rule": "📋 Требования назначения",
            "profile": "🛡 Профили безопасности",
            "counter": "📊 Счетчики ресурсов",
            "limit": "🚫 Ограничения ресурсов"
        }
        return names.get(mode, mode)

    def setup_connections(self):
        """Настройка соединений"""
        # Перенаправляем логи в текстовое поле
        import logging
        from PyQt6.QtCore import QObject, pyqtSignal

        class LogHandler(QObject, logging.Handler):
            log_signal = pyqtSignal(str)

            def __init__(self):
                super().__init__()
                logging.Handler.__init__(self)
                self.setFormatter(logging.Formatter('%(message)s'))

            def emit(self, record):
                msg = self.format(record)
                self.log_signal.emit(msg)

        self.log_handler = LogHandler()
        self.log_handler.log_signal.connect(self.log_text_append)
        self.logger.logger.addHandler(self.log_handler)

    def start_service_monitor(self):
        """Запуск мониторинга службы"""
        self.service_timer = QTimer()
        self.service_timer.timeout.connect(self.check_service_status)
        self.service_timer.start(5000)  # Проверка каждые 5 секунд

    def check_service_status(self):
        """Проверка статуса службы"""
        service_name = self.service_name_edit.text().strip() or self.ras_service_name
        is_running, status_message = self.service_manager.get_service_status(service_name)

        if is_running:
            self.service_status_indicator.setText("🟢")
            self.service_status_label.setText(f"Запущена: {service_name}")
            self.start_service_btn.setEnabled(False)
            self.stop_service_btn.setEnabled(True)
            self.restart_service_btn.setEnabled(True)
        else:
            self.service_status_indicator.setText("🔴")
            self.service_status_label.setText(f"Остановлена: {status_message}")
            self.start_service_btn.setEnabled(True)
            self.stop_service_btn.setEnabled(False)
            self.restart_service_btn.setEnabled(False)

    def start_ras_service(self):
        """Запуск службы RAS"""
        service_name = self.service_name_edit.text().strip() or self.ras_service_name
        success, message = self.service_manager.start_service(service_name)

        if success:
            self.logger.log_info(f"Служба {service_name} запущена: {message}", "SERVICE")
            QMessageBox.information(self, "Успех", f"Служба запущена:\n{message}")
        else:
            self.logger.log_error(f"Ошибка запуска службы {service_name}: {message}", "SERVICE")
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить службу:\n{message}")

        self.check_service_status()

    def stop_ras_service(self):
        """Остановка службы RAS"""
        service_name = self.service_name_edit.text().strip() or self.ras_service_name
        success, message = self.service_manager.stop_service(service_name)

        if success:
            self.logger.log_info(f"Служба {service_name} остановлена: {message}", "SERVICE")
            QMessageBox.information(self, "Успех", f"Служба остановлена:\n{message}")
        else:
            self.logger.log_error(f"Ошибка остановки службы {service_name}: {message}", "SERVICE")
            QMessageBox.critical(self, "Ошибка", f"Не удалось остановить службу:\n{message}")

        self.check_service_status()

    def restart_ras_service(self):
        """Перезапуск службы RAS"""
        service_name = self.service_name_edit.text().strip() or self.ras_service_name
        success, message = self.service_manager.restart_service(service_name)

        if success:
            self.logger.log_info(f"Служба {service_name} перезапущена: {message}", "SERVICE")
            QMessageBox.information(self, "Успех", f"Служба перезапущена:\n{message}")
        else:
            self.logger.log_error(f"Ошибка перезапуска службы {service_name}: {message}", "SERVICE")
            QMessageBox.critical(self, "Ошибка", f"Не удалось перезапустить службу:\n{message}")

        self.check_service_status()

    def open_variables_dialog(self):
        """Открытие диалога управления переменными"""
        dialog = VariablesDialog(self.variable_manager, self)
        dialog.exec()

    def on_mode_button_clicked(self):
        """Обработчик нажатия на кнопку режима"""
        button = self.sender()
        mode = button.property("mode")

        if mode in self.rac_commands:
            # Проверяем статус службы перед открытием диалога
            service_name = self.service_name_edit.text().strip() or self.ras_service_name
            is_running, _ = self.service_manager.get_service_status(service_name)

            if not is_running and mode != "help":
                reply = QMessageBox.question(
                    self,
                    "Служба не запущена",
                    f"Служба RAS не запущена. Команды {mode} могут не работать.\nПродолжить?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    return

            dialog = CommandDialog(mode, self.rac_commands[mode], self.command_executor, self.logger, self)
            dialog.command_executed.connect(self.on_command_executed)
            dialog.show()

    def on_command_executed(self, success: bool, command: str, output: str):
        """Обработчик выполнения команды"""
        if success:
            self.log_text_append(f"✅ Команда выполнена успешно: {command}")
            self.log_text_append(f"Вывод:\n{output}\n" + "=" * 80 + "\n")
        else:
            self.log_text_append(f"❌ Ошибка выполнения команды: {command}")
            self.log_text_append(f"Ошибка:\n{output}\n" + "=" * 80 + "\n")

    def log_text_append(self, text: str):
        """Добавление текста в лог"""
        self.log_text_edit.append(text)
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