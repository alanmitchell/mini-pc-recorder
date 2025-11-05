"""Main data reading and recording script.
"""
import time
from datetime import datetime
from pathlib import Path
import importlib
import logging
import logging.handlers

import settings

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

reader_module = importlib.import_module(f"readers.{settings.READER_MODULE}")
reader = reader_module.Reader(settings)

# Look for a header override in the Settings file and use it if there.
if hasattr(settings, 'HEADER') and settings.HEADER:
    header_row = settings.HEADER
else:
    header_row = reader.header_row()

while True:
    # Full path to the output file
    fn = f"{settings.FILE_PREFIX}_{datetime.now().strftime('%Y-%m-%d')}.csv"
    full_fn = Path(__file__).parent / "data" / fn

    # If output file doesn't exist, create it with a header row.
    if not full_fn.exists():
        with open(full_fn, 'w') as fout:
            fout.write(f"{header_row}\n")
    try:
        data_line = reader.read_data()
        if data_line:
            with open(full_fn, 'a') as fout:
                fout.write(f"{data_line}\n")

    except Exception as e:
        logging.error("An error occurred: %s", e, exc_info=True)

    time.sleep(settings.SLEEP_TIME)
