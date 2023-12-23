#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-11-22
# ---------------------------------------------------------------------------
"""
A module to enable customized logging to the console and to a log file.
Based on original code by fonic - https://github.com/fonic
"""
# ---------------------------------------------------------------------------

# - Extend 'setup_logging()' to create directory path for logfile -> see code
#   in 'write_file()', 'module_miscellaneous.py'

__all__ = ["setup_logging"]

import sys
import logging
import os

default_params_timedrotatingfilehandler = dict(
    when="midnight",
    interval=1,
    backupCount=7,
    encoding=None,
    delay=False,
    utc=False,
    atTime=None,
    errors=None,
)

default_params_filehandler = dict(
    mode="a",
    encoding=None,
    delay=False,
    errors=None,

)

default_params_streamhandler = dict(
    stream=None,
)

default_params_formatter = dict(
    fmt="%(color_on)s[%(asctime)s] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    color=False
)


# Logging formatter supporting colored output
class LogFormatter(logging.Formatter):
    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m",  # bright/bold magenta
        logging.ERROR: "\033[1;31m",  # bright/bold red
        logging.WARNING: "\033[1;33m",  # bright/bold yellow
        logging.INFO: "\033[1;37m",  # bright/bold white
        logging.DEBUG: "\033[0;37m",  # white / light gray
    }

    RESET_CODE = "\033[0m"

    def __init__(self, *args, color, **kwargs):
        self.color = color
        super(LogFormatter, self).__init__(*args, **kwargs)

    def format(self, record, *args, **kwargs):
        if self.color == True and record.levelno in self.COLOR_CODES:
            record.color_on = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on = ""
            record.color_off = ""
        record.levelname2 = record.levelname.capitalize()
        return super(LogFormatter, self).format(record, *args, **kwargs)


def merge_logging_formats(default_format, handler_format):
    # function to merge a logging.Formatter object with some default format options in a dioct
    # returns a logging.Formatter with the merged format options

    # get the default format options
    default_format_dict = default_format.__dict__
    # get the handler format options
    handler_format_dict = handler_format.__dict__
    # merge the two dicts
    merged_format_dict = default_format_dict.update(handler_format_dict)
    # create a logging.Formatter object with the merged format options
    merged_format = logging.Formatter(**merged_format_dict)
    # return the logging.Formatter object
    return merged_format

# Setup logging
# NOTE: logger_name == None -> root logger
def setup_logger(
    logger_name=None,
    default_handler_format = None,
    handlers=None
):
    # Create logger
    logger = logging.getLogger(logger_name)

    # Set global log level to 'debug' (required for handler levels to work)
    logger.setLevel(logging.DEBUG)

    if default_handler_format is None:
        default_handler_format = LogFormatter(
            **default_params_formatter,
        ).__dict__

    if handlers:
        for handler in handlers:
            if handler.formatter:
                handler_format = default_handler_format.update(handler.formatter.__dict__)
            else:
                handler_format = default_handler_format
            handler_format = LogFormatter(
                **default_handler_format
            )
            handler.setFormatter(handler_format)
            logger.addHandler(handler)
    else:
        # Create console handler
        console_handler = logging.StreamHandler(**default_params_streamhandler)
        console_handler_line_format = console_handler.fmt or default_line_format
        console_handler_date_format = console_handler.datefmt or default_date_format
        console_handler_color = console_handler.color or log_color
        console_handler_format = LogFormatter(
            fmt=console_handler_line_format,
            datefmt=console_handler_date_format,
            color=console_handler_color,
        )
        console_handler.setFormatter(console_handler_format)
        logger.addHandler(console_handler)

    if not logger:
        print("Failed to setup logging, aborting.")
        return
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


    logger = setup_logger(
        logger_name=script_name,
        handlers=[console_handler, file_handler]
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
