import logging
import os
import sys

import coloredlogs

FORMATTER = logging.Formatter()


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    return console_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)

    log_level = os.getenv('LOGLEVEL') if os.getenv('LOGLEVEL') else 'INFO'

    coloredlogs.install(fmt="[%(asctime)s] [%(levelname)s] — %(name)s: %(message)s", level=log_level, logger=logger)

    return logger
