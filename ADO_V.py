import os
import sys
import subprocess as sp
# import lcddriver
import time
from ADO_Rev import rev
from ADO_Unit import ado_

# display = lcddriver.lcd()
output = sp.getoutput('ls /sys/bus/w1/devices/')
output = output [0:15]
print (output)


if output == ('28-0313977918b4'): # ADO1 Full probe
    print('Valid HW')
    # os.execl(sys.executable, 'python3','/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
elif output == ('28-012026ff668d'): # ADO1
    print('Valid HW')
    # os.execl(sys.executable, 'python3','/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
elif output == ('28-012026df51f5'): # ADO2
    print('Valid HW')
    # os.execl(sys.executable, 'python3','/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
elif output == ('28-01202910e506'): # ADO3
    print('Valid HW')
    # os.execl(sys.executable, 'python3','/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
elif output == ('28-0120293b0a4f'): # ADO4
    print('Valid HW')
    # os.execl(sys.executable, 'python3','/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
elif output == ('28-012027260629'): # ADO5
    print('Valid HW')
    # os.execl(sys.executable, 'python3','/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
elif output == ('28-0120270d0c1f'): # ADO6
    print('Valid HW')
    # os.execl(sys.executable, 'python3','/home/pi/Bellwether/ADO_UI.py', *
elif output == ('28-3c01d6075443'): # ADOTEMP1
    print('Valid HW')
    # os.execl(sys.executable, 'python3','/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
elif output == (''): # ADOTEMP2
    print('Valid HW')
    # os.execl(sys.executable, 'python3','/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
elif output == (''): # ADOTEMP3
    print('Valid HW')
    # os.execl(sys.executable, 'python3','/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
elif output == (''): # ADOTEMP4
    print('Valid HW')
    # os.execl(sys.executable, 'python3','/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
else:
    print ('Invalid HW')
    # display.lcd_clear()
    # display.lcd_display_string("Bellwether Co. ADO", 1)
    # display.lcd_display_string('Invalid HW', 2)
    # display.lcd_display_string(str(ado_), 3)
    # display.lcd_display_string(str(rev), 4)
    # time.sleep(1)
    # display.lcd_clear()
    os.system('sudo reboot')
