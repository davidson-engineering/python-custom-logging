# python-formatted-logging
A module to enable customized logging to the console and to a log file

```python
from log_formatter import setup_logging

setup_logging(
    console_log_output="stdout",
    console_log_level="warning",
    console_log_color=True,
    logfile_file=f"logfile.log",
    logfile_log_level="debug",
    logfile_log_color=False,
    logfile_log_datefmt="%Y-%m-%d %H:%M:%S",
)

# Log some messages
logging.debug("Debug message")
logging.info("Info message")
logging.warning("Warning message")
logging.error("Error message")
logging.critical("Critical message")
```
Console output:
```
Warning: Warning message
Error: Error message
Critical: Critical message
```
<i>logfile.log</i> output
```
[2023-12-04 21:40:17.290] [DEBUG   ] Debug message
[2023-12-04 21:40:17.291] [INFO    ] Info message
[2023-12-04 21:40:17.291] [WARNING ] Warning message
[2023-12-04 21:40:17.291] [ERROR   ] Error message
[2023-12-04 21:40:17.291] [CRITICAL] Critical message
```
