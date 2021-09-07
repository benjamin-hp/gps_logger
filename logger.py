import serial
import time
import pynmea2
import io
import datetime
import csv
import logging
import socket
import strict_rfc3339

from logging.handlers import RotatingFileHandler
from datetime import datetime,timezone,date

try:
    ser = serial.Serial('/dev/ttyACM0',115200, timeout=1) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
    ser.flushInput()
    ser.flushOutput()
    sio = io.TextIOWrapper(io.BufferedRWPair(ser,ser))
except serial.SerialException as e:
    print('Device error: {}'.format(e))
    exit()

log_file = "gps_data.log"
hostname = socket.gethostname()
now_utc = datetime.now(timezone.utc)
iso_utc = now_utc.isoformat()
iso_utc = iso_utc.replace(':', '')
size = len(iso_utc)
iso_utc = iso_utc[:size - 5]
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "/home/end/gps_logger/logs/"+ "gps_" + hostname + "_" + iso_utc +".csv"
print(filename) 

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)

    # add a rotating handler
handler = RotatingFileHandler(filename, maxBytes=200000000,
                                  backupCount=0)
logger.addHandler(handler)


while True:
    try:
        now_utc = datetime.now(timezone.utc)
        rfc_3339 = strict_rfc3339.now_to_rfc3339_utcoffset()
        line = sio.readline()
        msg = pynmea2.parse(line)

        if isinstance(msg, pynmea2.types.talker.GGA):
            logger.info("%s,%s",rfc_3339, msg)
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        #break
    except:
        print("Keyboard Interrupt")
        #break
