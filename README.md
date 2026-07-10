# pyloggi

pyloggi is a small convenience layer over Python's built-in `logging` module.
It creates ready-to-use named loggers with validated configuration, optional
console colors, file logging, and preset construction modes for common
development and test workflows.

The package is intentionally simple: create a `Config`, create a `ColorConfig`,
pass both into `Log`, then use the standard `logging.Logger` available at
`logger.logger`.

## Quick Start

```python
from pyloggi import Log
from pyloggi.config import Config, ColorConfig

log = Log(
    logger_name="app",
    config=Config(),
    color_config=ColorConfig(),
)

log.logger.info("Application started")
log.logger.warning("Something needs attention")
```

By default, pyloggi logs to the console with this format:

```text
[%(asctime)s] : %(levelname)s - %(name)s > %(message)s
```

## Console and File Logging

Console logging is enabled by default. File logging is disabled by default.

```python
from pathlib import Path

from pyloggi import Log
from pyloggi.config import Config, ColorConfig

log = Log(
    logger_name="file-example",
    config=Config(
        console_logging=True,
        file_logging=True,
        log_file_path=Path("log.txt"),
    ),
    color_config=ColorConfig(),
)

log.logger.info("This message goes to the console and log.txt")
```

`log_file_path` must point to an existing folder and must use a supported file
extension:

- `.txt`
- `.rtf`

## Configuration

Use `Config` to control logger behavior.

```python
Config(
    construction_mode="default",
    disable_auto_level_construction=False,
    console_logging=True,
    file_logging=False,
    log_format="[%(asctime)s] : %(levelname)s - %(name)s > %(message)s",
    date_format="%Y-%m-%d %H:%M:%S",
    logging_level="INFO",
    log_file_path="log.txt",
)
```

### Construction Modes

`construction_mode` controls how pyloggi prepares the logger.

| Mode | Behavior |
| --- | --- |
| `"default"` | Uses your `Config` values exactly as provided. |
| `"dev"` | Sets the logger level to `DEBUG` unless automatic construction is disabled. |
| `"test"` | Sets the logger level to `WARNING`, disables console logging, enables file logging, and writes to `test_log.txt` unless automatic construction is disabled. |

The automatic behavior is intentional. pyloggi is designed to speed up common
logging setup. If you want full manual control, set:

```python
Config(
    construction_mode="dev",
    disable_auto_level_construction=True,
    logging_level="INFO",
)
```

### Logging Levels

`logging_level` accepts:

- `"NOTSET"`
- `"DEBUG"`
- `"INFO"`
- `"WARNING"`
- `"ERROR"`
- `"CRITICAL"`

## Log Format

`log_format` uses standard `logging.Formatter` placeholder style, but pyloggi
validates it strictly before the logger is created.

Supported fields:

- `%(name)s`
- `%(levelno)s`
- `%(levelname)s`
- `%(pathname)s`
- `%(filename)s`
- `%(module)s`
- `%(funcName)s`
- `%(asctime)s`
- `%(threadName)s`
- `%(taskName)s`
- `%(processName)s`
- `%(message)s`

Example:

```python
Config(
    log_format="%(levelname)s | %(name)s | %(message)s",
)
```

Invalid or unsupported formats raise `InvalidFormat`. Examples include unknown
fields, unsupported conversion types, incomplete percent syntax, and plain text
with no logging fields.

## Date Format

`date_format` uses Python `strftime` tokens.

```python
Config(
    date_format="%Y-%m-%dT%H:%M:%S%z",
)
```

Invalid date-format tokens raise `InvalidFormat`.

## Console Colors

Use `ColorConfig` to enable ANSI-colored console output by log level.

```python
from pyloggi.config import ColorConfig

colors = ColorConfig(
    enabled_console_color=True,
    debug="cyan",
    info="green",
    warning="yellow",
    error="red",
    critical="dark red",
)
```

Supported color names:

- `black`
- `red`
- `dark red`
- `green`
- `dark green`
- `yellow`
- `dark yellow`
- `blue`
- `dark blue`
- `magenta`
- `dark magenta`
- `cyan`
- `dark cyan`
- `white`
- `gray`
- `light red`
- `light green`
- `light yellow`
- `light blue`
- `light magenta`
- `light cyan`

File logs are not colorized. Colors are only applied to console output.

## Duplicate Logger Names

pyloggi tracks logger names created through `Log`. Duplicate names are rejected
by default to avoid accidental handler replacement or reconfiguration.

```python
from pyloggi import Log
from pyloggi.config import Config, ColorConfig

Log("app", Config(), ColorConfig())

# Raises DuplicateLogger
Log("app", Config(), ColorConfig())
```

If you intentionally want to recreate or reconfigure the same logger name, pass
`allow_duplicates=True`.

```python
Log("app", Config(), ColorConfig(), allow_duplicates=True)
```

Empty names and the literal `"root"` logger name are rejected. This protects the
root logger from being cleared or reconfigured accidentally.

## Exceptions

pyloggi raises custom exceptions for common configuration errors:

| Exception | Meaning |
| --- | --- |
| `DuplicateLogger` | A logger name was reused without `allow_duplicates=True`. |
| `EmptyLoggerName` | The logger name was empty or whitespace-only. |
| `LimitationError` | A blocked option was requested, such as using `"root"` as the logger name. |
| `InvalidConfigure` | `Log` or `CustomFormatter` received the wrong configuration object type. |
| `InvalidConstructionMode` | An unsupported construction mode was requested. |
| `InvalidFileType` | The configured log file extension is not supported. |
| `InvalidFormat` | The log or date format is invalid. |

## Intended Design

The project design, based on the to-do list, is:

- Provide an initial package structure for a focused logging helper.
- Use `Config` as the single place for logger behavior and validation.
- Use `ColorConfig` as the single place for console color choices.
- Build a main `Log` class that creates and exposes a standard
  `logging.Logger`.
- Provide separate console and file handler builders.
- Validate edge cases early, including invalid logger names, invalid file paths,
  bad log formats, bad date formats, duplicate loggers, and accidental root
  logger use.
- Keep automatic construction modes because they are part of the package's
  convenience goal, while allowing callers to disable automatic mode changes
  when they need manual control.

## Development Checks

The current verification commands are:

```bash
uv run pytest
uv run ruff check .
uv run pyright
```

At the time this documentation was written, tests and Ruff pass. Pyright reports
errors in negative tests that intentionally pass invalid runtime values to check
Pydantic and custom validation behavior.
