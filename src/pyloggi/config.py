from pydantic import BaseModel
from typing import Literal
from pathlib import Path

class Config(BaseModel):
    construction_mode: Literal["dev", "test", "default"] = "default"

    console_logging: bool = True
    file_logging: bool = False

    logging_level: Literal["NOTSET" ,"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    log_file_path : str | Path = Path.cwd()
