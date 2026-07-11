"""Project-specific exceptions raised by pyloggi.

The exception types keep validation failures explicit, so callers can catch
package errors without parsing generic ``ValueError`` or ``TypeError`` text.
"""


class DuplicateLogger(Exception):
    """Raised when a logger name is reused without duplicate support enabled."""

    def __init__(self, logger_name: str) -> None:
        super().__init__(
            f"Logger name {logger_name!r} is already registered. "
            "Use allow_duplicates=True if you want to recreate this logger."
        )


class InvalidConstructionMode(Exception):
    """Raised when a logger construction mode is not supported."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidFileType(Exception):
    """Raised when the configured log file extension is not supported."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidConfigure(Exception):
    """Raised when a pyloggi component receives the wrong configuration type."""

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
