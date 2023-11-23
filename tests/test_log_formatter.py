import logging
import os
import sys
from io import StringIO
import pytest
from log_formatter.log_formatter import setup_logging


@pytest.fixture
def captured_stdout():
    # Redirect stdout for capturing console log output
    sys.stdout = StringIO()
    yield sys.stdout
    # Restore stdout
    sys.stdout = sys.__stdout__


@pytest.fixture
def log_file_path(request):
    # Fixture to provide the log file path and cleanup after the test
    log_file = "your_script_name.log"
    yield log_file
    # Remove the log file created during the test
    if os.path.exists(log_file):
        os.remove(log_file)


def test_setup_logging_console_output(captured_stdout):
    logger = setup_logging(
        console_log_output="stdout",
        console_log_level="info",
        console_log_color=False,
    )
    assert isinstance(logger, logging.Logger)


def test_setup_logging_logfile_output(log_file_path):
    logger = setup_logging(
        logfile_file=log_file_path,
        logfile_log_level="info",
        logfile_log_color=False,
    )
    assert isinstance(logger, logging.Logger)


def test_setup_logging_console_and_logfile_output(captured_stdout, log_file_path):
    logger = setup_logging(
        console_log_output="stdout",
        console_log_level="info",
        console_log_color=False,
        logfile_file=log_file_path,
        logfile_log_level="info",
        logfile_log_color=False,
    )
    assert isinstance(logger, logging.Logger)


def test_log_messages(captured_stdout, log_file_path):
    logger = setup_logging(
        console_log_output="stdout",
        console_log_level="info",
        console_log_color=False,
        logfile_file=log_file_path,
        logfile_log_level="info",
        logfile_log_color=False,
    )

    logger.info("Test info message")
    logged_output = captured_stdout.getvalue().strip()
    assert "Info: Test info message" in logged_output

    # Check the content of the log file
    with open(log_file_path, "r") as f:
        log_file_content = f.read()
    assert "Test info message" in log_file_content
