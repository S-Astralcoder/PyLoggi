"""Configuration models and validation rules for pyloggi loggers.

``Config`` validates logger behavior before handlers are created. ``ColorConfig``
validates color names and converts them to ANSI escape sequences used by the
console formatter.
"""

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
    """Runtime configuration for console and file logging.

    File path validation runs only when file logging is enabled. Log and date
    formats are always validated so invalid formatter strings fail during
    configuration rather than later during logging. Automatic construction mode
    changes are opt in through ``allow_auto_level_construction``.
    """

    construction_mode: Literal["dev", "test", "default"] = "default"

    allow_auto_level_construction: bool = False

    console_logging: bool = True
    file_logging: bool = False

    log_format: str = "[%(asctime)s] : %(levelname)s - %(name)s > %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"

    logging_level: Literal[
        "NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ] = "INFO"

    log_file_path: str | Path = Path.cwd() / "log.txt"

    def model_post_init(self, context: Any, /) -> None:
        """Validate file, log-format, and date-format settings after parsing."""

        if self.file_logging:
            log_file_path = Path(self.log_file_path)
            folder_path = (
                log_file_path if log_file_path.is_dir() else log_file_path.parent
            )
            if log_file_path.suffix not in (".txt", ".rtf"):
                raise InvalidFileType(
                    "Unsupported log file extension "
                    f"{log_file_path.suffix!r}. Use '.txt' or '.rtf'."
                )
            if not folder_path.exists():
                raise FileNotFoundError(
                    f"Log file directory does not exist: {folder_path}"
                )

        format_tags = regex.findall(r"(?<=%[\(%])\w+", self.log_format)
        # Accept only known logging fields and reject malformed percent patterns.
        if (
            not all([format in valid_formats for format in format_tags])
            or not format_tags
            or regex.findall(r"%(?![%(])[^s]*?(?:s(?!$)|[^s])?", self.log_format)
        ):
            raise InvalidFormat(
                "Invalid log_format. Use at least one supported field such as "
                "'%(message)s', and use only simple '%(field)s' placeholders."
            )
        for tags in format_tags:
            validation_pattern = rf"%[\(%]{tags}\)s"
            if not regex.search(validation_pattern, self.log_format):
                raise InvalidFormat(
                    f"Invalid log_format placeholder for {tags!r}. "
                    "Use the exact form '%(field)s'."
                )

        date_format_tags = regex.findall("%(.)", self.date_format)
        # Keep date formatting limited to strftime tokens supported by Python.
        if not all(
            [
                format
                in "Y m d H M S I p a A b B j U W w w f u V G X x c Z z %".split(" ")
                for format in date_format_tags
            ]
        ):
            raise InvalidFormat(
                "Invalid date_format. Use supported Python strftime tokens "
                "such as '%Y', '%m', '%d', '%H', '%M', and '%S'."
            )


class ColorConfig(BaseModel):
    """Color choices for console output by log level.

    Pydantic validates the configured color names. After validation, each color
    field stores the ANSI escape sequence used by ``CustomFormatter``.
    """

    enabled_console_color: bool = False

    debug: ColorName = "cyan"
    info: ColorName = "green"
    warning: ColorName = "yellow"
    error: ColorName = "red"
    critical: ColorName = "dark red"

    def model_post_init(self, context: Any, /) -> None:
        """Convert configured color names into ANSI escape sequences."""

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
