from pydantic import BaseModel
from typing import Any, Literal
from pathlib import Path

from .exceptions import InvalidFileType, InvalidFormat
import regex

ColorName = Literal[
    "black",
    "red",
    "dark red",
    "green",
    "dark green",
    "yellow",
    "dark yellow",
    "blue",
    "dark blue",
    "magenta",
    "dark magenta",
    "cyan",
    "dark cyan",
    "white",
    "gray",
    "light red",
    "light green",
    "light yellow",
    "light blue",
    "light magenta",
    "light cyan",
]

valid_formats = [
    "name",
    "levelno",
    "levelname",
    "pathname",
    "filename",
    "module",
    "funcName",
    "asctime",
    "threadName",
    "taskName",
    "processName",
    "message",
]


class Config(BaseModel):
    construction_mode: Literal["dev", "test", "default"] = "default"

    console_logging: bool = True
    file_logging: bool = False

    log_format: str = "[%(asctime)s] : %(levelname)s - %(name)s > %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"

    logging_level: Literal[
        "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ] = "INFO"

    log_file_path: str | Path = Path.cwd() / "log.txt"

    def model_post_init(self, context: Any, /) -> None:
        log_file_path = Path(self.log_file_path)
        folder_path = log_file_path if log_file_path.is_dir() else log_file_path.parent
        if log_file_path.suffix not in (".txt", ".rtf"):
            raise InvalidFileType(
                f"The Give File Name [{log_file_path.suffix}] Is Invalid"
            )
        if not folder_path.exists():
            raise FileNotFoundError("The Give File Path doesn't Exist")

        format_tags = regex.findall(r"%\((.*?)\)s", self.log_format)
        if not all([format in valid_formats for format in format_tags]):
            raise InvalidFormat("The Give Log Format is Invalid")

        date_format_tags = regex.findall("%(.)", self.date_format)
        if not all([format in "H M S Y m d".split(" ") for format in date_format_tags]):
            raise InvalidFormat("The Give Date Format is Invalid")


class ColorConfig(BaseModel):
    enabled_console_color: bool = False

    debug: ColorName = "cyan"
    info: ColorName = "green"
    warning: ColorName = "yellow"
    error: ColorName = "red"
    critical: ColorName = "dark red"

    def model_post_init(self, context: Any, /) -> None:

        color_map = {
            "black": "\x1b[30;20m",
            "red": "\x1b[31;20m",
            "dark red": "\x1b[31;1m",
            "green": "\x1b[32;20m",
            "dark green": "\x1b[32;1m",
            "yellow": "\x1b[33;20m",
            "dark yellow": "\x1b[33;1m",
            "blue": "\x1b[34;20m",
            "dark blue": "\x1b[34;1m",
            "magenta": "\x1b[35;20m",
            "dark magenta": "\x1b[35;1m",
            "cyan": "\x1b[36;20m",
            "dark cyan": "\x1b[36;1m",
            "white": "\x1b[37;20m",
            "gray": "\x1b[37;2m",
            "light red": "\x1b[91;20m",
            "light green": "\x1b[92;20m",
            "light yellow": "\x1b[93;20m",
            "light blue": "\x1b[94;20m",
            "light magenta": "\x1b[95;20m",
            "light cyan": "\x1b[96;20m",
        }

        default = "\x1b[37;20m"
        for level in ("debug", "info", "warning", "error", "critical"):
            color = getattr(self, level)
            object.__setattr__(self, level, color_map.get(color, default))
