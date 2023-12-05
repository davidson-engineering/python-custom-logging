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


# Setup logging
# NOTE: logger_name == None -> root logger
def setup_logging(
    logger_name=None,
    console_log_output="stdout",
    console_log_level="debug",
    console_log_color=False,
    console_log_template="%(color_on)s%(levelname2)s: %(message)s%(color_off)s",
    logfile_file=None,
    logfile_log_level="debug",
    logfile_log_color=False,
    logfile_log_template="%(color_on)s[%(asctime)s] [%(levelname)-8s] %(message)s%(color_off)s",
    logfile_log_datefmt="%Y%m%d|%H:%M:%S.%f",
    logfile_truncate=False,
):
    # Create logger
    logger = logging.getLogger(logger_name)

    # Set global log level to 'debug' (required for handler levels to work)
    logger.setLevel(logging.DEBUG)

    # Console
    if console_log_output != None:
        # Create console handler
        console_log_output = console_log_output.lower()
        if console_log_output == "stdout":
            console_log_output = sys.stdout
        elif console_log_output == "stderr":
            console_log_output = sys.stderr
        else:
            raise ValueError("invalid console log output: '%s'" % console_log_output)
        try:
            console_handler = logging.StreamHandler(console_log_output)
        except Exception as exception:
            raise Exception(
                "failed to set up console handler: %s" % str(exception)
            ) from exception

        # Set console log level
        try:
            console_handler.setLevel(
                console_log_level.upper()
            )  # only accepts uppercase level names
        except ValueError as valueerror:
            raise ValueError(
                "invalid console log level: '%s'" % console_log_level
            ) from valueerror

        # Create and set formatter, add console handler to logger
        console_formatter = LogFormatter(
            fmt=console_log_template, color=console_log_color
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # Log file
    if logfile_file != None:
        # Create log file handler
        try:
            logfile_handler = logging.FileHandler(
                logfile_file, mode="a" if (logfile_truncate == False) else "w"
            )
        except Exception as exception:
            raise Exception(
                "failed to set up log file handler: %s" % str(exception)
            ) from exception

        # Set log file log level
        try:
            logfile_handler.setLevel(
                logfile_log_level.upper()
            )  # only accepts uppercase level names
        except ValueError as valueerror:
            raise ValueError(
                "invalid log file log level: '%s'" % logfile_log_level
            ) from valueerror

        # Create and set formatter, add log file handler to logger
        logfile_formatter = LogFormatter(
            fmt=logfile_log_template, color=logfile_log_color, datefmt=logfile_log_datefmt
        )
        logfile_handler.setFormatter(logfile_formatter)
        logger.addHandler(logfile_handler)

    # Return logger
    return logger


# Main function
def main():
    # Setup logging
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if not setup_logging(
        console_log_output="stdout",
        console_log_level="warning",
        console_log_color=True,
        logfile_file=f"{script_name}.log",
        logfile_log_level="debug",
        logfile_log_color=False,
        log_line_template="%(color_on)s[%(asctime)s] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s",
    ):
        print("Failed to setup logging, aborting.")
        return 1

    # Log some messages
    logging.debug("Debug message")
    logging.info("Info message")
    logging.warning("Warning message")
    logging.error("Error message")
    logging.critical("Critical message")


# Call main function
if __name__ == "__main__":
    sys.exit(main())
