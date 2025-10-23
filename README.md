# rac_admin_gui
Админ-панель всех комбинаций RAC-команд

## Структура
```
rac_admin_gui/
├── main.py                 # Главный запускаемый файл
├── core/
│   ├── init.py
│   ├── rac_commands.py    # Все определения команд RAC
│   ├── command_executor.py # Исполнитель команд
│   └── logger.py          # Система логирования
├── ui/
│   ├── init.py
│   ├── main_window.py     # Главное окно
│   ├── command_dialogs.py # Диалоги команд
│   └── widgets.py         # Кастомные виджеты
└── config/
    └── init.py
```
