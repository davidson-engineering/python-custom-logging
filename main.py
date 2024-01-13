#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-01-23
# version ='1.0'
# ---------------------------------------------------------------------------
"""
Demonstration code for a module to enable convienient access to customized logging to the console and to log files.
"""
# ---------------------------------------------------------------------------

import os
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from custom_logging import setup_logger, ColoredLogFormatter


# Main function
def main():
    # Setup logging with a stream handler and a file handler
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        ColoredLogFormatter(
            fmt="%(asctime)s,%(msecs)d - %(name)s - %(levelname)-8s - %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
    )

    file_handler = logging.FileHandler(filename=f"{script_name}.log")
    file_handler.setLevel(logging.DEBUG)

    # set the log format for the file handler
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s,%(msecs)03d - %(name)s - %(levelname)-8s - %(message)s",
            datefmt="%Y/%m/%d %H:%M:%S",
        )
    )
    # create the logger
    logger = setup_logger(
        logger_name=script_name, handlers=[console_handler, file_handler]
    )

    # Log some messages
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")

    # Setup a timed rotation log file handler
    file_handler = TimedRotatingFileHandler(
        filename=f"{script_name}.log",
        when="midnight",
        interval=1,
        backupCount=7,
        encoding=None,
        delay=False,
        utc=False,
        atTime=None,
    )
    file_handler.setLevel(logging.DEBUG)
    # Set the log format
    stream_formatter = ColoredLogFormatter(
        fmt="%(asctime)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S", color=True
    )
    console_handler.setFormatter(stream_formatter)
    file_formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)-8s - %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)

    timedrot_logger = setup_logger(
        logger_name=script_name,
        handlers=[console_handler, file_handler],
    )

    # Log some messages
    timedrot_logger.debug("Debug message")
    timedrot_logger.info("Info message")
    timedrot_logger.warning("Warning message")
    timedrot_logger.error("Error message")
    timedrot_logger.critical("Critical message")


# Call main function
if __name__ == "__main__":
    sys.exit(main())
