"""
Module for initializing the goodGirlBot logger.

This module sets up console and file handlers for the logger.
"""

import logging
import sys

logger = logging.Logger("goodGirlBot", level=logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

file_handler = logging.FileHandler("goodGirlBot.log")
file_handler.setLevel(logging.DEBUG)  # changed from logging.INFO to logging.DEBUG
file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
file_handler.addFilter(lambda record: record.levelno <= logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)


logger.setLevel(logging.DEBUG)

def _get_logger():
    """
    Return the logger instance for goodGirlBot.

    Returns
    -------
    logging.Logger
        The logger instance.
    """
    return logger