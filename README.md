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
[231204|213440.662] [DEBUG   ] Debug message
[231204|213440.662] [INFO    ] Info message
[231204|213440.663] [WARNING ] Warning message
[231204|213440.663] [ERROR   ] Error message
[231204|213440.663] [CRITICAL] Critical message
```
