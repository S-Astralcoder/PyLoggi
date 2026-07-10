if __name__ == "__main__":
    from pyloggi import Log
    from pyloggi.config import ColorConfig, Config

    logger = Log(
        "main",
        color_config=ColorConfig(enabled_console_color=False, info="light blue"),
        config=Config(file_logging=True, construction_mode="default"),
    )

    logger.logger.debug("debug")
    logger.logger.info("info")
    logger.logger.warning("warning")
    logger.logger.error("error")
    logger.logger.critical("critical")
