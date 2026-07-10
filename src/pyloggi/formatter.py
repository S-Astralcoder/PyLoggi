"""Formatter support for colorized console log output."""

from typing import Any
import logging

from pyloggi.exceptions import InvalidConfigure
from .config import ColorConfig, Config


class CustomFormatter(logging.Formatter):
    """Apply log-level-specific ANSI colors to formatted console records."""

    def __init__(
        self, log_format: str, config: Config, color_config: ColorConfig
    ) -> None:
        """Build a formatter map for each standard logging level."""

        self.validate_parameters(color_config=color_config)
        self._color_config = color_config
        self.RESET = "\x1b[37;20m"

        self._log_format = log_format
        self._date_format = config.date_format

        self.LEVEL_COLORS = {
            logging.DEBUG: self._color_config.debug + log_format + self.RESET,
            logging.INFO: self._color_config.info + log_format + self.RESET,
            logging.WARNING: self._color_config.warning + log_format + self.RESET,
            logging.ERROR: self._color_config.error + log_format + self.RESET,
            logging.CRITICAL: self._color_config.critical + log_format + self.RESET,
        }

    def validate_parameters(self, color_config: object):
        """Ensure the formatter receives a valid color configuration."""

        if not isinstance(color_config, ColorConfig):
            raise InvalidConfigure("Invalid ColorConfig passed as a parameter")

    def format(self, record: Any):
        """Format a log record with the color assigned to its level."""

        format_str = self.LEVEL_COLORS.get(record.levelno, self._log_format)
        formatter = logging.Formatter(format_str, datefmt=self._date_format)
        return formatter.format(record)
