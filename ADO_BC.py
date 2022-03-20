#!/usr/bin/env python
import lcddriver
import time
import os
import sys
display = lcddriver.lcd()
import pifacedigitalio as p
p.init()
import datetime
import csv
#CLS PN
from ADO_PN import BC_Drum_Assembly
from ADO_PN import BC_Drop
from ADO_PN import BC_PNU_Drop
from ADO_PN import BC_Exit
from ADO_PN import BC_Exhaust
from ADO_PN import BC_Panel

#BW PN
from ADO_PN import BC_Drum_ssembly_BW
from ADO_PN import BC_Drop_BW
from ADO_PN import BC_PNU_Drop_BW
from ADO_PN import BC_Exit_BW
from ADO_PN import BC_Exhaust_BW
from ADO_PN import BC_Panel_BW

from ADO_Rev import rev
from ADO_Unit import ado_

ttime = int(5)
button = int(0)
bc_cnt = int()
Label = str('')
PLabel = str('')
BCode = str('')
device = str('Panel')
cnt = int(0)
res = int(0)
db = int(0)

buf = datetime.datetime.now()
stime = time.time()

def Screen (PLabel):
    p.digital_write(6, 0)
    p.digital_write(7, 1)
    time.sleep(.5)
    display.lcd_clear()
    display.lcd_display_string(PLabel, 1)
    display.lcd_display_string('Press Button', 2)
    display.lcd_display_string('To Start', 3)
    display.lcd_display_string(str(rev), 4)
def BC (Label):
    global BCode
    ttime = 5
    while ttime != 0:
        button = p.digital_read(7)  # todo change to '7' after debug
        if button == 1:
            display.lcd_clear()
            display.lcd_display_string(Label, 1)
            display.lcd_display_string(str(rev), 4)
            prg = input("Enter Barcode ")
            bc_cnt = len(prg)
            while bc_cnt != 13:
                display.lcd_clear()
                display.lcd_display_string("Bellwether Co. ADO", 1)
                display.lcd_display_string('Invalid PN          ', 2)
                display.lcd_display_string(str(rev), 4)
                time.sleep(5)
                display.lcd_clear()
                display.lcd_display_string(Label, 1)
                display.lcd_display_string(str(rev), 4)
                prg = input("Enter Barcode ")
                bc_cnt = len(prg)
            BCode = prg[:-4]
            display.lcd_display_string(str(prg), 2)
        time.sleep(.5)
        ttime -= 1
    p.digital_write(7, 0)
    time.sleep(.5)
    ttime = 5
def ulog(note, state, result):
    rev2 = rev [8:]
    buf = datetime.datetime.now()
    global etime
    import time
    end = time.time()
    hours, rem = divmod(end - stime, 3600)
    minutes, seconds = divmod(rem, 60)
    etime = ("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
    with open('/home/pi/Bellwether/' + str(ado_) + '_' + 'Useage_Log.csv', mode='a') as Test_file: # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([buf, ado_, device, 'N/A', cnt, res, note, state, result, rev2, etime])
        Test_file.flush()
    if db == 1:
        display.lcd_clear()
        display.lcd_display_string("Bellwether Co. ADO", 1)
        display.lcd_display_string('Upload to DB          ', 2)
        display.lcd_display_string(str(rev), 4)
        file_name = (str(ado_) + '_' + 'Useage_Log.csv')
        dropbox_path = '/ADO_Log/'
        dbx = dropbox.Dropbox('TYQkL_IX4lAAAAAAAAABrz9rDoR4S3zXJgLYqiREuqOAVmUK4vvAiEUWVY9LII22')
        with open(file_name, 'r+') as f:
            dbx.files_upload(f.read(), dropbox_path + file_name, mode=dropbox.files.WriteMode.overwrite, mute=True)
# Button UI
display.lcd_clear()
display.lcd_display_string("PN# Barcode Change", 1)
display.lcd_display_string('Press Button', 2)
display.lcd_display_string('To Start', 3)
display.lcd_display_string(str(rev), 4)
p.digital_write(6, 1)
p.digital_write(7, 1)

while button != 1:
    button = p.digital_read(7)

Screen ('Change Load BC?')
BC('Scan Load BC')
if BCode != '':
    Drum_Assembly = BCode
    ulog('Load BC Change', 'PASS', 'PASS')
BCode = ''

Screen ('Change Drop BC?')
BC('Scan Drop BC')
if BCode != '':
    BC_Drop = BCode
    ulog('Drop BC Change', 'PASS', 'PASS')
BCode = ''

Screen ('Change PNU Drop BC?')
BC('Scan PNU Drop BC')
if BCode != '':
    BC_PNU_Drop = BCode
    ulog('PNU Drop BC Change', 'PASS', 'PASS')
BCode = ''

Screen ('Change Exit BC?')
BC('Scan Exit BC')
if BCode != '':
    BC_Exit = BCode
    ulog('Exit BC Change', 'PASS', 'PASS')
BCode = ''

Screen ('Change Exhaust BC?')
BC('Scan Exhaust BC')
if BCode != '':
    BC_Exit = BCode
    ulog('Exhaust', 'PASS', 'PASS')
BCode = ''

Screen ('Change EE Panel BC?')
BC('Scan EE Panel BC')
if BCode != '':
    BC_Panel = BCode
    ulog('EE Panel BC Change', 'PASS', 'PASS')
BCode = ''

ttime = 5
display.lcd_clear()
display.lcd_display_string("Barcode Change", 1)
display.lcd_display_string('Complete', 2)
display.lcd_display_string('Rebooting....', 3)
display.lcd_display_string(str(rev), 4)
p.digital_write (6, 1)
time.sleep(.5)



f = open('/home/pi/Bellwether/ADO_PN.py', "w")
f.write('# CLS PN')
f.write('\n')
f.write('Drum_Assembly ' + '= ' +'str'+'(' +"'"+ str(Drum Assembly) +"'" +')')
f.write('\n')
f.write('BC_Drop ' + '= ' +'str'+'(' +"'"+ str(BC_Drop) +"'" +')')
f.write('\n')
f.write('BC_PNU_Drop ' + '= ' +'str'+'(' +"'"+ str(BC_PNU_Drop) +"'" +')')
f.write('\n')
f.write('BC_Exit ' + '= ' +'str'+'(' +"'"+ str(BC_Exit) +"'" +')')
f.write('\n')
f.write('BC_Exhaust ' + '= ' +'str'+'(' +"'"+ str(BC_Exhaust) +"'" +')')
f.write('\n')
f.write('BC_Panel ' + '= ' +'str'+'(' +"'"+ str(BC_Panel) +"'" +')')
f.write('\n')
f.write('\n')
f.write('\n')
f.write('\n')
f.write('# BW PN')
f.write('\n')
f.write('Drum Assembly_BW ' + '= ' +'str'+'(' +"'"+ str(Drum Assembly_BW) +"'" +')')
f.write('\n')
f.write('BC_Drop_BW ' + '= ' +'str'+'(' +"'"+ str(BC_Drop_BW) +"'" +')')
f.write('\n')
f.write('BC_PNU_Drop_BW ' + '= ' +'str'+'(' +"'"+ str(BC_PNU_Drop_BW) +"'" +')')
f.write('\n')
f.write('BC_Exit_BW ' + '= ' +'str'+'(' +"'"+ str(BC_Exit_BW) +"'" +')')
f.write('\n')
f.write('BC_Exhaust_BW ' + '= ' +'str'+'(' +"'"+ str(BC_Exhaust_BW) +"'" +')')
f.write('\n')
f.write('BC_Panel_BW ' + '= ' +'str'+'(' +"'"+ str(BC_Panel_BW) +"'" +')')
f.write('\n')
f.close()

time.sleep(5)
p.digital_write(6, 0)
# os.execv('/home/pi/Bellwether/ADO_UI.py', sys.argv) #todo re enable after debug
os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])


print('Barcode change complete.')