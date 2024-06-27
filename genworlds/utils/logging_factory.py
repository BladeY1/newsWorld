import logging
import os
import colorlog
from dotenv import load_dotenv

load_dotenv("/home/newsworld/newsagents/.env")

class LoggingFactory:
    colors = ["red", "yellow", "blue", "purple", "cyan", "green", "white"]
    color_index = 0
    loggers = {}

    @classmethod
    def get_logger(cls, name, level=None):
        # If a logger with this name already exists, return it
        if name in cls.loggers:
            return cls.loggers[name]

        # Create a handler for the logger
        handler = colorlog.StreamHandler()
        handler.setFormatter(
            colorlog.ColoredFormatter(
                # f'%(log_color)s%(levelname)-8s%(reset)s %({cls.colors[cls.color_index]})s[%(name)s] %(message)s'
                f"%({cls.colors[cls.color_index]})s[%(name)s] %(message)s"
            )
        )

        # Create a logger
        logger = colorlog.getLogger(name)
        logger.addHandler(handler)

        # Set the logging level
        if level == None:
            level = os.getenv("LOGGING_LEVEL", logging.INFO)
        logger.setLevel(level)
        logger.debug(f"Created logger {name} with level {logger.level}")

        # Cache the logger instance
        cls.loggers[name] = logger

        # Update color index for next logger
        cls.color_index = (cls.color_index + 1) % len(cls.colors)

        return logger
    

class LoggingFile:
    loggers = {}

    @classmethod
    def get_logger(cls, name, level=None):
        if name in cls.loggers:
            return cls.loggers[name]

        logger = logging.getLogger(name)
        logger.propagate = False  # Prevent the log messages from being propagated to the root logger

        log_file_path = os.getenv("LOGGING_PATH", "/home/newsworld/newsagents/log/app.log")
        file_handler = logging.FileHandler(log_file_path)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        if not logger.hasHandlers():
            logger.addHandler(file_handler)

        if level is None:
            level = os.getenv("LOGGING_LEVEL", logging.INFO)
        logger.setLevel(level)

        cls.loggers[name] = logger

        return logger
