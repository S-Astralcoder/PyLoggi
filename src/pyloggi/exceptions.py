class DuplicateLogger(Exception):
    def __init__(self, logger_name: str) -> None:
        super().__init__(f"Logger {logger_name} Already Exists")


class InvalidConstructionMode(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidFileType(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class InvalidConfigure(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)