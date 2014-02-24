
import serial

try:
    # Win32
    from msvcrt import getch
except ImportError:
    # UNIX
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

ser = serial.Serial("/dev/ttyACM0",9600,timeout=3)			

while True:
    
    character = getch()
    print character
    if (character == "a" or character == "d"):    
        ser.write(character*5)
    elif (character == "x"):
        break
