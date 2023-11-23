#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Matthew Davidson
# Created Date: 2023-01-23
# version ='1.0'
# ---------------------------------------------------------------------------
"""a_short_project_description"""
# ---------------------------------------------------------------------------

import os
import logging
import sys

from log_formatter.log_formatter import setup_logging


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
        log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s",
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
