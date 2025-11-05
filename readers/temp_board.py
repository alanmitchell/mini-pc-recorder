"""For a Thermistor board connected to an Arduino running Firmata.
"""
import time
import math
import pyfirmata2


class TempSensor:

    READ_COUNT = 10

    def __init__(self, board, pin_num, C1, C2, C3):
        self.buffer = [70.0] * TempSensor.READ_COUNT
        self.ix = 0
        board.analog[pin_num].register_callback(self.new_data)
        board.analog[pin_num].enable_reporting()
        self.C1 = C1
        self.C2 = C2
        self.C3 = C3

    def new_data(self, value):
        self.buffer[self.ix] = value
        self.ix = (self.ix + 1) % TempSensor.READ_COUNT

    def temperature(self):
        val_avg = sum(self.buffer) / TempSensor.READ_COUNT
        if val_avg < 0.998:
            resis = val_avg / (1.0 - val_avg) * 9760.0
            lnR = math.log(resis)
            return (1.8 / (self.C1 + self.C2 * lnR + self.C3 * lnR ** 3)) - 459.67
        else:
            # no thermistor attached
            return None

class Reader:

    def __init__(self, settings):

        board = pyfirmata2.Arduino(settings.SERIAL_PORT)
        board.samplingOn(50)      # ms sampling interval
        self.sensors = [TempSensor(board, p, settings.C1, settings.C2, settings.C3) for p in range(4)]
        time.sleep(3)     # wait for Arduino

    def header_row(self):
        return "ts,temp0,temp1,temp2,temp3"

    def read_data(self):
        vals = [s.temperature() for s in self.sensors]
        vals_fmt = [f'{v:.1f}' if v is not None else '' for v in vals ]
        sensors_str = ','.join(vals_fmt)
        return f'{time.time():.1f},{sensors_str}'
