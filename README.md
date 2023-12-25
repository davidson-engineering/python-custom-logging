# python-custom-logging
A module to simplyfy customized logging to the console and to a log file

```python
from custom_logging import setup_logger

script_name = 'my_script.py'

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.warning)

file_handler = logging.FileHandler(filename=f"{script_name}.log")
file_handler.setLevel(logging.DEBUG)

# set the log format for the file handler
file_handler.setFormatter(
    logging.Formatter(
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

Console output:
```
Warning: Warning message
Error: Error message
Critical: Critical message
```
<i>logfile.log</i> output
```
2023/12/24 21:02:45,470 - main - DEBUG    - Debug message
2023/12/24 21:02:45,471 - main - INFO     - Info message
2023/12/24 21:02:45,471 - main - WARNING  - Warning message
2023/12/24 21:02:45,472 - main - ERROR    - Error message
2023/12/24 21:02:45,472 - main - CRITICAL - Critical message
```
