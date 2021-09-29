import serial
import time
import pynmea2
import io
import datetime
import csv
import logging
import socket
from pathlib import Path

from logging.handlers import RotatingFileHandler
#from datetime import datetime,timezone,date

try:
    ser = serial.Serial('/dev/ttyACM0',115200, timeout=1) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
    ser.flushInput()
    ser.flushOutput()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
except serial.SerialException as e:
    print('Device error: {}'.format(e))
    exit()

home = str(Path.home())
iso_utc = datetime.datetime.utcnow().isoformat().replace(':', '')
hostname = socket.gethostname()
fleet_id = hostname[:len(hostname) - 9]
hack_id = hostname[6:]
filename =home + "/gps_logger/logs/"+ "gps_"  + fleet_id + '_' + iso_utc + "_" + hack_id + '.csv'

print(filename) 

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)

    # add a rotating handler
handler = RotatingFileHandler(filename, maxBytes=200000000,
                                  backupCount=0)
logger.addHandler(handler)


while True:
    try:
#         now_utc = datetime.now(timezone.utc)
#        rfc_3339 = strict_rfc3339.now_to_rfc3339_utcoffset()
        line = sio.readline()
        msg = pynmea2.parse(line)

        if isinstance(msg, pynmea2.types.talker.GGA):
            logger.info("%s,%s",datetime.datetime.utcnow().isoformat(), msg)
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        #break
    except:
        print("Keyboard Interrupt")
        #break
