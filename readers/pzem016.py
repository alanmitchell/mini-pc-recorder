"""Reader for PZEM-016 AC power measurement device.
"""
import time
import minimalmodbus

minimalmodbus.CLOSE_PORT_AFTER_EACH_CALL=True
instr = minimalmodbus.Instrument('/dev/ttyACM0', 1)
instr.serial.timeout = 0.1
instr.serial.baudrate = 9600

def header_row():
    return "ts,voltage,current,frequency,power,power_factor,energy"

def read_data():
    data = None
    for i in range(5):
        try:
            data = instr.read_registers(0, 10, 4)
            break
        #except IOError as e:
        #    print('Error')
        #    pass
        except Exception as e:
            print(e)
    if data:
        v, i, p, en, f, pf, alarm = [ 
            round((data[0]*0.1), 1),                    # Voltage(0.1V)
            round((data[1]+data[2]*65536)*0.001, 3),  # Current(0.001A)
            round((data[3]+data[4]*65536)*0.1, 1),    # Power(0.1W)
            round((data[5]+data[6]*65536), 0),        # Energy(1Wh)
            round(data[7]*0.1, 1),                      # Frequency(0.1Hz)
            round(data[8]*0.01, 2),                     # Power Factor(0.01)
            int(data[9]>0)                              # Alarm(1)
        ]
        return f'{time.time():.2f},{v},{i},{f},{p},{pf},{en}'

    else:
        return None

