"""Main data reading and recording script.
"""
import time
from datetime import datetime
from pathlib import Path
import importlib
import logging
import logging.handlers

# Change the following three lines according to data collection needs.
# Note that reader modules must have "header_row" and "read_data" methods.

reader_module_name = "temp_board"
fn_prefix = "temp-"
sleep_time = 2.0

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


while True:
    # Full path to the output file
    fn = f"{fn_prefix}{datetime.now().strftime('%Y-%m-%d')}.csv"
    full_fn = Path(__file__).parent / "data" / fn

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
