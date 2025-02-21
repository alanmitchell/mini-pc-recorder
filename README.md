# mini-pc-recorder
Data recorder built for mini-PCs running Linux.

There is a systemd service set up to run the record.py script at start-up,
and to restart it on failure.

For the PZEM reader, remember that the power sensor reads an 120V circuit for 
its voltage reference. So, power and energy need to be multiplied by 2 for 
accurate readings.
