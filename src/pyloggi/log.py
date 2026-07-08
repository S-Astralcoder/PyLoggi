import logging

from .config import Config
from .exceptions import DuplicateLogger


class Log:
    active_loggers: list[str] = []
    def __init__(self, logger_name: str, config: Config = Config()) -> None:
        self._logger_name = self._validate_logger(logger_name=logger_name)
        self._config = config

        self.logger : logging.Logger = logging.getLogger(name=self._logger_name)
        

    @classmethod
    def _add_log_to_global_list(cls, logger_name: str) -> None:
        cls.active_loggers.append(logger_name)

    @classmethod
    def _is_logger_exist(cls, logger_name: str) -> bool:
        if logger_name in cls.active_loggers:
            return True
        return False

    def _validate_logger(self, logger_name: str) -> str:
        if self._is_logger_exist(logger_name=logger_name):
            raise DuplicateLogger(logger_name=logger_name)
        
        self._add_log_to_global_list(logger_name=logger_name)
        return logger_name
