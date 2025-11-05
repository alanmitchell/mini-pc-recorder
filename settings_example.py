# Sample Settings file for application. Copy to "settings.py" and adjust.

READER_MODULE = 'temp_board'   # name of reader module
FILE_PREFIX = 'temp'           # prefix for data file names
SLEEP_TIME = 3.0               # seconds of sleep between readings

# Overrides the Reader-supplied header row. Comment out to not override
HEADER = 'ts,ex_cool,ex_warm,sup_cool,sup_warm' 

# Serial port for readers using a serial connection
SERIAL_PORT = '/dev/ttyUSB1'

# Steinhart Coefficients for thermistors when using temp_board reader.
C1 = 0.00128637
C2 = 0.00023595
C3 = 9.3841E-08
