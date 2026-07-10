"""Custom exceptions raised by pyloggi."""


class DuplicateLogger(Exception):
    """Raised when a logger name is reused without duplicate support enabled."""

    def __init__(self, logger_name: str) -> None:
        super().__init__(f"Logger {logger_name} Already Exists")


class InvalidConstructionMode(Exception):
    """Raised when an unsupported logger construction mode is requested."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidFileType(Exception):
    """Raised when the configured log file extension is not supported."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidConfigure(Exception):
    """Raised when a configuration object has the wrong type."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidFormat(Exception):
    """Raised when a log or date format string is not valid."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class EmptyLoggerName(Exception):
    """Raised when a logger name is empty or only whitespace."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class LimitationError(Exception):
    """Raised when a requested option is intentionally not supported."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
