# rac_admin_gui
Админ-панель всех комбинаций RAC-команд

## Структура
```
rac_admin_gui/
├── requirements.txt
├── main.py
├── core/
│   ├── __init__.py
│   ├── rac_commands.py
│   ├── command_executor.py      # ОБНОВЛЕН
│   ├── logger.py
│   ├── service_manager.py
│   └── variable_manager.py      # ОБНОВЛЕН
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── command_dialogs.py       # ПОЛНОСТЬЮ ПЕРЕПИСАН
│   ├── variables_dialog.py      # ПОЛНОСТЬЮ ПЕРЕПИСАН
│   └── widgets.py
└── config/
    ├── __init__.py
    └── variables.json
```
