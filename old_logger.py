import serial
import time
ser = serial.Serial('/dev/ttyACM0',115200, timeout=1) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
ser.flushInput()
ser.flushOutput()

while True:
    try:
        bytesToRead = ser.inWaiting()
        if bytesToRead != 0:
            #print(bytesToRead)
            #print(ser.read(bytesToRead))
            print(ser.readline(bytesToRead))
            print('------------------')
        #print(ser.read(bytesToRead))
    except:
        print("Keyboard Interrupt")
        break
