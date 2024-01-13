# python-custom-logging
## Purpose
A module to simplify logging setup in Python

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

Use the <i>\_\_name\_\_</i> variable so that the logger in each module is uniquely identifiable.

The logger name can then be referenced by adding the <i>name</i> attribute to the <i>fmt</i> parameter when initiliasing a <i>logging.Formatter</i> object.

This allows clear identification of the which module the log was made from.

A simple example is shown below:
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
console_handler.setFormatter(logging.Formatter("%(name)s: %(levelname)s - %(message)s"))

file_handler = logging.FileHandler(filename=f"debug.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter("%(name)s: %(levelname)s - %(message)s"))

logger = setup_logger(
    logger_name="main.py",
    handlers=[console_handler, file_handler]
)

logger.info("logger initialised")

```
### Console Output
```console
module1: WARNING - Warning message
module2: ERROR - Error message
```
### <i>debug.log</i> Output
```log
root: INFO - logger initialised
module1: WARNING - Warning message
module1: DEBUG - Debug message
module2: ERROR - Error message
module2: DEBUG - Debug message

```
