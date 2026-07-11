"""High-level logger construction for pyloggi.

Use ``Log`` when you need access to pyloggi's wrapper object. Use
``get_logger()`` when you only need a standard ``logging.Logger``.
"""

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

    The class validates names and configuration objects, tracks registered
    logger names, resets existing handlers for the selected logger, and attaches
    handlers for the configured construction mode.
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
            raise InvalidConfigure(
                "config must be an instance of pyloggi.config.Config."
            )
        if not isinstance(color_config, ColorConfig):
            raise InvalidConfigure(
                "color_config must be an instance of pyloggi.config.ColorConfig."
            )

    def _validate_logger(self, logger_name: str) -> str:
        """Validate, normalize, and register a logger name."""
        if not isinstance(logger_name, str):  # pyright: ignore[reportUnnecessaryIsInstance]
            raise TypeError(
                f"logger_name must be a string, got {type(logger_name).__name__}."
            )

        logger_name = logger_name.strip()

        if logger_name == "":
            raise EmptyLoggerName("logger_name cannot be empty or only whitespace.")

        if logger_name == "root":
            raise LimitationError(
                "logger_name='root' is not allowed because pyloggi would modify "
                "the Python root logger."
            )

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
            raise InvalidConstructionMode(
                "Invalid construction_mode. Use 'default', 'dev', or 'test'."
            )

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
        """Attach development handlers, optionally raising the level to DEBUG."""

        if self._config.allow_auto_level_construction:
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
        """Attach test handlers, optionally switching to WARNING file-only output."""

        if self._config.allow_auto_level_construction:
            self._config.logging_level = "WARNING"
            self.logger.setLevel(logging.WARNING)
            self._config.log_file_path = (
                Path(self._config.log_file_path).parent / "test_log.txt"
            )
        if self._config.allow_auto_level_construction:
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
    """Create a pyloggi logger and return the underlying ``logging.Logger``."""

    log = Log(
        logger_name=name,
        config=config or Config(),
        color_config=color_config or ColorConfig(),
        allow_duplicates=allow_duplicates,
    )
    return log.logger
