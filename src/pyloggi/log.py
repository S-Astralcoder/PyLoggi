"""High-level logger construction for pyloggi."""

import logging
from pathlib import Path

from .config import Config, ColorConfig
from .exceptions import (
    DuplicateLogger,
    EmptyLoggerName,
    InvalidConfigure,
    InvalidConstructionMode,
    LimitationError,
)
from .handlers import ConsoleHandler, FileHandler


class Log:
    """Build a named logger from pyloggi configuration objects.

    The class owns validation, duplicate-name tracking, base logger setup, and
    handler construction for the supported construction modes.
    """

    active_loggers: set[str] = set()

    def __init__(
        self,
        logger_name: str,
        config: Config,
        color_config: ColorConfig,
        allow_duplicates: bool = False,
    ) -> None:
        """Validate settings and create a configured ``logging.Logger``."""

        self.allow_duplicates = allow_duplicates
        self.validate_parameters(config=config, color_config=color_config)
        self._logger_name = self._validate_logger(logger_name=logger_name)
        self._config = config
        self._color_config = color_config

        self.logger: logging.Logger = logging.getLogger(name=self._logger_name)
        self._initial_setup()
        self.setup_handlers()

    @classmethod
    def _add_log_to_global_list(cls, logger_name: str) -> None:
        """Register a logger name so duplicates can be detected later."""
        cls.active_loggers.add(logger_name)

    @classmethod
    def _is_logger_exist(cls, logger_name: str) -> bool:
        """Return whether a logger name has already been registered."""
        return logger_name in cls.active_loggers

    def validate_parameters(self, config: object, color_config: object):
        """Ensure logger setup receives the expected configuration objects."""

        if not isinstance(config, Config):
            raise InvalidConfigure("Invalid Config passed as a parameter")
        if not isinstance(color_config, ColorConfig):
            raise InvalidConfigure("Invalid ColorConfig passed as a parameter")

    def _validate_logger(self, logger_name: str) -> str:
        """Validate and register a logger name."""
        if not isinstance(logger_name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError("logger_name must be a string")

        logger_name = logger_name.strip()

        if logger_name == "":
            raise EmptyLoggerName("logger_name should not be empty")

        if logger_name == "root":
            raise LimitationError("Logger name 'root' is not allowed")

        if self._is_logger_exist(logger_name) and not self.allow_duplicates:
            raise DuplicateLogger(logger_name)

        self._add_log_to_global_list(logger_name)
        return logger_name

    def _initial_setup(self) -> None:
        """Reset existing handlers and apply base logger settings."""

        while self.logger.handlers:
            handler = self.logger.handlers[0]
            handler.close()
            self.logger.removeHandler(handler)
        self.logger.propagate = False
        self.logger.setLevel(self._config.logging_level)

    def setup_handlers(self):
        """Attach handlers for the selected construction mode."""

        if self._config.construction_mode == "default":
            self.default_handler_setup()
        elif self._config.construction_mode == "dev":
            self.dev_handler_setup()
        elif self._config.construction_mode == "test":
            self.test_handler_setup()
        else:
            raise InvalidConstructionMode("Invalid Construction Mode")

    def default_handler_setup(self):
        """Attach handlers using the configuration exactly as provided."""

        if self._config.console_logging:
            self.logger.addHandler(
                ConsoleHandler(self._config, self._color_config).get_handler()
            )
        if self._config.file_logging:
            self.logger.addHandler(
                FileHandler(self._config, self._color_config).get_handler()
            )

    def dev_handler_setup(self):
        """Attach development handlers, defaulting to DEBUG level."""

        if not self._config.disable_auto_level_construction:
            self._config.logging_level = "DEBUG"
            self.logger.setLevel(logging.DEBUG)
        if self._config.console_logging:
            self.logger.addHandler(
                ConsoleHandler(
                    config=self._config, color_config=self._color_config
                ).get_handler()
            )
        if self._config.file_logging:
            self.logger.addHandler(
                FileHandler(
                    config=self._config, color_config=self._color_config
                ).get_handler()
            )

    def test_handler_setup(self):
        """Attach test handlers, defaulting to WARNING file-only logging."""

        if not self._config.disable_auto_level_construction:
            self._config.logging_level = "WARNING"
            self.logger.setLevel(logging.WARNING)
            self._config.log_file_path = (
                Path(self._config.log_file_path).parent / "test_log.txt"
            )
        if not self._config.disable_auto_level_construction:
            self._config.console_logging = False
            self._config.file_logging = True

        if self._config.console_logging:
            self.logger.addHandler(
                ConsoleHandler(
                    config=self._config, color_config=self._color_config
                ).get_handler()
            )
        if self._config.file_logging:
            self.logger.addHandler(
                FileHandler(
                    config=self._config, color_config=self._color_config
                ).get_handler()
            )

    @classmethod
    def get_active_loggers(cls):
        """Return the names registered through ``Log`` instances."""

        return cls.active_loggers


def get_logger(
    name: str,
    config: Config | None = None,
    color_config: ColorConfig | None = None,
    allow_duplicates: bool = False,
) -> logging.Logger:
    log = Log(
        logger_name=name,
        config=config or Config(),
        color_config=color_config or ColorConfig(),
        allow_duplicates=allow_duplicates,
    )
    return log.logger
