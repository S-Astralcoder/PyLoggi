from config import Config
from exceptions import DuplicateLogger


class Log:
    active_loggers: list[str] = []

    def __init__(self, logger_name: str, config: Config = Config()) -> None:
        self.logger_name = self.validate_logger(logger_name=logger_name)
        self.config = config
        


    @classmethod
    def add_log_to_global_list(cls, logger_name: str) -> None:
        cls.active_loggers.append(logger_name)

    @classmethod
    def is_logger_exist(cls, logger_name: str) -> bool:
        if logger_name in cls.active_loggers:
            return True
        return False

    def validate_logger(self, logger_name: str) -> str:
        if not self.is_logger_exist(logger_name=logger_name):
            DuplicateLogger(logger_name=logger_name)
        return logger_name
