import pytest

from pyloggi import Log
from pyloggi import DuplicateLogger
from pyloggi.config import Config
from pyloggi.exceptions import InvalidConfigure, InvalidFormat


@pytest.fixture
def default_logger():
    return Log("test")


def test_duplicate_logger():
    logger_name = "log1"

    Log(logger_name=logger_name)

    with pytest.raises(DuplicateLogger):
        Log(logger_name=logger_name)


def test_invalid_name_parameters():
    with pytest.raises(TypeError):
        Log(10)


def test_invalid_config_parameter():
    with pytest.raises(InvalidConfigure):
        Log("name", "test", "test")


def test_invalid_format():
    with pytest.raises(InvalidFormat):
        Log("test", Config(log_format="%(test)s", construction_mode="test"))
