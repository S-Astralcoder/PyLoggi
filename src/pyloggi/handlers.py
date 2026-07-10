"""Logging handler builders used by pyloggi."""

import logging

from .config import ColorConfig, Config
from .formatter import CustomFormatter


class ConsoleHandler:
    """Create and expose a configured console logging handler."""

    def __init__(self, config: Config, color_config: ColorConfig) -> None:
        """Store configuration and initialize the console handler."""

        self._config = config
        self._color_config = color_config
        self.handler = self._setup_console_handler()

    def _setup_console_handler(self) -> logging.Handler:
        """Create a stream handler with plain or colorized formatting."""

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self._config.logging_level)
        if self._color_config.enabled_console_color:
            console_handler.setFormatter(
                CustomFormatter(
                    log_format=self._config.log_format,
                    config=self._config,
                    color_config=self._color_config,
                )
            )
        else:
            console_handler.setFormatter(
                logging.Formatter(
                    fmt=self._config.log_format, datefmt=self._config.date_format
                )
            )
        return console_handler

    def get_console_handler(self) -> logging.Handler:
        """Return the configured logging handler."""

        return self.handler


class FileHandler(ConsoleHandler):
    """Create and expose a configured file logging handler."""

    def __init__(self, config: Config, color_config: ColorConfig) -> None:
        """Initialize file logging with the same configuration interface."""

        super().__init__(config=config, color_config=color_config)

    def _setup_console_handler(self) -> logging.FileHandler:
        """Create a file handler that writes plain text log records."""

        file_handler = logging.FileHandler(filename=self._config.log_file_path)
        file_handler.setLevel(self._config.logging_level)
        file_handler.setFormatter(
            logging.Formatter(
                fmt=self._config.log_format, datefmt=self._config.date_format
            )
        )
        return file_handler
