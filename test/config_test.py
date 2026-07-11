from pydantic import ValidationError
import pytest


from pyloggi.config import ColorConfig, Config
from pyloggi.exceptions import InvalidFileType, InvalidFormat


@pytest.mark.parametrize(("file_path"), ["src/", "src/te.xt"])
# @pytest.mark.xfail(reason="Current Config behavior does not raise InvalidFileType")
def test_invalid_file(file_path: str):
    with pytest.raises(InvalidFileType):
        Config(log_file_path=file_path, file_logging=True)


@pytest.mark.parametrize(("file_path"), ["sr/text.txt", "w/te.txt"])
# @pytest.mark.xfail(reason="Current Config behavior does not raise FileNotFoundError")
def test_invalid_file_path(file_path: str):
    with pytest.raises(FileNotFoundError):
        Config(log_file_path=file_path, file_logging=True)


@pytest.mark.parametrize(("mode"), ["mark", "admin"])
def test_invalid_construction_mode(mode: str):
    with pytest.raises(ValidationError):
        Config(construction_mode=mode) # pyright: ignore[reportArgumentType]


@pytest.mark.parametrize(
    ("console_mode", "file_mode"), [("mark", True), (True, "admin")]
)
def test_invalid_logging_bool(console_mode: bool, file_mode: bool):
    with pytest.raises(ValidationError):
        Config(console_logging=console_mode, file_logging=file_mode)


@pytest.mark.parametrize(("level"), ["test", "mark"])
def test_logging_level(level: str):
    with pytest.raises(ValidationError):
        Config(logging_level=level) # pyright: ignore[reportArgumentType]


@pytest.mark.parametrize(("color"), ["lonna", "london"])
def test_unknown_color(color: str): 
    with pytest.raises(ValidationError):
        ColorConfig(
            enabled_console_color=True,
            debug=color,# pyright: ignore[reportArgumentType]
            info=color,# pyright: ignore[reportArgumentType]
            warning=color,# pyright: ignore[reportArgumentType]
            error=color,# pyright: ignore[reportArgumentType]
            critical=color,# pyright: ignore[reportArgumentType]
        )


@pytest.mark.parametrize(("value"), ["lonna", "london"])
def test_invalid_color_toggle(value: bool):
    with pytest.raises(ValidationError):
        ColorConfig(enabled_console_color=value)


@pytest.mark.parametrize(
    ("formats"),
    [
        "%(test)s",
        "%(bad)d",
        "%(message)s %(bad)d",
        "%(message",
        "%(message)",
        "%(message)q",
        "%(message)s %",
        "%(message)s %q",
        "%(message)s %(bad)",
        "plain text with no fields",
    ],
)
def test_invalid_format(formats: str):
    with pytest.raises(InvalidFormat):
        Config(log_format=formats, construction_mode="test")


def test_invalid_date_format():
    with pytest.raises(InvalidFormat):
        Config(date_format="%q")
