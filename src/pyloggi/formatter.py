from typing import Any
import logging
from .config import ColorConfig


class CustomFormatter(logging.Formatter):
    def __init__(self, log_format: str, color_config: ColorConfig) -> None:
        self.color_config = color_config
        self.RESET = "\x1b[37;20m"

        self.log_format = log_format

        self.LEVEL_COLORS = {
        logging.DEBUG: self.color_config.debug + log_format + self.RESET,
        logging.INFO: self.color_config.info + log_format + self.RESET,
        logging.WARNING: self.color_config.warning + log_format + self.RESET,
        logging.ERROR: self.color_config.error + log_format + self.RESET,
        logging.CRITICAL: self.color_config.critical + log_format + self.RESET
        }

    def format(self, record: Any):
        format_str = self.LEVEL_COLORS.get(record.levelno, self.log_format)
        formatter = logging.Formatter(format_str, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


