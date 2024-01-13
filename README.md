# python-custom-logging
## Purpose
A module to simplyfy customized logging to the console and to a log file

## Installation

```console
pip install git+https://github.com/davidson-engineering/python-custom-logging.git@stable
```

## Simple Initialisation and Usage
### myscript.py
```python
from custom_logging import setup_logger, ColoredLogFormatter

script_name = 'my_script'

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)

file_handler = logging.FileHandler(filename=f"{script_name}.log")
file_handler.setLevel(logging.DEBUG)

# set the log format for the file handler
file_handler.setFormatter(
    ColoredLogFormatter(
        fmt="%(asctime)s,%(msecs)d - %(name)s - %(levelname)-8s - %(message)s",
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
```

### Console output:
```
Warning: Warning message
Error: Error message
Critical: Critical message
```
### <i>my_script.log</i> output
![image](https://github.com/davidson-engineering/python-custom-logging/assets/106140501/69ee7316-edd8-4f58-9075-59c558909625)

## Best Practices for Multi-module Usage

### module1.py
```python
import logging

logger = logging.getLogger(__name__)

logger.warning("Warning message")
logger.debug("Debug message")
```

### module2.py
```python
import logging

logger = logging.getLogger(__name__)

logger.error("Error message")
logger.debug("Debug message")
```

### main.py
```python
import logging
from custom_logging import setup_logger

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)

file_handler = logging.FileHandler(filename=f"debug.log")
file_handler.setLevel(logging.DEBUG)

logger = setup_logger(
    logger_name="main.py",
    handlers=[console_handler, file_handler]
)

logger.info("logger initialised")

```
