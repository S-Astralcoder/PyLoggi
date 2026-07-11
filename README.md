# pyloggi

pyloggi is a small convenience layer over Python's built-in `logging` module.
It creates ready-to-use named loggers with validated configuration, optional
console colors, file logging, controlled duplicate-name handling, and preset
construction modes for common development and test workflows.

The package is intentionally simple: create a `Config`, create a `ColorConfig`,
pass both into `Log`, then use the standard `logging.Logger` available at
`logger.logger`. For simpler code, use `get_logger()` to create and return the
standard logger directly.

pyloggi validates setup early and returns clear errors for common mistakes, such
as invalid logger names, unsupported file extensions, missing log directories,
bad format strings, and duplicate logger names.

## Requirements

pyloggi requires Python 3.12 or newer.

Runtime dependencies:

- `pydantic`
- `regex`

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

You can also use `get_logger()` when you only need the standard
`logging.Logger` object:

```python
from pyloggi.log import get_logger

logger = get_logger("app")

logger.info("Application started")
```

By default, pyloggi logs to the console with this format:

```text
[%(asctime)s] : %(levelname)s - %(name)s > %(message)s
```

## Console and File Logging

Console logging is enabled by default. File logging is disabled by default.

`log_file_path` is validated only when `file_logging=True`. This lets you create
console-only loggers without needing a valid file path.

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

When file logging is enabled, `log_file_path` must point to an existing folder
and must use a supported file extension:

- `.txt`
- `.rtf`

File output is covered by the test suite. The file handler stores a real
`logging.FileHandler`, so messages are written to the configured file when
`file_logging=True`.

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
| `"test"` | Sets the logger level to `WARNING`, disables console logging, enables file logging, and changes the configured path to `test_log.txt` unless automatic construction is disabled. |

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

Error messages point to the failing setting. For example, an invalid log format
explains that pyloggi supports simple `%(field)s` placeholders such as
`%(message)s`.

## Date Format

`date_format` uses Python `strftime` tokens.

```python
Config(
    date_format="%Y-%m-%dT%H:%M:%S%z",
)
```

Invalid date-format tokens raise `InvalidFormat`.

When the date format is invalid, the error message recommends supported Python
`strftime` tokens such as `%Y`, `%m`, `%d`, `%H`, `%M`, and `%S`.

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

pyloggi tracks logger names created through `Log` in `Log.active_loggers`.
Logger names are stripped before they are stored, so `" app "` is registered as
`"app"`. Duplicate names are rejected by default to avoid accidental handler
replacement or reconfiguration.

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

You can inspect registered logger names with:

```python
from pyloggi import Log

print(Log.get_active_loggers())
```

## Exceptions

pyloggi raises custom exceptions for common configuration errors:

| Exception | Meaning |
| --- | --- |
| `DuplicateLogger` | A logger name was reused without `allow_duplicates=True`; the error message includes the duplicated name. |
| `EmptyLoggerName` | The logger name was empty or whitespace-only. |
| `LimitationError` | A blocked option was requested, such as using `"root"` as the logger name. |
| `InvalidConfigure` | `Log` or `CustomFormatter` received the wrong configuration object type. |
| `InvalidConstructionMode` | An unsupported construction mode was requested; use `"default"`, `"dev"`, or `"test"`. |
| `InvalidFileType` | The configured log file extension is not supported; use `.txt` or `.rtf`. |
| `InvalidFormat` | The log or date format is invalid, with feedback about the expected format style. |

pyloggi also uses standard Python exceptions where they fit better. For example,
an internal handler subclass that does not implement `_setup_handler()` raises
`NotImplementedError`.

## Error Feedback

pyloggi tries to fail at configuration time instead of failing later while a log
message is being written.

Common feedback examples:

- `logger_name must be a string, got int.`
- `logger_name cannot be empty or only whitespace.`
- `logger_name='root' is not allowed because pyloggi would modify the Python root logger.`
- `config must be an instance of pyloggi.config.Config.`
- `color_config must be an instance of pyloggi.config.ColorConfig.`
- `Unsupported log file extension '.log'. Use '.txt' or '.rtf'.`
- `Log file directory does not exist: logs`
- `Invalid construction_mode. Use 'default', 'dev', or 'test'.`

## Intended Design

pyloggi is built around a few simple rules:

- Keep logger setup small and predictable.
- Keep `Config` responsible for logger behavior and validation.
- Keep `ColorConfig` responsible for console color choices.
- Expose a standard `logging.Logger` so normal Python logging methods still work.
- Build console and file handlers through separate handler classes.
- Expose handlers with a shared `get_handler()` method.
- Store `FileHandler.handler` as a real `logging.FileHandler`.
- Store active logger names in a set for direct duplicate checks.
- Strip logger names before storing them.
- Reject unsafe names such as an empty string or `"root"`.
- Validate file paths only when file logging is enabled.
- Validate format strings early so bad placeholders do not fail later.
- Keep automatic construction modes for convenience, with
  `disable_auto_level_construction=True` available when manual control matters.

## Development Checks

The current verification commands are:

```bash
uv run pytest
uv run ruff check .
uv run pyright
```

At the time this documentation was written, tests, Ruff, and Pyright pass. The
test suite contains 40 passing tests.
