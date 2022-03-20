#!/usr/bin/env python

import time
import datetime
import lcddriver
import lcddriver2
import socket
import subprocess
import os
import sys
from ADO_Rev import rev
from ADO_HW_Bootcheck import HW_C
from gmail import mail
var1 = str('')
D_OLED = str('')
E_IO = str('')


def GScroll(text='', num_line=1, num_cols=20):
    if D_OLED == 1:
        if (len(text) > num_cols):
            display2.lcd2_display_string(text[:num_cols], num_line)
            time.sleep(1)
            for i in range(len(text) - num_cols + 1):
                text_to_print = text[i:i + num_cols]
                display2.lcd2_display_string(text_to_print, num_line)
                time.sleep(0.1)
            time.sleep(1)
        else:
            display2.lcd2_display_string(text, num_line)
    else:
        if (len(text) > num_cols):
            display.lcd_display_string(text[:num_cols], num_line)
            time.sleep(1)
            for i in range(len(text) - num_cols + 1):
                text_to_print = text[i:i + num_cols]
                display.lcd_display_string(text_to_print, num_line)
                time.sleep(0.2)
            time.sleep(1)
        else:
            display.lcd_display_string(text, num_line)

#ADO Name
print('ADO_NET ')
ado_ = os.uname()[1]
print('Unit Name', ado_)
print('ADO Revision ', rev)
f = open('/home/pi/Bellwether/ADO_Unit.py', "w")
f.write('ado_ ' + '= ' +'str'+'(' +"'"+ str(ado_) +"'" +')')
f.write('\n')
f.close()
import ADO_V
# Dual Display Detect
proc = subprocess.Popen('i2cdetect -y 1 %s' % (str(var1),), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()  # Read data from stdout and stderr

out = out [165:-309]
out = str(out)
if out == str(b'21'):
    f = open('/home/pi/Bellwether/ADO_D_OLED.py', "w")
    f.write('D_OLED = int (1)')
    f.write('\n')
    f.close()
    D_OLED = 1
    print('Dual Display ADO')
else:
    f = open('/home/pi/Bellwether/ADO_D_OLED.py', "w")
    f.write('D_OLED = int (0)')
    f.write('\n')
    f.close()
    D_OLED = 0
    print('Single Display ADO')

# Expanded IO
proc = subprocess.Popen('i2cdetect -y 1 %s' % (str(var1),), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
out, err = proc.communicate()  # Read data from stdout and stderr

# out = out [162:-312] # Address 0x20
out = out [168:-306] # Address 0x22
out = str(out)
if out == str(b'22'):
    f = open('/home/pi/Bellwether/ADO_E_IO.py', "w")
    f.write('E_IO = int (1)')
    f.write('\n')
    f.close()
    E_IO = 1
    print('Expanded IO (HVC) ADO')
else:
    f = open('/home/pi/Bellwether/ADO_E_IO.py', "w")
    f.write('E_IO = int (0)')
    f.write('\n')
    f.close()
    E_IO = 0
    print('Standard IO ADO')

if HW_C != 1:

    display = lcddriver.lcd()

    display.lcd_clear()
    display.lcd_display_string("Bellwether Co. ADO", 1)
    display.lcd_display_string('Network Check      ', 2)
    display.lcd_display_string(str(ado_), 3)
    display.lcd_display_string(str(rev), 4)


    time.sleep(20)

    import subprocess as sp
    output = sp.getoutput('iwgetid -r')
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    IP = ip_address
    print('IP Address ' + str(IP))



    display.lcd_clear()
    display.lcd_display_string(str(ado_), 1)
    display.lcd_display_string('SSID', 2)
    display.lcd_display_string(str(output), 3)
    display.lcd_display_string(str(IP), 4)

    if D_OLED == 1:
        display2 = lcddriver2.lcd2()
        display2.lcd2_clear()
        display2.lcd2_display_string(str(ado_), 1)
        display2.lcd2_display_string('SSID', 2)
        display2.lcd2_display_string(str(output), 3)
        display2.lcd2_display_string(str(IP), 4)

    now = datetime.datetime.now()
    ddate = (now.strftime("%m-%d-%Y"))
    ttime = (now.strftime("%H:%M:%S"))
    # mail.SendEmail(str(ado_) +' Reboot (Do Not Reply)', 'ADO Reboot on ' + str(ddate)+ ' at ' +
    # str(ttime) + ' With version '+ str(rev)) #todo enable after debug
    time.sleep(5)


