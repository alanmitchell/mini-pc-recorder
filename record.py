"""Main data reading and recording script.
"""
import time
from pathlib import Path
import importlib
import logging
import logging.handlers

# Change the following three lines according to data collection needs.
# Note that reader modules must have "header_row" and "read_data" methods.
"""
# PZEM-016 power sensor
reader_module_name = "pzem016"
fn = 'power.csv'
sleep_time = 5.0
"""
# Reading 12VDC battery voltage through an MCP2221A board.
reader_module_name = "bat_volts"
fn = "battery.csv"
sleep_time = 1.0

# --------------------------- No Changes Needed below Here ------------------

def configure_logging():
    """
    Configures the logging for the application.
    Logs will include timestamps, file names, line numbers, log levels, and messages.
    Uses a rotating file handler with a size limit.
    """

    # Create a rotating file handler that rotates at 1 MB
    # and keeps up to 5 backup log files.
    log_path = Path(__file__).parent / "logs" / "errors.log"
    rotating_file_handler = logging.handlers.RotatingFileHandler(
        log_path, 
        maxBytes=1024 * 1024,  # 1 MB
        backupCount=5
    )

    # Define the format for the log messages
    log_format = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    rotating_file_handler.setFormatter(log_format)

    # Get the root logger and set its level
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(rotating_file_handler)

configure_logging()

reader_module = importlib.import_module(f"readers.{reader_module_name}")

# Full path to the output file
full_fn = Path(__file__).parent / "data" / fn

while True:
    # If output file doesn't exist, create it with a header row.
    if not full_fn.exists():
        with open(full_fn, 'w') as fout:
            fout.write(f"{reader_module.header_row()}\n")
    try:
        data_line = reader_module.read_data()
        if data_line:
            with open(full_fn, 'a') as fout:
                fout.write(f"{data_line}\n")

    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)

    time.sleep(sleep_time)
