# python-formatted-logging
A module to enable customized logging to the console and to a log file

```python
from log_formatter import setup_logging

setup_logging(
    console_log_output="stdout",
    console_log_level="warning",
    console_log_color=True,
    logfile_file="logfile.log",
    logfile_log_level="debug",
    logfile_log_color=False,
    log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s"
)

# Log some messages
logging.debug("Debug message")
logging.info("Info message")
logging.warning("Warning message")
logging.error("Error message")
logging.critical("Critical message")
```
Console Output:
```
Warning: Warning message
Error: Error message
Critical: Critical message
```
logfile.log output
```
[1700718790] [MainThread] [DEBUG   ] Debug message
[1700718790] [MainThread] [INFO    ] Info message
[1700718790] [MainThread] [WARNING ] Warning message
[1700718790] [MainThread] [ERROR   ] Error message
[1700718790] [MainThread] [CRITICAL] Critical message
```
