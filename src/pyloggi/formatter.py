from typing import Any
import logging
from .config import ColorConfig


class CustomFormatter(logging.Formatter):
    def __init__(
        self, log_format: str, date_format: str, color_config: ColorConfig
    ) -> None:
        self._color_config = color_config
        self.RESET = "\x1b[37;20m"

        self._log_format = log_format
        self._date_format = date_format

        self.LEVEL_COLORS = {
            logging.DEBUG: self._color_config.debug + log_format + self.RESET,
            logging.INFO: self._color_config.info + log_format + self.RESET,
            logging.WARNING: self._color_config.warning + log_format + self.RESET,
            logging.ERROR: self._color_config.error + log_format + self.RESET,
            logging.CRITICAL: self._color_config.critical + log_format + self.RESET,
        }

    def format(self, record: Any):
        format_str = self.LEVEL_COLORS.get(record.levelno, self._log_format)
        formatter = logging.Formatter(format_str, datefmt=self._date_format)
        return formatter.format(record)
