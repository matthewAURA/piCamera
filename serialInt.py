import arduinoCommands as Arduino
import time

ard = Arduino.ArduinoController()
time.sleep(2)
ard.sendInt(12345);
print "Now Listening"
while True:
    print ard.ser.read()
