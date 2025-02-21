"""Main data reading and recording script.
"""
import time
from pathlib import Path
import importlib

# Change the following three lines according to data collection needs.
# Note that reader modules must have "header_row" and "read_data" methods.
reader_module_name = "pzem016"
fn = 'power.csv'
sleep_time = 5.0

# --------------------------- No Changes Needed below Here ------------------

reader_module = importlib.import_module(f"readers.{reader_module_name}")

# If output file doesn't exist, create it with a header row.
full_fn = Path(__file__).parent / "data" / fn
if not full_fn.exists():
    with open(full_fn, 'w') as fout:
        fout.write(f"{reader_module.header_row()}\n")

while True:
    try:
        data_line = reader_module.read_data()
        if data_line:
            with open(full_fn, 'a') as fout:
                fout.write(f"{data_line}\n")
        time.sleep(sleep_time)

    except Exception as e:
        print(e)
        time.sleep(sleep_time)