class DuplicateLogger(Exception):
    def __init__(self, logger_name: str) -> None:
        super().__init__(f"Logger {logger_name} Already Exists")
