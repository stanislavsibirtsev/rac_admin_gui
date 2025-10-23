import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDir
from PyQt6.QtGui import QFont

from ui.main_window import MainWindow

def main():
    # Создание приложения
    app = QApplication(sys.argv)
    
    # Настройка шрифта для поддержки кириллицы
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Создание и отображение главного окна
    window = MainWindow()
    window.showMaximized()  # Открыть на весь экран
    
    # Запуск приложения
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
