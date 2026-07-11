import pytest

from pyloggi import Log
from pyloggi.config import ColorConfig, Config
from pyloggi.exceptions import InvalidConfigure, InvalidFormat, DuplicateLogger


@pytest.fixture
def default_logger():
    return Log("default", Config(), ColorConfig())


def test_duplicate_logger():
    logger_name = "log1"

    Log(logger_name=logger_name, config=Config(), color_config=ColorConfig())

    with pytest.raises(DuplicateLogger):
        Log(logger_name=logger_name, config=Config(), color_config=ColorConfig())


def test_invalid_name_parameters():
    with pytest.raises(TypeError):
        Log(10, Config(), ColorConfig())  # pyright: ignore[reportArgumentType]
    assert 10 not in Log("tester", Config(), ColorConfig()).active_loggers


def test_invalid_config_parameter():
    with pytest.raises(InvalidConfigure):
        Log("name", "test", ColorConfig())  # pyright: ignore[reportArgumentType]

    with pytest.raises(InvalidConfigure):
        Log("name", Config(), "test")  # pyright: ignore[reportArgumentType]


@pytest.mark.parametrize(
    ("log_format"),
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
def test_invalid_format(log_format: str):
    Log.active_loggers.clear()
    with pytest.raises(InvalidFormat):
        Log(
            "test",
            Config(log_format=log_format, construction_mode="test"),
            ColorConfig(),
        )


def test_custom_color_console_output(capsys):
    logger = Log(
        logger_name="color_test",
        color_config=ColorConfig(enabled_console_color=True),
        config=Config(
            log_format="%(message)s",
            construction_mode="dev",
            allow_auto_level_construction=True,
        ),
    )

    expected_logs = [
        color_code + "test\x1b[37;20m\n"
        for color_code in [
            "\x1b[36;20m",
            "\x1b[32;20m",
            "\x1b[33;20m",
            "\x1b[31;20m",
            "\x1b[31;1m",
        ]
    ]
    logger.logger.debug("test")
    capture = capsys.readouterr()
    assert capture.err in expected_logs
    logger.logger.info("test")
    capture = capsys.readouterr()
    assert capture.err in expected_logs
    logger.logger.warning("test")
    capture = capsys.readouterr()
    assert capture.err in expected_logs
    logger.logger.error("test")
    capture = capsys.readouterr()
    assert capture.err in expected_logs
    logger.logger.critical("test")
    capture = capsys.readouterr()
    assert capture.err in expected_logs


def test_file_log_output(tmp_path):  # pyright: ignore[reportUnknownParameterType]
    file_path = tmp_path / "test_log.txt"  #  pyright: ignore[reportUnknownVariableType]
    logger = Log(
        logger_name="file_log_test",
        config=Config(
            log_format="%(message)s",
            construction_mode="dev",
            log_file_path=file_path,  # pyright: ignore[reportUnknownArgumentType]
            console_logging=False,
            file_logging=True,
            allow_auto_level_construction=True,
        ),
        color_config=ColorConfig(),
    )
    logger.logger.info("test")
    logger.logger.debug("what")

    with open(file_path, "r") as file:  # pyright: ignore[reportUnknownArgumentType]
        lines = file.readlines()
        for test_string in ["test\n", "what\n"]:
            assert test_string in lines
