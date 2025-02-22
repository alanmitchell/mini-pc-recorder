"""Reader to read 12VDC battery from MCP2221A board
"""
import time

import board
from analogio import AnalogIn

battery_in = AnalogIn(board.G1)

def header_row():
    return "ts,voltage"

def read_data():
    try:
        bat_tot = 0.0
        for i in range(10):
            bat_tot += battery_in.value 
        bat_volts = bat_tot / 10.0 * 3.3 / 65536 * 5.695
        return f'{time.time():.0f},{bat_volts}'
    except Exception as e:
        return None

