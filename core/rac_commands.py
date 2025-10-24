from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum

class ParamType(Enum):
    STRING = "string"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    ENUM = "enum"
    UUID = "uuid"
    PORT = "port"
    HOST = "host"
    PASSWORD = "password"

@dataclass
class CommandParam:
    name: str
    param_type: ParamType
    required: bool = False
    description: str = ""
    default_value: Any = None
    enum_values: List[str] = field(default_factory=list)
    short_name: str = ""

@dataclass
class RacCommand:
    mode: str
    command: str
    description: str
    parameters: List[CommandParam] = field(default_factory=list)
    sub_commands: List['RacCommand'] = field(default_factory=list)

class RACCommands:
    """Класс содержащий все команды RAC"""
    
    @staticmethod
    def get_all_commands() -> Dict[str, List[RacCommand]]:
        """Возвращает все команды сгруппированные по режимам"""
        return {
            "help": RACCommands._get_help_commands(),
            "agent": RACCommands._get_agent_commands(),
            "cluster": RACCommands._get_cluster_commands(),
            "manager": RACCommands._get_manager_commands(),
            "server": RACCommands._get_server_commands(),
            "process": RACCommands._get_process_commands(),
            "service": RACCommands._get_service_commands(),
            "infobase": RACCommands._get_infobase_commands(),
            "connection": RACCommands._get_connection_commands(),
            "session": RACCommands._get_session_commands(),
            "lock": RACCommands._get_lock_commands(),
            "rule": RACCommands._get_rule_commands(),
            "profile": RACCommands._get_profile_commands(),
            "counter": RACCommands._get_counter_commands(),
            "limit": RACCommands._get_limit_commands(),
        }
    
    @staticmethod
    def _get_help_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="help",
                command="help",
                description="Отображение справочной информации для указанного режима",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("mode", ParamType.STRING, False, "Режим для получения справки"),
                    CommandParam("version", ParamType.BOOLEAN, False, "Получение версии утилиты", short_name="v"),
                    CommandParam("help", ParamType.BOOLEAN, False, "Краткая информация об утилите", short_name="?")
                ]
            )
        ]
    
    @staticmethod
    def _get_agent_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="agent",
                command="admin list",
                description="Получение списка администраторов агента кластера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("agent-user", ParamType.STRING, False, "Имя администратора агента"),
                    CommandParam("agent-pwd", ParamType.PASSWORD, False, "Пароль администратора агента")
                ]
            ),
            RacCommand(
                mode="agent",
                command="admin register",
                description="Добавление нового администратора агента кластера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("agent-user", ParamType.STRING, False, "Имя администратора агента"),
                    CommandParam("agent-pwd", ParamType.PASSWORD, False, "Пароль администратора агента"),
                    CommandParam("name", ParamType.STRING, True, "Имя администратора"),
                    CommandParam("pwd", ParamType.PASSWORD, False, "Пароль администратора"),
                    CommandParam("descr", ParamType.STRING, False, "Описание администратора"),
                    CommandParam("auth", ParamType.ENUM, False, "Способы аутентификации", enum_values=["pwd", "os"]),
                    CommandParam("os-user", ParamType.STRING, False, "Имя пользователя ОС")
                ]
            ),
            RacCommand(
                mode="agent",
                command="admin remove",
                description="Удаление администратора агента кластера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("agent-user", ParamType.STRING, False, "Имя администратора агента"),
                    CommandParam("agent-pwd", ParamType.PASSWORD, False, "Пароль администратора агента"),
                    CommandParam("name", ParamType.STRING, True, "Имя администратора агента")
                ]
            ),
            RacCommand(
                mode="agent",
                command="version",
                description="Получение версии агента кластера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("agent-user", ParamType.STRING, False, "Имя администратора агента"),
                    CommandParam("agent-pwd", ParamType.PASSWORD, False, "Пароль администратора агента")
                ]
            )
        ]
    
    @staticmethod
    def _get_cluster_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="cluster",
                command="admin list",
                description="Получение списка администраторов кластера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                ]
            ),
            RacCommand(
                mode="cluster",
                command="admin register",
                description="Добавление нового администратора кластера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("name", ParamType.STRING, True, "Имя администратора"),
                    CommandParam("pwd", ParamType.PASSWORD, False, "Пароль администратора"),
                    CommandParam("descr", ParamType.STRING, False, "Описание администратора"),
                    CommandParam("auth", ParamType.ENUM, False, "Способы аутентификации", enum_values=["pwd", "os"]),
                    CommandParam("os-user", ParamType.STRING, False, "Имя пользователя ОС"),
                    CommandParam("agent-user", ParamType.STRING, False, "Администратор агента"),
                    CommandParam("agent-pwd", ParamType.PASSWORD, False, "Пароль администратора агента")
                ]
            ),
            RacCommand(
                mode="cluster",
                command="admin remove",
                description="Удаление администратора кластера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("name", ParamType.STRING, True, "Имя администратора кластера"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера")
                ]
            ),
            RacCommand(
                mode="cluster",
                command="info",
                description="Получение информации о кластере",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера")
                ]
            ),
            RacCommand(
                mode="cluster",
                command="list",
                description="Получение списка информации о кластерах",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                ]
            ),
            RacCommand(
                mode="cluster",
                command="insert",
                description="Регистрация нового кластера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("name", ParamType.STRING, False, "Имя кластера"),
                    CommandParam("expiration-timeout", ParamType.INTEGER, False, "Период принудительного завершения (сек)"),
                    CommandParam("lifetime-limit", ParamType.INTEGER, False, "Период перезапуска процессов (сек)"),
                    CommandParam("max-memory-size", ParamType.INTEGER, False, "Максимальный объем памяти (Кб)"),
                    CommandParam("max-memory-time-limit", ParamType.INTEGER, False, "Период превышения памяти (сек)"),
                    CommandParam("security-level", ParamType.INTEGER, False, "Уровень безопасности"),
                    CommandParam("session-fault-tolerance-level", ParamType.INTEGER, False, "Уровень отказоустойчивости"),
                    CommandParam("load-balancing-mode", ParamType.ENUM, False, "Режим балансировки", enum_values=["performance", "memory"]),
                    CommandParam("errors-count-threshold", ParamType.INTEGER, False, "Допустимое отклонение ошибок (%)"),
                    CommandParam("kill-problem-processes", ParamType.ENUM, False, "Завершать проблемные процессы", enum_values=["yes", "no"]),
                    CommandParam("kill-by-memory-with-dump", ParamType.ENUM, False, "Дамп при превышении памяти", enum_values=["yes", "no"]),
                    CommandParam("agent-user", ParamType.STRING, False, "Администратор агента"),
                    CommandParam("agent-pwd", ParamType.PASSWORD, False, "Пароль администратора агента")
                ]
            ),
            RacCommand(
                mode="cluster",
                command="update",
                description="Обновление параметров кластера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("name", ParamType.STRING, False, "Имя кластера"),
                    CommandParam("expiration-timeout", ParamType.INTEGER, False, "Период принудительного завершения (сек)"),
                    CommandParam("lifetime-limit", ParamType.INTEGER, False, "Период перезапуска процессов (сек)"),
                    CommandParam("max-memory-size", ParamType.INTEGER, False, "Максимальный объем памяти (Кб)"),
                    CommandParam("max-memory-time-limit", ParamType.INTEGER, False, "Период превышения памяти (сек)"),
                    CommandParam("security-level", ParamType.INTEGER, False, "Уровень безопасности"),
                    CommandParam("session-fault-tolerance-level", ParamType.INTEGER, False, "Уровень отказоустойчивости"),
                    CommandParam("load-balancing-mode", ParamType.ENUM, False, "Режим балансировки", enum_values=["performance", "memory"]),
                    CommandParam("errors-count-threshold", ParamType.INTEGER, False, "Допустимое отклонение ошибок (%)"),
                    CommandParam("kill-problem-processes", ParamType.ENUM, False, "Завершать проблемные процессы", enum_values=["yes", "no"]),
                    CommandParam("kill-by-memory-with-dump", ParamType.ENUM, False, "Дамп при превышении памяти", enum_values=["yes", "no"]),
                    CommandParam("agent-user", ParamType.STRING, False, "Администратор агента"),
                    CommandParam("agent-pwd", ParamType.PASSWORD, False, "Пароль администратора агента")
                ]
            ),
            RacCommand(
                mode="cluster",
                command="remove",
                description="Удаление кластера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера")
                ]
                )
        ]
    
    @staticmethod
    def _get_manager_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="manager",
                command="info",
                description="Получение информации о менеджере",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("manager", ParamType.UUID, True, "Идентификатор менеджера")
                ]
            ),
            RacCommand(
                mode="manager",
                command="list",
                description="Получение списка информации о менеджерах",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера")
                ]
            )
        ]
    
    @staticmethod
    def _get_server_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="server",
                command="info",
                description="Получение информации о рабочем сервере",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("server", ParamType.UUID, True, "Идентификатор сервера")
                ]
            ),
            RacCommand(
                mode="server",
                command="list",
                description="Получение списка информации о рабочих серверах",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера")
                ]
            ),
            RacCommand(
                mode="server",
                command="insert",
                description="Регистрация рабочего сервера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("agent-host", ParamType.HOST, True, "Хост агента сервера"),
                    CommandParam("agent-port", ParamType.PORT, True, "Порт агента сервера"),
                    CommandParam("port-range", ParamType.STRING, True, "Диапазон портов (min:max)"),
                    CommandParam("name", ParamType.STRING, False, "Имя сервера"),
                    CommandParam("using", ParamType.ENUM, False, "Вариант использования", enum_values=["main", "normal"]),
                    CommandParam("infobases-limit", ParamType.INTEGER, False, "Лимит баз на процесс"),
                    CommandParam("memory-limit", ParamType.INTEGER, False, "Лимит памяти (Кб)"),
                    CommandParam("connections-limit", ParamType.INTEGER, False, "Лимит соединений"),
                    CommandParam("cluster-port", ParamType.PORT, False, "Порт менеджера кластера"),
                    CommandParam("dedicate-managers", ParamType.ENUM, False, "Размещение менеджеров", enum_values=["all", "none"]),
                    CommandParam("safe-working-processes-memory-limit", ParamType.INTEGER, False, "Безопасная память процессов"),
                    CommandParam("safe-call-memory-limit", ParamType.INTEGER, False, "Безопасная память вызова"),
                    CommandParam("critical-total-memory", ParamType.INTEGER, False, "Критическая память"),
                    CommandParam("temporary-allowed-total-memory", ParamType.INTEGER, False, "Временная память"),
                    CommandParam("temporary-allowed-total-memory-time-limit", ParamType.INTEGER, False, "Лимит временной памяти"),
                    CommandParam("service-principal-name", ParamType.STRING, False, "SPN сервера"),
                    CommandParam("speech-to-text-model-directory", ParamType.STRING, False, "Каталог моделей речи"),
                    CommandParam("add-prohibiting-assignment-rule", ParamType.ENUM, False, "Запрещающее требование", enum_values=["yes"])
                ]
            ),
            RacCommand(
                mode="server",
                command="update",
                description="Изменение параметров рабочего сервера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("server", ParamType.UUID, True, "Идентификатор сервера"),
                    CommandParam("port-range", ParamType.STRING, False, "Диапазон портов (min:max)"),
                    CommandParam("using", ParamType.ENUM, False, "Вариант использования", enum_values=["main", "normal"]),
                    CommandParam("infobases-limit", ParamType.INTEGER, False, "Лимит баз на процесс"),
                    CommandParam("memory-limit", ParamType.INTEGER, False, "Лимит памяти (Кб)"),
                    CommandParam("connections-limit", ParamType.INTEGER, False, "Лимит соединений"),
                    CommandParam("dedicate-managers", ParamType.ENUM, False, "Размещение менеджеров", enum_values=["all", "none"]),
                    CommandParam("safe-working-processes-memory-limit", ParamType.INTEGER, False, "Безопасная память процессов"),
                    CommandParam("safe-call-memory-limit", ParamType.INTEGER, False, "Безопасная память вызова"),
                    CommandParam("critical-total-memory", ParamType.INTEGER, False, "Критическая память"),
                    CommandParam("temporary-allowed-total-memory", ParamType.INTEGER, False, "Временная память"),
                    CommandParam("temporary-allowed-total-memory-time-limit", ParamType.INTEGER, False, "Лимит временной памяти"),
                    CommandParam("service-principal-name", ParamType.STRING, False, "SPN сервера"),
                    CommandParam("speech-to-text-model-directory", ParamType.STRING, False, "Каталог моделей речи")
                ]
            ),
            RacCommand(
                mode="server",
                command="remove",
                description="Удаление рабочего сервера",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("server", ParamType.UUID, True, "Идентификатор сервера")
                ]
            )
            ]
    
    @staticmethod
    def _get_process_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="process",
                command="info",
                description="Получение информации о рабочем процессе",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("process", ParamType.UUID, True, "Идентификатор процесса"),
                    CommandParam("licenses", ParamType.BOOLEAN, False, "Информация о лицензиях")
                ]
            ),
            RacCommand(
                mode="process",
                command="list",
                description="Получение списка информации о рабочих процессах",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластera"),
                    CommandParam("server", ParamType.UUID, False, "Идентификатор сервера"),
                    CommandParam("licenses", ParamType.BOOLEAN, False, "Информация о лицензиях")
                ]
            )
        ]
    
    @staticmethod
    def _get_service_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="service",
                command="list",
                description="Получение списка информации о сервисах",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера")
                ]
            )
        ]
    
    @staticmethod
    def _get_infobase_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="infobase",
                command="info",
                description="Получение информации об информационной базе",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("infobase", ParamType.UUID, True, "Идентификатор базы"),
                    CommandParam("infobase-user", ParamType.STRING, False, "Администратор базы"),
                    CommandParam("infobase-pwd", ParamType.PASSWORD, False, "Пароль администратора базы")
                ]
            ),
            RacCommand(
                mode="infobase",
                command="summary info",
                description="Получение краткой информации об указанной информационной базе",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("infobase", ParamType.UUID, True, "Идентификатор базы")
                ]
            ),
            RacCommand(
                mode="infobase",
                command="summary list",
                description="Получение списка краткой информации об информационных базах",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластera"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера")
                ]
            ),
            RacCommand(
                mode="infobase",
                command="summary update",
                description="Обновление краткой информации об информационной базе",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("infobase", ParamType.UUID, True, "Идентификатор базы"),
                    CommandParam("descr", ParamType.STRING, False, "Описание базы")
                ]
            ),
            RacCommand(
                mode="infobase",
                command="create",
                description="Создание информационной базы",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("create-database", ParamType.BOOLEAN, False, "Создать базу данных"),
                    CommandParam("name", ParamType.STRING, True, "Имя базы"),
                    CommandParam("dbms", ParamType.ENUM, True, "Тип СУБД", enum_values=["MSSQLServer", "PostgreSQL", "IBMDB2", "OracleDatabase"]),
                    CommandParam("db-server", ParamType.HOST, True, "Сервер БД"),
                    CommandParam("db-name", ParamType.STRING, True, "Имя БД"),
                    CommandParam("locale", ParamType.STRING, True, "Национальные настройки"),
                    CommandParam("db-user", ParamType.STRING, False, "Администратор БД"),
                    CommandParam("db-pwd", ParamType.PASSWORD, False, "Пароль БД"),
                    CommandParam("descr", ParamType.STRING, False, "Описание"),
                    CommandParam("date-offset", ParamType.INTEGER, False, "Смещение дат"),
                    CommandParam("security-level", ParamType.INTEGER, False, "Уровень безопасности"),
                    CommandParam("scheduled-jobs-deny", ParamType.ENUM, False, "Блокировка заданий", enum_values=["on", "off"]),
                    CommandParam("license-distribution", ParamType.ENUM, False, "Выдача лицензий", enum_values=["deny", "allow"])
                ]
            ),
            RacCommand(
                mode="infobase",
                command="update",
                description="Обновление информации об информационной базе",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("infobase", ParamType.UUID, True, "Идентификатор базы"),
                    CommandParam("infobase-user", ParamType.STRING, False, "Администратор базы"),
                    CommandParam("infobase-pwd", ParamType.PASSWORD, False, "Пароль администратора базы"),
                    CommandParam("dbms", ParamType.ENUM, False, "Тип СУБД", enum_values=["MSSQLServer", "PostgreSQL", "IBMDB2", "OracleDatabase"]),
                    CommandParam("db-server", ParamType.HOST, False, "Сервер БД"),
                    CommandParam("db-name", ParamType.STRING, False, "Имя БД"),
                    CommandParam("db-user", ParamType.STRING, False, "Администратор БД"),
                    CommandParam("db-pwd", ParamType.PASSWORD, False, "Пароль БД"),
                    CommandParam("descr", ParamType.STRING, False, "Описание"),
                    CommandParam("denied-from", ParamType.STRING, False, "Начало блокировки"),
                    CommandParam("denied-to", ParamType.STRING, False, "Конец блокировки"),
                    CommandParam("denied-message", ParamType.STRING, False, "Сообщение блокировки"),
                    CommandParam("denied-parameter", ParamType.STRING, False, "Параметр блокировки"),
                    CommandParam("permission-code", ParamType.STRING, False, "Код разрешения"),
                    CommandParam("sessions-deny", ParamType.ENUM, False, "Блокировка сеансов", enum_values=["on", "off"]),
                    CommandParam("scheduled-jobs-deny", ParamType.ENUM, False, "Блокировка заданий", enum_values=["on", "off"]),
                    CommandParam("license-distribution", ParamType.ENUM, False, "Выдача лицензий", enum_values=["deny", "allow"]),
                    CommandParam("external-session-manager-connection-string", ParamType.STRING, False, "Параметры внешнего управления"),
                    CommandParam("external-session-manager-required", ParamType.ENUM, False, "Обязательное внешнее управление", enum_values=["yes", "no"]),
                    CommandParam("reserve-working-processes", ParamType.ENUM, False, "Резервирование процессов", enum_values=["yes", "no"]),
                    CommandParam("security-profile-name", ParamType.STRING, False, "Профиль безопасности"),
                    CommandParam("safe-mode-security-profile-name", ParamType.STRING, False, "Профиль безопасности кода"),
                    CommandParam("disable-local-speech-to-text", ParamType.ENUM, False, "Запрет распознавания речи", enum_values=["yes", "no"]),
                    CommandParam("configuration-unload-delay-by-working-process-without-active-users", ParamType.INTEGER, False, "Задержка выгрузки"),
                    CommandParam("minimum-scheduled-jobs-start-period-without-active-users", ParamType.INTEGER, False, "Минимальный период заданий"),
                    CommandParam("maximum-scheduled-jobs-start-shift-without-active-users", ParamType.INTEGER, False, "Максимальный сдвиг заданий")
                ]
            ),
            RacCommand(
                mode="infobase",
                command="drop",
                description="Удаление информационной базы",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("infobase", ParamType.UUID, True, "Идентификатор базы"),
                    CommandParam("infobase-user", ParamType.STRING, False, "Администратор базы"),
                    CommandParam("infobase-pwd", ParamType.PASSWORD, False, "Пароль администратора базы"),
                    CommandParam("drop-database", ParamType.BOOLEAN, False, "Удалить БД"),
                    CommandParam("clear-database", ParamType.BOOLEAN, False, "Очистить БД")
                ]
            )
        ]
    
    @staticmethod
    def _get_connection_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="connection",
                command="info",
                description="Получение информации о соединении",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("connection", ParamType.UUID, True, "Идентификатор соединения")
                ]
            ),
            RacCommand(
                mode="connection",
                command="list",
                description="Получение списка соединений",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("process", ParamType.UUID, False, "Идентификатор процесса"),
                    CommandParam("infobase", ParamType.UUID, False, "Идентификатор базы"),
                    CommandParam("infobase-user", ParamType.STRING, False, "Администратор базы"),
                    CommandParam("infobase-pwd", ParamType.PASSWORD, False, "Пароль администратора базы")
                ]
            ),
            RacCommand(
                mode="connection",
                command="disconnect",
                description="Разрыв соединения",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("process", ParamType.UUID, True, "Идентификатор процесса"),
                    CommandParam("connection", ParamType.UUID, True, "Идентификатор соединения"),
                    CommandParam("infobase-user", ParamType.STRING, False, "Администратор базы"),
                    CommandParam("infobase-pwd", ParamType.PASSWORD, False, "Пароль администратора базы")
                ]
            )
        ]
    
    @staticmethod
    def _get_session_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="session",
                command="info",
                description="Получение информации о сеансе",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("session", ParamType.UUID, True, "Идентификатор сеанса"),
                    CommandParam("licenses", ParamType.BOOLEAN, False, "Информация о лицензиях")
                ]
            ),
            RacCommand(
                mode="session",
                command="list",
                description="Получение списка информации о сеансах",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("infobase", ParamType.UUID, False, "Идентификатор информационной базы"),
                    CommandParam("licenses", ParamType.BOOLEAN, False, "Информация о лицензиях")
                ]
            ),
            RacCommand(
                mode="session",
                command="terminate",
                description="Принудительное завершение сеанса",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("session", ParamType.UUID, True, "Идентификатор сеанса"),
                    CommandParam("error-message", ParamType.STRING, False, "Сообщение о причине завершения")
                ]
            ),
            RacCommand(
                mode="session",
                command="interrupt-current-server-call",
                description="Прерывание текущего серверного вызова",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластera"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("session", ParamType.UUID, True, "Идентификатор сеанса"),
                    CommandParam("error-message", ParamType.STRING, False, "Сообщение о причине прерывания")
                ]
            )
        ]
    
    @staticmethod
    def _get_lock_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="lock",
                command="list",
                description="Получение списка информации о блокировках",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("infobase", ParamType.UUID, False, "Идентификатор базы"),
                    CommandParam("connection", ParamType.UUID, False, "Идентификатор соединения"),
                    CommandParam("session", ParamType.UUID, False, "Идентификатор сеанса")
                ]
            )
        ]
    
    @staticmethod
    def _get_rule_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="rule",
                command="apply",
                description="Применение требований",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("full", ParamType.BOOLEAN, False, "Полное применение"),
                    CommandParam("partial", ParamType.BOOLEAN, False, "Частичное применение")
                ]
            ),
            RacCommand(
                mode="rule",
                command="info",
                description="Получение информации о требовании назначения",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("server", ParamType.UUID, True, "Идентификатор сервера"),
                    CommandParam("rule", ParamType.UUID, True, "Идентификатор требования")
                    ]
            ),
            RacCommand(
                mode="rule",
                command="list",
                description="Получение списка требований назначения",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("server", ParamType.UUID, True, "Идентификатор сервера")
                ]
            ),
            RacCommand(
                mode="rule",
                command="insert",
                description="Вставка нового требования назначения в список",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("server", ParamType.UUID, True, "Идентификатор сервера"),
                    CommandParam("position", ParamType.INTEGER, True, "Позиция в списке"),
                    CommandParam("object-type", ParamType.STRING, False, "Тип объекта"),
                    CommandParam("infobase-name", ParamType.STRING, False, "Имя базы"),
                    CommandParam("rule-type", ParamType.ENUM, False, "Тип правила", enum_values=["auto", "always", "never"]),
                    CommandParam("application-ext", ParamType.STRING, False, "Приложение с уточнением"),
                    CommandParam("priority", ParamType.INTEGER, False, "Приоритет")
                ]
            ),
            RacCommand(
                mode="rule",
                command="update",
                description="Обновление параметров существующего требования назначения в списке",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("server", ParamType.UUID, True, "Идентификатор сервера"),
                    CommandParam("rule", ParamType.UUID, True, "Идентификатор требования"),
                    CommandParam("position", ParamType.INTEGER, True, "Позиция в списке"),
                    CommandParam("object-type", ParamType.STRING, False, "Тип объекта"),
                    CommandParam("infobase-name", ParamType.STRING, False, "Имя базы"),
                    CommandParam("rule-type", ParamType.ENUM, False, "Тип правила", enum_values=["auto", "always", "never"]),
                    CommandParam("application-ext", ParamType.STRING, False, "Приложение с уточнением"),
                    CommandParam("priority", ParamType.INTEGER, False, "Приоритет")
                ]
            ),
            RacCommand(
                mode="rule",
                command="remove",
                description="Удаление требования назначения",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("server", ParamType.UUID, True, "Идентификатор сервера"),
                    CommandParam("rule", ParamType.UUID, True, "Идентификатор требования")
                    ]
            )
        ]
    
    @staticmethod
    def _get_profile_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="profile",
                command="list",
                description="Получение списка профилей безопасности",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера")
                ]
            ),
            RacCommand(
                mode="profile",
                command="update",
                description="Создание нового профиля безопасности или обновление параметров существующего",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("name", ParamType.STRING, True, "Имя профиля"),
                    CommandParam("descr", ParamType.STRING, False, "Описание профиля"),
                    CommandParam("config", ParamType.ENUM, False, "Использование из конфигурации", enum_values=["yes", "no"]),
                    CommandParam("priv", ParamType.ENUM, False, "Привилегированный режим", enum_values=["yes", "no"]),
                    CommandParam("full-privileged-mode", ParamType.ENUM, False, "Полный привилегированный режим", enum_values=["yes", "no"]),
                    CommandParam("privileged-mode-roles", ParamType.STRING, False, "Роли привилегированного режима"),
                    CommandParam("crypto", ParamType.ENUM, False, "Криптография", enum_values=["yes", "no"]),
                    CommandParam("right-extension", ParamType.ENUM, False, "Расширение прав", enum_values=["yes", "no"]),
                    CommandParam("right-extension-definition-roles", ParamType.STRING, False, "Роли расширения прав"),
                    CommandParam("all-modules-extension", ParamType.ENUM, False, "Расширение всех модулей", enum_values=["yes", "no"]),
                    CommandParam("modules-available-for-extension", ParamType.STRING, False, "Доступные для расширения модули"),
                    CommandParam("modules-not-available-for-extension", ParamType.STRING, False, "Недоступные для расширения модули")
                ]
            ),
            RacCommand(
                mode="profile",
                command="remove",
                description="Удаление профиля безопасности",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("name", ParamType.STRING, True, "Имя профиля")
                ]
            )
        ]
    
    @staticmethod
    def _get_counter_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="counter",
                command="list",
                description="Получение списка счетчиков",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера")
                    ]
            ),
            RacCommand(
                mode="counter",
                command="info",
                description="Получение информации по счетчику",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("counter", ParamType.STRING, True, "Идентификатор счетчика")
                ]
            ),
            RacCommand(
                mode="counter",
                command="update",
                description="Создание нового счетчика или обновление параметров существующего",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("name", ParamType.STRING, True, "Имя счетчика"),
                    CommandParam("collection-time", ParamType.STRING, True, "Время накопления"),
                    CommandParam("group", ParamType.ENUM, True, "Тип группировки", enum_values=["users", "data-separation"]),
                    CommandParam("filter-type", ParamType.ENUM, True, "Тип отбора", enum_values=["all-selected", "all-but-selected", "all"]),
                    CommandParam("filter", ParamType.STRING, True, "Значение отбора"),
                    CommandParam("duration", ParamType.ENUM, False, "Анализ длительности", enum_values=["analyze", "not-analyze"]),
                    CommandParam("cpu-time", ParamType.ENUM, False, "Анализ процессорного времени", enum_values=["analyze", "not-analyze"]),
                    CommandParam("memory", ParamType.ENUM, False, "Анализ памяти", enum_values=["analyze", "not-analyze"]),
                    CommandParam("read", ParamType.ENUM, False, "Анализ чтения", enum_values=["analyze", "not-analyze"]),
                    CommandParam("write", ParamType.ENUM, False, "Анализ записи", enum_values=["analyze", "not-analyze"]),
                    CommandParam("duration-dbms", ParamType.ENUM, False, "Анализ СУБД", enum_values=["analyze", "not-analyze"]),
                    CommandParam("dbms-bytes", ParamType.ENUM, False, "Анализ данных СУБД", enum_values=["analyze", "not-analyze"]),
                    CommandParam("service", ParamType.ENUM, False, "Анализ сервисов", enum_values=["analyze", "not-analyze"]),
                    CommandParam("call", ParamType.ENUM, False, "Анализ вызовов", enum_values=["analyze", "not-analyze"]),
                    CommandParam("number-of-active-sessions", ParamType.ENUM, False, "Анализ активных сеансов", enum_values=["analyze", "not-analyze"]),
                    CommandParam("number-of-sessions", ParamType.ENUM, False, "Анализ сеансов", enum_values=["analyze", "not-analyze"]),
                    CommandParam("descr", ParamType.STRING, False, "Описание")
                ]
            ),
            RacCommand(
                mode="counter",
                command="values",
                description="Вывод текущих значений счетчика потребления ресурсов",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("counter", ParamType.STRING, True, "Имя счетчика"),
                    CommandParam("object", ParamType.STRING, False, "Фильтры")
                ]
            ),
            RacCommand(
                mode="counter",
                command="remove",
                description="Удаление счетчика потребления ресурсов",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("name", ParamType.STRING, True, "Имя счетчика")
                ]
            ),
            RacCommand(
                mode="counter",
                command="clear",
                description="Очистка значений счетчика",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("counter", ParamType.STRING, True, "Имя счетчика"),
                    CommandParam("object", ParamType.STRING, False, "Фильтры")
                ]
            ),
            RacCommand(
                mode="counter",
                command="accumulated-values",
                description="Получение списка накопленных значений счетчика",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("counter", ParamType.STRING, True, "Имя счетчика"),
                    CommandParam("object", ParamType.STRING, False, "Фильтры")
                ]
            )
        ]
    
    @staticmethod
    def _get_limit_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="limit",
                command="list",
                description="Получение списка ограничений",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера")
                ]
            ),
            RacCommand(
                mode="limit",
                command="info",
                description="Получение информации по ограничению",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("limit", ParamType.STRING, True, "Идентификатор ограничения")
                ]
            ),
            RacCommand(
                mode="limit",
                command="update",
                description="Создание нового ограничения или обновление параметров существующего",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("name", ParamType.STRING, True, "Имя ограничения"),
                    CommandParam("action", ParamType.ENUM, True, "Действие", enum_values=["none", "set-low-priority-thread", "interrupt-current-call", "interrupt-session"]),
                    CommandParam("counter", ParamType.STRING, False, "Счетчик"),
                    CommandParam("duration", ParamType.INTEGER, False, "Ограничение длительности"),
                    CommandParam("cpu-time", ParamType.INTEGER, False, "Ограничение процессорного времени"),
                    CommandParam("memory", ParamType.INTEGER, False, "Ограничение памяти"),
                    CommandParam("read", ParamType.INTEGER, False, "Ограничение чтения"),
                    CommandParam("write", ParamType.INTEGER, False, "Ограничение записи"),
                    CommandParam("duration-dbms", ParamType.INTEGER, False, "Ограничение СУБД"),
                    CommandParam("dbms-bytes", ParamType.INTEGER, False, "Ограничение данных СУБД"),
                    CommandParam("service", ParamType.INTEGER, False, "Ограничение сервисов"),
                    CommandParam("call", ParamType.INTEGER, False, "Ограничение вызовов"),
                    CommandParam("number-of-active-sessions", ParamType.INTEGER, False, "Ограничение активных сеансов"),
                    CommandParam("number-of-sessions", ParamType.INTEGER, False, "Ограничение сеансов"),
                    CommandParam("error-message", ParamType.STRING, False, "Сообщение об ошибке"),
                    CommandParam("descr", ParamType.STRING, False, "Описание")
                ]
            ),
            RacCommand(
                mode="limit",
                command="remove",
                description="Удаление ограничения потребления ресурсов",
                parameters=[
                    CommandParam("host", ParamType.HOST, False, "Адрес сервера (по умолчанию: localhost)"),
                    CommandParam("port", ParamType.PORT, False, "Порт сервера (по умолчанию: 1545)"),
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("name", ParamType.STRING, True, "Имя ограничения")
                ]
            )
        ]
