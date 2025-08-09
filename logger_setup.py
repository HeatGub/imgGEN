import logging
from logging.handlers import RotatingFileHandler
import config
import sys

class ColorFormatter(logging.Formatter):
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[41m',  # Red background
    }
    RESET = '\033[0m'

    def format(self, record):
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.RESET}"
        return super().format(record)


def setup_logging():
    # File formatter
    file_formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(funcName)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Color console formatter
    console_formatter = ColorFormatter(
        fmt="%(asctime)s %(levelname)s [%(funcName)s] %(message)s",
        datefmt="%H:%M:%S"
    )

    # Rotating file handler (10 MB per file, keep 3 backups)
    file_handler = RotatingFileHandler("logs.log", maxBytes=10_000_000, backupCount=3) # keeps 3 last files up to 10mb
    file_handler.setLevel(config.LOGGING_LEVEL_FILE)
    file_handler.setFormatter(file_formatter)

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(config.LOGGING_LEVEL_CONSOLE)
    console_handler.setFormatter(console_formatter)

    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG) # global gatekeeper
    root_logger.handlers = []  # Clear existing handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)



# def setup_logging(level=logging.INFO):
#     # Define formatter
#     formatter = logging.Formatter(
#         fmt="%(asctime)s %(levelname)s [%(name)s.%(funcName)s] %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S"
#     )

#     # File handler
#     file_handler = logging.FileHandler("logs.log")
#     file_handler.setLevel(level)
#     file_handler.setFormatter(formatter)

#     # Console handler
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_handler.setLevel(level)
#     console_handler.setFormatter(formatter)

#     # Get root logger and clear previous handlers
#     root_logger = logging.getLogger()
#     root_logger.setLevel(level)
#     root_logger.handlers = []  # Clear existing handlers to avoid duplicates
#     root_logger.addHandler(file_handler)
#     root_logger.addHandler(console_handler)

# def setup_logging(level = logging.ERROR):
#     logging.basicConfig(
#         filename="logs.log",
#         level=level,
#         format="%(asctime)s %(levelname)s [%(name)s.%(funcName)s] %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S",
#     )