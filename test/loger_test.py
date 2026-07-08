import pytest

from pyloggi import Log
from pyloggi import DuplicateLogger


def test_duplicate_logger():
    logger_name = "log1"

    Log(logger_name=logger_name)

    with pytest.raises(DuplicateLogger):
        Log(logger_name=logger_name)

