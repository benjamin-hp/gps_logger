import serial
import time
import pynmea2
import io
import datetime
import csv
import logging
import socket

from logging.handlers import RotatingFileHandler

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
timestr = time.strftime("%Y%m%d-%H%M%S")
filename = "/home/hp/gps_logger/logs/"+ hostname + "_" + timestr +"_gps.log"
print(filename) 

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.INFO)

    # add a rotating handler
handler = RotatingFileHandler(filename, maxBytes=200000000,
                                  backupCount=0)
logger.addHandler(handler)


while True:
    try:
        line = sio.readline()
        msg = pynmea2.parse(line)
        #print(repr(msg)) 
        #print(repr(msg.timestamp))
        #print(msg.latitude)
        if isinstance(msg, pynmea2.types.talker.GGA):
            #print('GGA MSG:\n')
            #print(repr(msg))
            #print('GPS time:' + repr(msg.timestamp))
            #print('System time:' + datetime.datetime.now().isoformat())
            #print(msg.lat+msg.lat_dir)
            #print(msg.lon+msg.lon_dir)
            #print(repr(msg.gps_qual)+repr(msg.num_sats))
            #local_time = datetime.datetime.now().isoformat()
            #gps_time = msg.timestamp
            #gps_lat = msg.lat+msg.lat_dir
            #gps_lon =  msg.lon+msg.lon_dir
            #print(local_time)
            #print(gps_time)
            #print(gps_lat)
            #print(gps_lon)
            
            #logger.info("%s %s %s %s", local_time, gps_time, gps_lat, gps_lon)
            #logger.info("%s",local_time)
            logger.info("%s",msg)
            #with open("test_data.csv","a") as f:
                #writer = csv.writer(f,delimiter=",")
                #writer.writerow([local_time,gps_time,gps_lat,gps_lon])
        #if isinstance(msg, pynmea2.types.talker.GLL):
        #    print(repr(msg))
        #print('-----------------------------------\n')
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break
    except:
        print("Keyboard Interrupt")
        break
