#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-11-22
# ---------------------------------------------------------------------------
"""
A module to simplyfy customized logging to the console and to log files.
Based on original code by fonic - https://github.com/fonic
"""
# ---------------------------------------------------------------------------

__all__ = ["setup_logger"]

from typing import Union
import sys
import logging
import os
from yaml import safe_load


class CreateLoggerError(Exception):
    pass


class IncorrectSettingsError(Exception):
    pass


def get_current_directory():
    return os.path.dirname(os.path.realpath(__file__))


def load_yaml(filepath: str):
    with open(filepath, "r") as f:
        content = safe_load(f)
    return content


def load_default_settings_global(filename: str = "default_settings.yaml"):
    filepath = os.path.join(get_current_directory(), filename)
    return load_yaml(filepath)


# Logging formatter supporting colored output
class ColoredLogFormatter(logging.Formatter):
    COLOR_CODES = {
        logging.CRITICAL: "\033[1;97;41m",  # bright/bold magenta
        logging.ERROR: "\033[1;31m",  # bright/bold red
        logging.WARNING: "\033[0;33m",  # bright/bold yellow
        logging.INFO: "\033[0;37m",  # bright/bold white
        logging.DEBUG: "\033[2;37m",  # white / light gray
    }

    RESET_CODE = "\033[0m"

    def __init__(self, *args, color=True, fmt=None, datefmt=None, **kwargs):
        self.color = color
        if self.color:
            fmt = f"%(color_on)s{fmt}%(color_off)s"
        super().__init__(*args, fmt=fmt, datefmt=datefmt, **kwargs)

    def format(self, record, *args, **kwargs):
        if self.color == True and record.levelno in self.COLOR_CODES:
            record.color_on = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on = ""
            record.color_off = ""
        record.levelname2 = record.levelname.capitalize()
        return super().format(record, *args, **kwargs)


# Setup logging
# NOTE: logger_name == None -> root logger
def setup_logger(
    logger_name: str = None,
    default_handler_format: Union[logging.Formatter, ColoredLogFormatter] = None,
    handlers: list = None,
    default_settings: Union[str, dict] = None,
):
    """
    Setup a logger, attach the handlers specified in the handlers list. Assign default formatter to handlers if not specified.
    :param logger_name: Name of the logger to be created. If None, the root logger will be used.
    :param default_handler_format: Formatter to be used for handlers if not specified.
    :param handlers: List of handlers to be attached to the logger.
    :param default_settings: Path to a yaml file containing default settings for the logger. Can also be a dict of the settings
    :return: logger
    """
    "TODO: Add dataclasses for default_settings to ensure correct format"
    # Create logger
    logger = logging.getLogger(logger_name)

    # Set global log level to 'debug' (required for handler levels to work)
    logger.setLevel(logging.DEBUG)

    if default_settings is None:
        default_settings = load_default_settings_global()
    elif isinstance(default_settings, str):
        # check if file exists
        if not os.path.isfile(default_settings):
            raise IncorrectSettingsError(
                f"Specified default_settings file does not exist: {default_settings}"
            )
        default_settings = load_yaml(default_settings)
    else:
        try:
            assert isinstance(default_settings, dict)
        except AssertionError:
            raise IncorrectSettingsError("default_settings must be a dict")

    try:
        if default_handler_format is None:
            default_handler_format = ColoredLogFormatter(
                **default_settings["logFormatter"]["streamHandler"]
            )
    except KeyError:
        raise IncorrectSettingsError(
            "default_settings must follow the format of default_settings.yaml"
        )

    # Add handlers to logger
    if handlers:
        for handler in handlers:
            if handler.formatter is None:
                handler.setFormatter(default_handler_format)
            logger.addHandler(handler)
    else:
        # If no handlers are specified, then create console handler as default
        handler = logging.StreamHandler(**default_settings["streamHandler"])
        handler.setFormatter(default_handler_format)
        logger.addHandler(handler)

    # Check if logger was created, if not then raise an exception
    if not logger:
        raise CreateLoggerError("Failed to setup logging, aborting.")
    # Return logger
    return logger


# Main function
def main():
    # Setup logging
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(filename=f"{script_name}.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        ColoredLogFormatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
    )

    logger = setup_logger(
        logger_name=script_name, handlers=[console_handler, file_handler]
    )

    # Log some messages
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")


# Call main function
if __name__ == "__main__":
    sys.exit(main())
