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
                    CommandParam("agent-user", ParamType.STRING, False, "Имя администратора агента"),
                    CommandParam("agent-pwd", ParamType.PASSWORD, False, "Пароль администратора агента")
                ]
            ),
            RacCommand(
                mode="agent",
                command="admin register",
                description="Добавление нового администратора агента кластера",
                parameters=[
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
                    CommandParam("agent-user", ParamType.STRING, False, "Имя администратора агента"),
                    CommandParam("agent-pwd", ParamType.PASSWORD, False, "Пароль администратора агента")
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
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера"),
                    CommandParam("cluster-user", ParamType.STRING, False, "Администратор кластера"),
                    CommandParam("cluster-pwd", ParamType.PASSWORD, False, "Пароль администратора кластера"),
                    CommandParam("session", ParamType.UUID, True, "Идентификатор сеанса"),
                    CommandParam("error-message", ParamType.STRING, False, "Сообщение о причине прерывания")
                ]
            )
        ]
    
    # Аналогичные методы для остальных режимов (реализованы по тому же принципу)
    @staticmethod
    def _get_cluster_commands() -> List[RacCommand]:
        return [
            RacCommand(
                mode="cluster",
                command="admin list",
                description="Получение списка администраторов кластера",
                parameters=[]
            ),
            RacCommand(
                mode="cluster",
                command="admin register",
                description="Добавление нового администратора кластера",
                parameters=[
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
                command="info",
                description="Получение информации о кластере",
                parameters=[
                    CommandParam("cluster", ParamType.UUID, True, "Идентификатор кластера")
                ]
            ),
            RacCommand(
                mode="cluster",
                command="list",
                description="Получение списка информации о кластерах",
                parameters=[]
            )
        ]
    
    # Сокращённо - остальные режимы реализуются аналогично
    @staticmethod
    def _get_manager_commands() -> List[RacCommand]:
        return []  # Реализация по аналогии
    
    @staticmethod
    def _get_server_commands() -> List[RacCommand]:
        return []  # Реализация по аналогии
    
    @staticmethod
    def _get_process_commands() -> List[RacCommand]:
        return []  # Реализация по аналогии
    
    @staticmethod
    def _get_service_commands() -> List[RacCommand]:
        return []  # Реализация по аналогии
    
    @staticmethod
    def _get_infobase_commands() -> List[RacCommand]:
        return []  # Реализация по аналогии
    
    @staticmethod
    def _get_connection_commands() -> List[RacCommand]:
        return []  # Реализация по аналогии
    
    @staticmethod
    def _get_lock_commands() -> List[RacCommand]:
        return []  # Реализация по аналогии
    
    @staticmethod
    def _get_rule_commands() -> List[RacCommand]:
        return []  # Реализация по аналогии
    
    @staticmethod
    def _get_profile_commands() -> List[RacCommand]:
        return []  # Реализация по аналогии
    
    @staticmethod
    def _get_counter_commands() -> List[RacCommand]:
        return []  # Реализация по аналогии
    
    @staticmethod
    def _get_limit_commands() -> List[RacCommand]:
        return []  # Реализация по аналогии
