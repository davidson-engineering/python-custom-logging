import logging
import os
import sys
from io import StringIO
import pytest
from custom_logging.custom_logging import setup_logger
import uuid
import atexit
import time


@pytest.fixture
def captured_stdout():
    # Redirect stdout for capturing console log output
    sys.stdout = StringIO()
    yield sys.stdout
    # Restore stdout
    sys.stdout = sys.__stdout__


def log_file_cleanup(log_file):
    if os.path.exists(log_file):
        os.remove(log_file)


def close_file_handles(log_file):
    for handler in logging.getLogger().handlers:
        if (
            isinstance(handler, logging.FileHandler)
            and handler.baseFilename == log_file
        ):
            handler.close()


@pytest.fixture
def log_file_path(request):
    # Fixture to provide the log file path and cleanup after the test
    log_file = f"{str(uuid.uuid4())}.log"
    yield log_file

    # Register a finalizer to ensure cleanup even if an exception occurs
    request.addfinalizer(lambda: atexit.register(close_file_handles, log_file))

    time.sleep(1)

    request.addfinalizer(lambda: log_file_cleanup(log_file))


def test_setup_logging_console_output(captured_stdout):
    logger = setup_logger()
    assert isinstance(logger, logging.Logger)


def test_setup_logging_logfile_output(log_file_path):
    file_handler = logging.FileHandler(filename=log_file_path)
    logger = setup_logger(handlers=[file_handler])
    assert isinstance(logger, logging.Logger)


def test_setup_logging_console_and_logfile_output(log_file_path):
    file_handler = logging.FileHandler(filename=log_file_path)
    console_handler = logging.StreamHandler(sys.stdout)
    logger = setup_logger(handlers=[file_handler, console_handler])
    assert isinstance(logger, logging.Logger)


def test_log_messages(capsys, log_file_path):
    file_handler = logging.FileHandler(filename=log_file_path)
    console_handler = logging.StreamHandler(sys.stdout)
    logger = setup_logger(handlers=[file_handler, console_handler])

    # Log a message
    logger.info("Test info message")

    # Check the content of the captured console output
    captured = capsys.readouterr()
    logged_output = captured.out.strip()
    assert (
        "Test info message" in logged_output
    ), "Expected log message not found in console output"

    # Check the content of the log file
    with open(log_file_path, "r") as log_file:
        log_file_content = log_file.read()
        assert (
            "Test info message" in log_file_content
        ), "Expected log message not found in log file"
