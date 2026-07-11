"""Handler builders used by pyloggi.

Each builder creates one configured ``logging.Handler`` and exposes it through
``get_handler()`` so ``Log`` can attach console and file handlers uniformly.
"""

import logging


from .config import ColorConfig, Config
from .formatter import CustomFormatter


class BaseHandler:
    """Base class for handler builders that share configuration storage."""

    def __init__(self, config: Config, color_config: ColorConfig) -> None:
        """Store configuration and build the concrete logging handler."""

        self._config = config
        self._color_config = color_config
        self.handler = self._setup_handler()

    def _setup_handler(self) -> logging.Handler:
        """Create the concrete handler for a subclass."""

        raise NotImplementedError(
            f"{self.__class__.__name__} must implement _setup_handler()."
        )

    def get_handler(self) -> logging.Handler:
        """Return the configured logging handler."""

        return self.handler


class ConsoleHandler(BaseHandler):
    """Build a stream handler for console logging."""

    def __init__(self, config: Config, color_config: ColorConfig) -> None:
        """Create a console handler from pyloggi configuration."""
        super().__init__(config=config, color_config=color_config)

    def _setup_handler(self) -> logging.Handler:
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


class FileHandler(BaseHandler):
    """Build a file handler for plain text log output."""

    def __init__(self, config: Config, color_config: ColorConfig) -> None:
        """Create a file handler from pyloggi configuration."""
        super().__init__(config=config, color_config=color_config)

    def _setup_handler(self) -> logging.FileHandler:
        """Create a file handler that writes plain text log records."""

        file_handler = logging.FileHandler(filename=self._config.log_file_path)
        file_handler.setLevel(self._config.logging_level)
        file_handler.setFormatter(
            logging.Formatter(
                fmt=self._config.log_format, datefmt=self._config.date_format
            )
        )
        return file_handler
