#!/usr/bin/env python
import ADO_V
import time
import datetime
import csv
import lcddriver2
import os
import sys
from ADO_Rev import rev
rev2 = rev [7:]
from ADO_Rev import ST1
from ADO_Rev import ST1_BW
from ADO_PN_Buf import prg
from ADO_Rev import debug
from ADO_Rev import db
from ADO_D_OLED import D_OLED
from ADO_E_IO import E_IO
from ADO_Unit import ado_
from ADO import ado
from ADO_Report import report
open_ = open('/home/pi/Bellwether/ADO_Tag.py', 'rt')
tag = open_.read()
open_.close()
button = int(0)

if ado_ == ('ADO5'):
    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
if ado_ == '':
    ado_ = str('NO_NAME')
    print('NO_NAME')
print (ado_)
#For DropBox
import dropbox
from dropbox.files import WriteMode
access_token = '6c3d849c913a11'

if debug == 1:
    ST1 = ST1_BW

device = str('Load')
ado.CDA()
ado.PNU_ISO()
latch = int(0)
if debug == 1:
    D_OLED = 0
    print('Debug via Rev.')
if D_OLED == 1:
    display2 = lcddriver2.lcd2()
opn = int(0)
cls = int(0)
cnt = int(0)
ssn = str('')
state = str('')
min_psi = int(0)
leak_psi = int(0)
hopper = int(0)
hopper2wire = int(0)
hopper3wire = int(0)
if debug == 1:
    print('Debug via Rev.')
else:
    timer = int(30)
OC_Timer = int(3)
BC_Check = int(0)
bt_time = int(1.5)
result = str('')
msg1 = str('')
msg2 = str('')
msg3 = str('')
msg4 = str('')
msg5 = str('')
note = str('')
buf = datetime.datetime.now()
stime = time.time()

ado.GDisplay('Bellwether Co. ADO', '', 'ADO Load', str(rev))

def Open():
    global opn
    global cls
    ado.OPN()
    time.sleep(OC_Timer)
    opn = ado.OPN_S()
    cls = ado.CLS_S()
def Close():
    global opn
    global cls
    ado.CLS()
    time.sleep(OC_Timer)
    opn = ado.OPN_S()
    cls = ado.CLS_S()
def Leak_Test():
    global timer
    global cnt
    global fail
    global res
    global button
    ado.OCO()
    time.sleep(10)
    ado.PNU_ISO()
    time.sleep(5)
    ado.OPN()
    time.sleep(1)
    ado.PNU_ISO()
    time.sleep(2)
    ado.PNU_ISO()
    ado.GDisplay('Bellwether Co. ADO', 'Leak Testing', '', str(rev))
    print('Leak Test ', timer)
    time.sleep(1)
    while timer != 0:
        ado.GDisplay_Cnt(str(timer))
        time.sleep(1)
        timer -= 1
        print('Leak Test ', timer)
        if timer == 9:
            ado.GDisplay('Bellwether Co. ADO', 'Leak Testing', '', str(rev))
            report.log('Blah', 'ADO_LOAD_DATA', device, 'N/A', '_Piston Ring', 'PASS', tag, ado_,
                       prg, BC, cnt, res, rev, fail)
    ado.GDisplay('Bellwether Co. ADO', 'Leak Testing', 'Complete', str(rev))
    ado.PNU_ISO()

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
        report.log('Blah', 'ADO_LOAD_DATA', device, 'N/A', '_Piston Ring', 'FAIL', tag, ado_,
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
        ado.B_Off()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
def Leak_Housing():
    global timer
    global cnt
    global fail
    global res
    global button
    button = 0
    print ('Leak Housing')
    test_timer = int(30)
    ado.OCOn()
    ado.CDA_(1)
    ado.PNU_ISO_(1)
    ado.GDisplay('ADO Pressurizing', 'Subassembly', 'Please Wait', str(rev))
    time.sleep(5)
    ado.GDisplay('ADO Subassembly', 'Housing Leak Test', '', str(rev))
    ado.CDA_(0)
    while test_timer != 0:
        print ('Housing Leak Test', test_timer)
        ado.GDisplay_Cnt(str(test_timer))
        ML = ado.Min_CDA()
        if test_timer == 9:
            ado.GDisplay('ADO Subassembly', 'Housing Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            ado.GDisplay('ADO Subassembly', 'Housing Leak Found', '', str(rev))
            report.log('Blah', 'ADO_LOAD_DATA', device, 'N/A', '_Housing Leak', 'FAIL', tag, ado_,
                       prg, BC, cnt, res, rev, fail)
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_Load.py', "w")
            f.write('cnt ' + '= ' + str(cnt))
            f.write('\n')
            f.write('ssn ' + '= ' + "'" + str(BC) + "'")
            f.write('\n')
            f.write('res ' + '= ' + str(res))
            f.write('\n')
            f.write('fail ' + '= ' + str(fail))
            f.write('\n')
            if hall == 1:
                f.write('hall ' + '= ' + str(1))
                f.close()
            else:
                f.write('hall ' + '= ' + str(0))
                f.close()
            ado.CDA_(0)
            ado.PNU_ISO_(0)
            ado.OCO()
            while button != 1:
                ado.B_Red()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
            ado.B_Off()
            ado.OCO()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1

    ado.GDisplay('ADO External', 'Leak Test', 'PASS', str(rev))
    report.log('Blah', 'ADO_LOAD_DATA', device, 'Subassembly Leak', '_Housing Leak', 'PASS', tag, ado_,
               prg, BC, cnt, res, rev, fail)
time.sleep(2)

while BC_Check != 1:
    ado.GDisplay('Enter Serial #', 'Barcode', '', str(rev))
    ado.B_Yellow()
    BC = input("Enter SN Barcode ") #todo Enable after debug
    # BC = ('2222') #todo Remove after debug
    # BC = ('0000') #todo Remove after debug
    if BC == str('0000'):
        BC == str('debug')
        debug = 1
        timer = int(60) # debug leak timer
        ST1 = ST1_BW
        print('Debug Enabled via SSN')
    ado.B_Off()
    if prg == BC:
        ado.GDisplay('Bellwether Co. ADO', 'Invalid Serial #', '', str(rev))
        ado.B_Red()
        time.sleep(5)
        ado.B_Off()
        time.sleep(1)
    else:
        ado.GDisplay('', '', str(BC), '')
        time.sleep(1)
        ado.GDisplay('Begin Testing', '', '', '')
        BC_Check += 1

ado.GDisplay('Begin Testing', '', '', '')

from ADO_ODO_Load import ssn
from ADO_ODO_Load import cnt
from ADO_ODO_Load import res
from ADO_ODO_Load import fail
from ADO_ODO_Load import hall

if BC == ssn:
    print("Yes")
    f = open('/home/pi/Bellwether/ADO_ODO_Load.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' + "'" + str(BC) + "'")
    f.write('\n')
    f.write('res ' + '= ' + str(res))
    f.write('\n')
    f.write('fail ' + '= ' + str(fail))
    f.write('\n')
    if hall == 1:
        f.write('hall ' + '= ' + str(1))
        f.close()
    else:
        f.write('hall ' + '= ' + str(0))
        f.close()
else:
    print("No")
    cnt = 0
    res = 0
    fail = 0
    hall = 0

    # CSV Header
    report.log_h('Self', 'ADO_SLT_DATA', device, BC)
    f = open('/home/pi/Bellwether/ADO_ODO_Load.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' + "'" + str(BC) + "'")
    f.write('\n')
    f.write('res ' + '= ' + str(res))
    f.write('\n')
    f.write('fail ' + '= ' + str(fail))
    f.write('\n')
    if hall == 1:
        f.write('hall ' + '= ' + str(1))
        f.close()
    else:
        f.write('hall ' + '= ' + str(0))
        f.close()


ado.GDisplay('Bellwether Co. ADO', 'Press Button', 'To Start', str(rev))

if debug == 1:
    button = 1
while button == 0:
    ado.B_Green()
    time.sleep(.5)
    ado.B_Off()
    time.sleep(.5)
    button = ado.BTN()

ado.B_Off()
button = 0

if debug == 1:
    print('No Hall Debug')
else:
    if hall == 0:
        ado.GDisplay('Bellwether Co. ADO', 'ADO Hall ADJ (CLS)', 'Press Green', 'Button to Start')
        time.sleep(1)
        while button != 1:
            ado.B_Green()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        ado.B_Off()
        button = 0
        Close()
        ado.GDisplay('Adjust Close Hall', 'Press Green Button', 'When', 'Complete')
        time.sleep(1)


        # Close Hall feedback
        while button != 1:
            if ado.CLS_S() == 1:
                ado.B_Green()
            else:
                ado.B_Off()
            button = ado.BTN()
        ado.B_Off()
        button = 0
        print("Hall Close PASS")
        ado.GDisplay('Hall Adjustment', '', 'Complete', '')

        if hall == 0:
            ado.GDisplay('Bellwether Co. ADO', 'ADO Hall ADJ (OPN)', 'Press Green', 'Button to Start')
            time.sleep(1)
            while button != 1:
                ado.B_Green()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
            ado.B_Off()
            button = 0
            Open()
            ado.GDisplay('Adjust Open Hall', 'Press Green Button', 'When', 'Complete')
            time.sleep(1)

        # Open Hall feedback
        while button != 1:
            if ado.OPN_S() == 1:
                ado.B_Green()
            else:
                ado.B_Off()
            button = ado.BTN()
        ado.B_Off()
        button = 0
        print("Hall Open PASS")
        ado.GDisplay('Hall Adjustment', '', 'Complete', '')
        time.sleep(1)


        hall = 1

if debug == 1:
    print('No Hopper Test Debug')
else:
    if hopper == 0:
        ado.B_Yellow()
        ado.GDisplay('Bellwether Co. ADO', 'Insert Hopper', '', str(rev))
    while hopper == 0:
        ado.B_Yellow()
        time.sleep(.5)
        ado.B_Off()
        time.sleep(.5)

        if ado.SHOPS() == 1:
            hopper3wire = 1
        print('3 wire', hopper3wire)
        if hopper3wire == 1:
            hopper = 1
    print('Button', button)
    time.sleep(2)
    ado.GDisplay('Bellwether Co. ADO', 'ADO Load', 'Shoe Door', 'Test')
    time.sleep(1)


    # Shoe Door Q&A
    ado.Mag()
    while ado.BTN() == 0:
        ado.B_Green()
        ado.GDisplay('Did shoe door open?', 'If "Yes" press', 'Green Button', str(rev))
        time.sleep(bt_time)
        ado.B_Off()
        if ado.BTN() == 1:
            ado.B_Off()
        else:
            ado.B_Red()
            ado.GDisplay('Did shoe door open?', 'If "No" press', 'Red Button', str(rev))
            time.sleep(bt_time)
            ado.B_Off()
            if ado.BTN() == 1:
                print("Shoe Door Not Close")
                cnt += 1
                fail += 1
                res += 1
                print('cnt', cnt)
                print('fail', fail)
                print('res', res)
                report.log('Blah', 'ADO_LOAD_DATA', device, 'N/A', '_Shoe Door open FAILURE', 'FAIL', tag, ado_,
                           prg, BC, cnt, res, rev, fail)
                print("Press Reset")
                ado.GDisplay('Bellwether Co. ADO', 'Shoe Door Open Failure', 'Press Reset', str(rev))
                while button != 1:
                    ado.B_Red()
                    time.sleep(.5)
                    ado.B_Off()
                    time.sleep(.5)
                    button = ado.BTN()
                # GPIO.cleanup()
                ado.B_Off()
                os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])


#Open
min_psi = ado.Min_CDA() # Added for small volume compressor
while ST1 != 0:
    # min_psi = ado.Min_CDA() # Removed for small volume compressor
    if min_psi == 0:
        cnt += 1
        fail += 1
        res += 1
        print("Bellow 100 PSI")
        report.log('Blah', 'ADO_LOAD_DATA', device, 'N/A', '_Main Pressure Low', 'FAIL', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
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
        # GPIO.cleanup()
        ado.B_Off()
        ado.CLS()
        time.sleep(1)
        ado.OCO()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    ado.GDisplay('Bellwether Co. ADO', 'ADO Load Count', str(cnt), str(rev))
    Open()
    if cls != 0:
        print('CLS sensor state not  changed')
        report.log('Blah', 'ADO_LOAD_DATA', device, 'N/A', '_CLS Sensor State', 'FAIL', tag, ado_,
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
        # GPIO.cleanup()
        ado.B_Off()
        ado.CLS()
        time.sleep(1)
        ado.OCO()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    if opn != 1:
        cnt += 1
        fail += 1
        res += 1
        print("Fail Open")
        report.log('Blah', 'ADO_LOAD_DATA', device, 'N/A', '_Open Failure', 'FAIL', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
        ado.GDisplay('Bellwether Co. ADO', 'Open Fail!', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        # GPIO.cleanup()
        ado.B_Off()
        ado.CLS()
        time.sleep(1)
        ado.OCO()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])


    # Close
    # min_psi = ado.Min_CDA() # Removed for small volume compressor
    if min_psi == 0:
        cnt += 1
        fail += 1
        res += 1
        print("Bellow 100 PSI")
        report.log('Blah', 'ADO_LOAD_DATA', device, 'N/A', '_Main Pressure Low', 'FAIL', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
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
        # GPIO.cleanup()
        ado.B_Off()
        ado.CLS()
        time.sleep(1)
        ado.OCO()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    # Close
    ado.B_Off()
    Close()
    if opn != 0:
        print('OPN sensor state not  changed')
        report.log('Blah', 'ADO_LOAD_DATA', device, 'N/A', 'OPN Sensor State', 'FAIL', tag, ado_,
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
        ado.B_Off()
        ado.CLS()
        time.sleep(1)
        ado.OCO()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    if cls != 1:
        cnt += 1
        fail += 1
        res += 1
        print("Fail Close")
        report.log('Blah', 'ADO_LOAD_DATA', device, 'N/A', '_Close Failure', 'FAIL', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
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
        # GPIO.cleanup()
        ado.B_Off()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    report.log('Blah', 'ADO_LOAD_DATA', device, 'N/A', 'PASS', 'PASS', tag, ado_,
               prg, BC, cnt, res, rev, fail)
    time.sleep(1)
    cnt += 1
    ST1 -= 1




print(cnt)
ado.GDisplay('Bellwether Co. ADO', 'ADO Load Count', str(cnt), str(rev))

#Leak Test
Leak_Test() #todo enable after debug
Leak_Housing()



print('Leak Test Complete')
report.log('Blah', 'ADO_LOAD_DATA', device, 'N/A', 'PASS', 'PASS', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
report.mlog('Blah','ADO_MASTER_LIST_DATA', device, 'N/A', 'PASS', 'PASS', tag, ado_, prg, BC, cnt, res, rev)


('ADO_LOAD_DATA', 'Load', 'N/A', 'PASS', 'PASS')

if ST1 == 0:
    f = open('/home/pi/Bellwether/ADO_ODO_Load.py', "w")
    f.write('cnt = 0')
    f.write('\n')
    f.write('ssn = ""')
    f.write('\n')
    f.write('res = 0')
    f.write('\n')
    f.write('fail = 0')
    f.write('\n')
    f.write('hall ' + '= ' + str(0))
    f.write('\n')
    f.close()
ado.OCO()

time.sleep(1)
ado.PNU_ISO()
ado.B_Off()
ado.GDisplay('Bellwether Co. ADO', '"Pass" Test Complete', str(cnt), str(rev))
print('Test Complete')
ado.PNU_ISO()
time.sleep(1)
ado.B_Off()

Open()

if debug == 1:
    button = 1

while button == 0:
    ado.B_Green()
    time.sleep(.5)
    ado.B_Off()
    time.sleep(.5)
    button = ado.BTN()
ado.B_Off()
button = 0
ado.GDisplay_CLR()
time.sleep(1)
os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
# GPIO.cleanup()
