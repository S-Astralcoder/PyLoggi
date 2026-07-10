from pydantic import ValidationError
import pytest


from pyloggi.config import ColorConfig, Config
from pyloggi.exceptions import InvalidFileType, InvalidFormat


@pytest.mark.parametrize(("file_path"), ["src/", "src/te.xt"])
def test_invalid_file(file_path: str):
    with pytest.raises(InvalidFileType):
        Config(log_file_path=file_path)


@pytest.mark.parametrize(("file_path"), ["sr/text.txt", "w/te.txt"])
def test_invalid_file_path(file_path: str):
    with pytest.raises(FileNotFoundError):
        Config(log_file_path=file_path)


@pytest.mark.parametrize(("mode"), ["mark", "admin"])
def test_invalid_construction_mode(mode: str):
    with pytest.raises(ValidationError):
        Config(construction_mode=mode)


@pytest.mark.parametrize(
    ("console_mode", "file_mode"), [("mark", True), (True, "admin")]
)
def test_invalid_logging_bool(console_mode: bool, file_mode: bool):
    with pytest.raises(ValidationError):
        Config(console_logging=console_mode, file_logging=file_mode)


@pytest.mark.parametrize(("level"), ["test", "mark"])
def test_logging_level(level: str):
    with pytest.raises(ValidationError):
        Config(logging_level=level)


@pytest.mark.parametrize(("color"), ["lonna", "london"])
def test_unknown_color(color: str):
    with pytest.raises(ValidationError):
        ColorConfig(
            enabled_console_color=True,
            debug=color,
            info=color,
            warning=color,
            error=color,
            critical=color,
        )


@pytest.mark.parametrize(("value"), ["lonna", "london"])
def test_invalid_color_toggle(value: bool):
    with pytest.raises(ValidationError):
        ColorConfig(enabled_console_color=value)


@pytest.mark.parametrize(("formats"), [])
def test_invalid_format(formats : str):
    with pytest.raises(InvalidFormat):
        Config(log_format=formats, construction_mode="test")


def test_invalid_date_format():
    with pytest.raises(InvalidFormat):
        Config(date_format="%q")
