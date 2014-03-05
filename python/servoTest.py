import arduinoCommands as Arduino
import time
import binascii

ard = Arduino.ArduinoController()
time.sleep(2)


# To see what it looks like on python side
val = 15000
print binascii.hexlify(ard.packIntegerAsULong(val))
ard.sendLong(val)
# send and receive via pyserial
line = ard.ser.readline()
print line

