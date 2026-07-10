import logging
from pathlib import Path

from .config import Config, ColorConfig
from .exceptions import DuplicateLogger, InvalidConfigure, InvalidConstructionMode
from .handlers import ConsoleHandler, FileHandler


class Log:
    active_loggers: list[str] = []

    def __init__(
        self,
        logger_name: str,
        config: Config = Config(),
        color_config: ColorConfig = ColorConfig(),
    ) -> None:
        self.validate_parameters(config=config, color_config=color_config)
        self._logger_name = self._validate_logger(logger_name=logger_name)
        self._config = config
        self._color_config = color_config

        self.logger: logging.Logger = logging.getLogger(name=self._logger_name)
        self._initial_setup()
        self.setup_handlers()

    @classmethod
    def _add_log_to_global_list(cls, logger_name: str) -> None:
        cls.active_loggers.append(logger_name)

    @classmethod
    def _is_logger_exist(cls, logger_name: str) -> bool:
        if logger_name in cls.active_loggers:
            return True
        return False

    def validate_parameters(self, config : object, color_config : object):
        if not isinstance(config, Config):
            raise InvalidConfigure("Invalid Config passed as a parameter")
        if not isinstance(color_config, ColorConfig):
            raise InvalidConfigure("Invalid ColorConfig passed as a parameter")

    def _validate_logger(self, logger_name: str) -> str:
        if self._is_logger_exist(logger_name=logger_name):
            raise DuplicateLogger(logger_name=logger_name)

        self._add_log_to_global_list(logger_name=logger_name)
        return logger_name

    def _initial_setup(self) -> None:
        self.logger.handlers.clear()
        self.logger.propagate = False
        self.logger.setLevel(self._config.logging_level)

    def setup_handlers(self):
        if self._config.construction_mode == "default":
            self.default_handler_setup()
        elif self._config.construction_mode == "dev":
            self.dev_handler_setup()
        elif self._config.construction_mode == "test":
            self.test_handler_setup()
        else:
            raise InvalidConstructionMode("Invalid Construction Mode")

    def default_handler_setup(self):
        if self._config.console_logging:
            self.logger.addHandler(
                ConsoleHandler(self._config, self._color_config).get_console_handler()
            )
        if self._config.file_logging:
            self.logger.addHandler(
                FileHandler(self._config, self._color_config).get_console_handler()
            )

    def dev_handler_setup(self):
        self._config.logging_level = "DEBUG"
        self.logger.setLevel(logging.DEBUG)
        if self._config.console_logging:
            self.logger.addHandler(
                ConsoleHandler(
                    config=self._config, color_config=self._color_config
                ).get_console_handler()
            )
        if self._config.file_logging:
            self.logger.addHandler(
                FileHandler(
                    config=self._config, color_config=self._color_config
                ).get_console_handler()
            )

    def test_handler_setup(self):
        self._config.logging_level = "WARNING"
        self.logger.setLevel(logging.WARNING)
        self._config.log_file_path = (
            Path(self._config.log_file_path).parent / "test_log.txt"
        )
        if self._config.file_logging:
            self.logger.addHandler(
                FileHandler(
                    config=self._config, color_config=self._color_config
                ).get_console_handler()
            )
