""" Logger module. """
from typing import Any
import logging


class Logger:
    """ Logger class. """

    @staticmethod
    def get_logger() -> Any:
        """ Get logger. """
        return logging

    @staticmethod
    def init_logger(log_level: str) -> None:
        """ Configures the logger. """
        logging_levels = {
            "critical": logging.CRITICAL,
            "error": logging.ERROR,
            "warning": logging.WARNING,
            "info": logging.INFO,
            "debug": logging.DEBUG,
            "none": logging.NOTSET,
        }
        if log_level is None:
            log_level = "warning"

        # TODO use a separate logger.
        logging.basicConfig(level=logging_levels[log_level])
