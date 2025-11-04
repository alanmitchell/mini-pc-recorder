"""Reader for PZEM-016 AC power measurement device.
"""
import time
import math
import pyfirmata2

# Steinhart Coefficients for thermistors
C1 = 0.00128637
C2 = 0.00023595
C3 = 9.3841E-08

PORT = '/dev/ttyUSB1'
board = pyfirmata2.Arduino(PORT)
board.samplingOn(50)      # ms sampling interval

class TempSensor:

    READ_COUNT = 10

    def __init__(self, pin_num):
        self.buffer = [70.0] * TempSensor.READ_COUNT
        self.ix = 0
        board.analog[pin_num].register_callback(self.new_data)
        board.analog[pin_num].enable_reporting()

    def new_data(self, value):
        self.buffer[self.ix] = value
        self.ix = (self.ix + 1) % TempSensor.READ_COUNT

    def temperature(self):
        val_avg = sum(self.buffer) / TempSensor.READ_COUNT
        if val_avg < 0.998:
            resis = val_avg / (1.0 - val_avg) * 9760.0
            lnR = math.log(resis)
            return (1.8 / (C1 + C2 * lnR + C3 * lnR ** 3)) - 459.67
        else:
            # open connection
            return -999.0

sensors = [TempSensor(p) for p in range(4)]
time.sleep(3)     # wait for Arduino

def header_row():
    return "ts,temp0,temp1,temp2,temp3"

def read_data():
    sensors_str = ','.join([f'{sensors[i].temperature():.1f}' for i in range(4)])
    return f'{time.time():.1f},{sensors_str}'
