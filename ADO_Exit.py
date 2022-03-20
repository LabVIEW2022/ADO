#!/usr/bin/env python
# Rev 1b
import ADO_V
import time
import datetime
import csv
import lcddriver2
import os
import RPi.GPIO as GPIO
import pifacedigitalio as p
import sys
from ADO_Decoder import Encoder
enc = Encoder(18, 17)
from ADO_Report import report
from ADO_Unit import ado_
from ADO import ado
open_ = open('/home/pi/Bellwether/ADO_Tag.py', 'rt')
tag = open_.read()
open_.close()

if ado_ == ('ADO5'):
    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
if ado_ == '':
    ado_ = str('NO_NAME')
    print('NO_NAME')
from ADO_Rev import rev
rev2 = rev [7:]
from ADO_Rev import ST3
ST_buf = ST3
from ADO_Rev import ST3_BW
from ADO_PN import BC_Exit
from ADO_PN_Buf import prg
from ADO_Rev import debug
from ADO_Rev import db
from ADO_D_OLED import D_OLED
from ADO_E_IO import E_IO

from ADO_ODO_Exit import ssn
from ADO_ODO_Exit import cnt
from ADO_ODO_Exit import res
from ADO_ODO_Exit import fail
hall = int(1) # to bypass hall adjust


#For DropBox
import dropbox
from dropbox.files import WriteMode
access_token = '6c3d849c913a11'

if debug == 1:
    D_OLED = 0
    ST3 = ST3_BW

    print('Debug via Rev.')
p.init()

ado.CDA_(1)
ado.PNU_ISO_(1)
ado.CDA_(1)

latch = int(0)
button = int(0)
if D_OLED == 1:
    display2 = lcddriver2.lcd2()
opn = int(0)
cls = int(0)
cnt = int(0)
min_psi = int(0)
leak_psi = int(0)
hopper = int(0)
if debug == 1:
    timer = int(5)
else:
    timer = int(30)
    timer2 = int(30)
BC_Check = int(0)
bt_time = int(1.5)
OC_Time = int(5)
buf = datetime.datetime.now()
stime = time.time()
device = str('Exit')
state = str('')
note = str('')


def Open():
    global opn
    global cls
    ado.OPN() # Exit Open
    time.sleep(OC_Time)
    # opn = ado.OPN_S()
    cls = ado.CLS_S()
def Close():
    global opn
    global cls
    ado.CLS() # Exit Close
    time.sleep(OC_Time)
    # opn = ado.OPN_S()
    cls = ado.CLS_S()
def Leak_Test():
    global timer
    global timer2
    global cnt
    global fail
    global res
    global button
    ado.OCO()
    ado.PNU_ISO_(1)
    time.sleep(5)
    ado.PNU_ISO_(0)
    time.sleep(5)
    ado.OPN()
    time.sleep(1)
    ado.PNU_ISO_(1)
    time.sleep(2)
    ado.PNU_ISO_(0)
    ado.GDisplay('Bellwether Co. ADO', 'Leak Testing  A', '', str(rev))
    print('Leak Test ', timer)
    time.sleep(1)
    while timer != 0:
        ado.GDisplay_Cnt(str(timer))
        time.sleep(1)
        timer -= 1
        print('Leak Test ', timer)
        if timer == 9:
            ado.GDisplay('Bellwether Co. ADO', 'Leak Testing  A', '', str(rev))

    leak_psi = ado.Leak_S()
    if leak_psi == 0:
        cnt += 1
        fail += 1
        res += 1
        ado.CLS()
        time.sleep(1)
        ado.OCO()
        print("Cylinder Leak")
        state = ('_Cylinder Leak')
        report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_Piston Ring A', 'Fail', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
        ado.GDisplay('Bellwether Co. ADO', 'Pressure Leak!', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        GPIO.cleanup()
        ado.B_Off()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    else:
        report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_Piston Ring A', 'PASS', tag, ado_,
                   prg, BC, cnt, res, rev, fail)

    # Side B Cylinder leak Test
    ado.B_Off()
    ado.CDA_(0)
    ado.CDA_(0)
    ado.PNU_ISO_(0)
    time.sleep(2)
    ado.CLS()
    ado.CDA_(1)
    ado.PNU_ISO_(1)
    time.sleep(5)
    ado.CDA_(0)
    ado.PNU_ISO_(1)

    ado.GDisplay('Bellwether Co. ADO', 'Leak Testing  B', '', str(rev))
    while timer2 != 0:
        ado.GDisplay_Cnt(str(timer2))
        time.sleep(1)
        timer2 -= 1
        print('Leak Test ', timer2)
        if timer2 == 9:
            ado.GDisplay('Bellwether Co. ADO', 'Leak Testing  B', '', str(rev))
    leak_psi = ado.Min_CDA()
    if leak_psi == 0:
        cnt += 1
        fail += 1
        res += 1
        ado.CLS()
        time.sleep(1)
        ado.OCO()
        print("Cylinder Leak")
        state = ('_Cylinder Leak')
        report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_Piston Ring B', 'Fail', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
        ado.GDisplay('Bellwether Co. ADO', 'Pressure Leak!', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        GPIO.cleanup()
        ado.B_Off()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_Piston Ring B', 'PASS', tag, ado_,
               prg, BC, cnt, res, rev, fail)
    ado.PNU_ISO_(1)
def Leak_Housing():
    global fail, res
    print ('Leak Housing')
    test_timer = int(30)
    ado.CDA_(1) # Open
    ado.PNU_ISO_(1) # Open
    ado.OPN()
    ado.CLS()
    ado.GDisplay('ADO Pressurizing', 'Subassembly', 'Please Wait', str(rev))
    time.sleep(5)
    ado.GDisplay('ADO Subassembly', 'Housing Leak Test', '', str(rev))
    ado.CDA_(0) # Close
    while test_timer != 0:
        print ('Housing Leak Test', test_timer)
        ado.GDisplay_Cnt(str(test_timer))
        ML = GPIO.input(5)
        if test_timer == 9:
            ado.GDisplay('ADO Subassembly', 'Housing Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            ado.GDisplay('ADO Subassembly', 'Housing Leak Found', '', str(rev))
            report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_housing Leak', 'FAIL', tag, ado_,
                       prg, BC, cnt, res, rev, fail)

            ado.CDA_(0)  # Close
            ado.PNU_ISO_(0)  # Close
            ado.OCO()
            while button != 1:
                ado.B_Red()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
            ado.CDA_(0)  # Close
            ado.PNU_ISO_(0)  # Close
            GPIO.cleanup()
            ado.B_Off()
            ado.V24Off()
            ado.OCO()
            # GPAp1.value = True # Missing import
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1
    ado.CDA_(1)
    ado.OCO()
    ado.GDisplay('ADO External', 'Leak Test', 'PASS', str(rev))
    report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_Housing Leak', 'PASS', tag, ado_,
               prg, BC, cnt, res, rev, fail)

ado.GDisplay('Bellwether Co. ADO', 'ADO Cooling Tray', '', str(rev))
time.sleep (2)
while BC_Check != 1:
    ado.GDisplay('Enter Serial #', 'Barcode', '', str(rev))
    ado.B_Green()
    ado.B_Red()
    BC = input('Enter SN Barcode ') # todo re enable after debug
    # BC = str('1112') # todo remove after debug
    ado.GDisplay_CLR()
    if BC == str('0000'):
        debug = 1
        timer = int(5)
        ST3 = ST3_BW
        print('Debug Enabled via SSN')
    ado.OCO()
    ado.B_Off()
    if prg == BC:
        ado.GDisplay('Bellwether Co. ADO', 'Invalid Serial #', '', str(rev))
        ado.B_Red()
        time.sleep(5)
        ado.B_Off()
        time.sleep(1)
    else:
        # ado.GDisplay('Begin Testing', '', '', '')
        BC_Check += 1
# ado.GDisplay('Begin Testing', '', '', '')

if BC == ssn:
    print("Yes")
    f = open('/home/pi/Bellwether/ADO_ODO_Exit.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' +"'" + str(BC) + "'")
    f.write('\n')
    f.write('res ' + '= ' + str(res))
    f.write('\n')
    f.write('fail ' + '= ' + str(fail))
    f.write('\n')
else:
    print("No")
    cnt = 0
    res = 0
    fail = 0
    # hall = 0
    report.log_h('Self', 'ADO_EXIT_DATA', device, BC)
if debug == 1:
    button = 1
ado.OCO()
button = 0




button = 0
ado.GDisplay('Bellwether Co. ADO', 'Press Button', 'To Start', str(rev))
ado.CDA_(1)
while button == 0:
    ado.B_Green()
    time.sleep(.5)
    ado.OCO()
    time.sleep(.5)
    button = ado.BTN()
ado.OCO()
button = 0

# Agitator Test
ado.OCO()

if debug == 1:
    print('No Agitator Debug')
else:
    print("Agitator Test")
    ado.GDisplay('Bellwether Co. ADO', 'Agitator Test', 'Please Wait....', str(rev))
    time.sleep(2)
    enc.zero()
    pre_enc = enc.read()
    ado.V24A()
    time.sleep(2)
    ado.V24Off()
    pos_enc = enc.read()
    enc_enc = pos_enc - pre_enc
    if enc_enc >= 15000:
        ado.GDisplay('Agitator', 'Pass', '', '')
        time.sleep(2)
        ado.GDisplay('', '', '', '')
        report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_Agitator', 'PASS', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
    else:
        cnt += 1
        fail += 1
        res += 1
        print('cnt', cnt)
        print('fail', fail)
        print('res', res)
        report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_Agitator FAILURE', 'FAIL', tag, ado_,
                   prg, BC, cnt, res, rev, fail)

        print("Press Reset")
        ado.GDisplay('Bellwether Co. ADO', 'Agitator Failure', 'Press Reset', str(rev))

        button = 0
        if debug == 1:
            button = 1
        while button != 1:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        GPIO.cleanup()
        ado.B_Off()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    print('Agitator PASS')

#Open
button = 0
while ST3 != 0:
    if ado.Min_CDA() == 0:
        cnt += 1
        fail += 1
        res += 1
        print("Bellow 100 PSI")
        report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_Main Pressure Low', 'FAIL', tag, ado_,
                   prg, BC, cnt, res, rev, fail)

        button = 0
        print("Press Reset")
        ado.GDisplay('Bellwether Co. ADO', 'Bellow 100 PSI', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        GPIO.cleanup()
        ado.B_Off()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])



    # Open
    ado.GDisplay('Bellwether',
             'ADO Exit Count',
             str(cnt),
             str(rev))

    Open()
    if cls != 0:
        print('CLS sensor state not  changed')
        report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_CLS Sensor State', 'FAIL', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
        ado.GDisplay('Bellwether Co. ADO', 'CLS State', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        GPIO.cleanup()
        ado.B_Off()
        ado.OCO()
        ado.CLS()
        time.sleep(1)
        ado.OCO()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        if debug == 1:
            button = 1
        print("Press Reset")
        ado.GDisplay('Bellwether Co. ADO', 'Open Fail!', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        GPIO.cleanup()
        ado.B_Off()
        ado.OCO()
        ado.CLS()
        time.sleep(1)
        ado.OCO()

        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    #Close
    min_psi = GPIO.input(5)
    # min_psi = 1 #Min Psi Bypass
    if min_psi == 0:
        cnt += 1
        fail += 1
        res += 1
        print("Bellow 100 PSI")
        report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_Main Pressure Low', 'FAIL', tag, ado_,
                   prg, BC, cnt, res, rev, fail)

        print("Press Reset")
        button = 0
        ado.GDisplay('Bellwether Co. ADO', 'Bellow 100 PSI', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            ado.B_Red()
            time.sleep(.5)
            e
            button = ado.BTN()
        GPIO.cleanup()
        ado.B_Off()
        ado.OCO()
        ado.CLS()
        time.sleep(1)
        ado.OCO()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    #Close
    ado.B_Off()
    ado.OCO()
    Close()
    print('Open', opn)
    print('Close', cls)
    if opn != 0:
        print('OPN sensor state not  changed')
        report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_OPN Sensor State', 'FAIL', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
        ado.GDisplay('Bellwether Co. ADO', 'OPN State', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        GPIO.cleanup()
        ado.B_Off()
        ado.OCO()
        ado.CLS()
        time.sleep(1)
        ado.OCO()

        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    if cls != 1:
        cnt += 1
        fail += 1
        res += 1
        print("Fail Close")

        report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_Close Failure', 'FAIL', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
        button = 0
        print("Press Reset")
        ado.GDisplay('Bellwether Co. ADO', 'Close Fail!', 'Press Reset', str(rev))

        if debug == 1:
            button = 1
        while button != 1:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        GPIO.cleanup()
        ado.OCO()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', '_Cycle', 'PASS', tag, ado_,
               prg, BC, cnt, res, rev, fail)
    time.sleep(2)
    cnt += 1
    ST3 -= 1
    print(cnt)
    ado.GDisplay('Bellwether',
             'ADO Exit Count',
             str(cnt),
             str(rev))





#Leak Test
Leak_Test()
Leak_Housing()

report.log('Blah', 'ADO_EXIT_DATA', device, 'N/A', 'PASS', 'PASS', tag, ado_,
               prg, BC, cnt, res, rev, fail)
report.mlog('Blah','ADO_MASTER_LIST_DATA', device, 'N/A', 'TEST', 'PASS', tag, ado_, prg, BC, cnt, res, rev)

if ST3 == 0:
    f = open('/home/pi/Bellwether/ADO_ODO_Exit.py', "w")
    f.write('cnt = 0')
    f.write('\n')
    f.write('ssn = ""')
    f.write('\n')
    f.write('res = 0')
    f.write('\n')
    f.write('fail = 0')
    f.write('\n')
    f.write('hall = 0')
    f.write('\n')
    f.close()

ado.OCO()
ado.CLS()
time.sleep(1)
ado.OCO()
ado.PNU_ISO_(1)
ado.B_Off()
ado.GDisplay('Bellwether Co. ADO',
             '"Pass" Test Complete',
             '',
             str(rev))
time.sleep(1)
ado.B_Off()
ado.OCO()

if debug == 1:
    button = 1
while button == 0:
    ado.B_Green()
    time.sleep(.5)
    ado.B_Off()
    time.sleep(.5)
    button = ado.BTN()
ado.OCO()
button = 0
ado.GDisplay('','','','')
time.sleep(1)
# os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
GPIO.cleanup()
