# python-formatted-logging
A module to enable customized logging to the console and to a log file

```python
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
