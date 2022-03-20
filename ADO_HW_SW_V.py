import os
import sys
import subprocess as sp
import lcddriver
import time
from ADO_Rev import rev
from ADO_Unit import ado_

display = lcddriver.lcd()
output = sp.getoutput('ls /sys/bus/w1/devices/')
output = output [0:15]
print (output)





def GDisplay(Line1,Line2,Line3,Line4):
    display.lcd_clear()
    display.lcd_display_string(Line1, 1)
    display.lcd_display_string(Line2, 2)
    display.lcd_display_string(Line3, 3)
    display.lcd_display_string(Line4, 4)


if output == ('28-0313977918b4'): # ADO1 Full probe
    if ado_ == 'ADO1':
        print('Valid HW to SW', ado_)
    else:
        print ('HW / SW Mismatch')
        GDisplay('Hardware / ', 'Software', 'Mismatch', 'Call BW')
        time.sleep(5)
        os.system('sudo reboot')
elif output == ('28-012026ff668d'): # ADO1
    if ado_ == 'ADO1':
        print('Valid HW to SW', ado_)
    else:
        print('HW / SW Mismatch')
        GDisplay('Hardware / ', 'Software', 'Mismatch', 'Call BW')
        time.sleep(5)
        os.system('sudo reboot')
elif output == ('28-012026df51f5'): # ADO2
    if ado_ == 'ADO2':
        print('Valid HW to SW', ado_)
    else:
        print('HW / SW Mismatch')
        GDisplay('Hardware / ', 'Software', 'Mismatch', 'Call BW')
        time.sleep(5)
        os.system('sudo reboot')
elif output == ('28-01202910e506'): # ADO3
    if ado_ == 'ADO3':
        print('Valid HW to SW', ado_)
    else:
        print('HW / SW Mismatch')
        GDisplay('Hardware / ', 'Software', 'Mismatch', 'Call BW')
        time.sleep(5)
        os.system('sudo reboot')
elif output == ('28-0120293b0a4f'): # ADO4
    if ado_ == 'ADO4':
        print('Valid HW to SW', ado_)
    else:
        print('HW / SW Mismatch')
        GDisplay('Hardware / ', 'Software', 'Mismatch', 'Call BW')
        time.sleep(5)
        os.system('sudo reboot')
elif output == ('28-012027260629'): # ADO5
    if ado_ == 'ADO5':
        print('Valid HW to SW', ado_)
    else:
        print('HW / SW Mismatch')
        time.sleep(5)
        os.system('sudo reboot')
elif output == ('28-0120270d0c1f'): # ADO6
    if ado_ == 'ADO6':
        print('Valid HW to SW', ado_)
    else:
        print('HW / SW Mismatch')
        GDisplay('Hardware / ', 'Software', 'Mismatch', 'Call BW')
        time.sleep(5)
        os.system('sudo reboot')
else:
    print('Error Reading Address')
    GDisplay('Error Reading ', 'Address', '', 'Call BW')
    os.system('sudo reboot')
# else:
#     print ('Invalid HW')
#     # display.lcd_clear()
#     # display.lcd_display_string("Bellwether Co. ADO", 1)
#     # display.lcd_display_string('Invalid HW', 2)
#     # display.lcd_display_string(str(ado_), 3)
#     # display.lcd_display_string(str(rev), 4)
#     # time.sleep(1)
#     # display.lcd_clear()
#     os.system('sudo reboot')
