import logging

from .config import ColorConfig, Config
from .formatter import CustomFormatter


class ConsoleHandler:
    def __init__(self, config: Config, color_config: ColorConfig) -> None:
        self._config = config
        self._color_config = color_config
        self.handler = self._setup_console_handler()

    def _setup_console_handler(self) -> logging.Handler:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self._config.logging_level)
        if self._color_config.enabled_console_color:
            console_handler.setFormatter(
                CustomFormatter(
                    log_format=self._config.log_format,
                    date_format=self._config.date_format,
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
        return self.handler


class FileHandler(ConsoleHandler):
    def __init__(self, config: Config, color_config: ColorConfig) -> None:
        super().__init__(config=config, color_config=color_config)

    def _setup_console_handler(self) -> logging.FileHandler:
        file_handler = logging.FileHandler(filename=self._config.log_file_path)
        file_handler.setLevel(self._config.logging_level)
        file_handler.setFormatter(
            logging.Formatter(
                fmt=self._config.log_format, datefmt=self._config.date_format
            )
        )
        return file_handler
