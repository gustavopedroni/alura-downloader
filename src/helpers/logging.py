import logging
import sys

import coloredlogs

FORMATTER = logging.Formatter()


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    return console_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    coloredlogs.install(fmt="[%(asctime)s] [%(levelname)s] — %(name)s: %(message)s", level='INFO', logger=logger)

    return logger
