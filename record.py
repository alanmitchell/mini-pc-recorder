"""Main data reading and recording script.
"""
import time
from pathlib import Path

# Change the following three lines according to data collection needs.
from readers.pzem016 import read_data, header_row
fn = 'power.csv'
sleep_time = 0.2

# If output file doesn't exist, create it with a header row.
full_fn = Path(__file__).parent / "data" / fn
if not full_fn.exists():
    with open(full_fn, 'w') as fout:
        fout.write(f"{header_row()}\n")

while True:
    try:
        data_line = read_data()
        if data_line:
            with open(full_fn, 'a') as fout:
                fout.write(f"{data_line}\n")
        time.sleep(sleep_time)

    except Exception as e:
        print(e)
        time.sleep(sleep_time)