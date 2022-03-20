#!/usr/bin/env python
import ADO_V
import time
import datetime
import csv
import lcddriver2
import os
import sys
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
from ADO_Rev import ST2
from ADO_Rev import ST2_BW
from ADO_PN_Buf import prg
from ADO_Rev import debug
from ADO_Rev import db
from ADO_D_OLED import D_OLED
from ADO_Report import report
dchk = int(0)
Drop_Type = int(3)



#For DropBox
import dropbox
from dropbox.files import WriteMode
access_token = '6c3d849c913a11'

if debug == 1:
    D_OLED = 0
    ST2 = ST2_BW

if debug == 1:
    timer = int(5)
else:
    timer = int(30)
    timer2 = int(30)
buf = datetime.datetime.now()
stime = time.time()
device = str('PNU Drop')
state = str('')

ado.CDA_(1)
ado.PNU_ISO_(1)

latch = int(0)
button = int(0)
if D_OLED == 1:
    display2 = lcddriver2.lcd2()


opn = int(0)
cls = int(0)
cnt = int(0)
ssn = str("")
min_psi = int(0)
leak_psi = int(0)
hopper = int(0)
note = str('')
BC_Check = int(0)
bt_time = int(1.5)
switch_delay = int(5)


def Open():
    global opn
    global cls
    print('Open')
    ado.OPN()
    time.sleep(switch_delay)
    opn = ado.OPN_S()
    cls = ado.CLS_S()
    print('Open', opn)
    print('Close', cls)
def Close():
    global opn
    global cls
    print('Close')
    ado.CLS()
    time.sleep(switch_delay)
    opn = ado.OPN_S()
    cls = ado.CLS_S()
    print('Open', opn)
    print('Close', cls)
def Leak_Test():
    global timer
    global timer2
    global cnt
    global fail
    global res
    global button
    ado.OCO()
    ado.PNU_ISO_(1)
    ado.GDisplay('Bellwether Co. ADO', 'Leak Testing A', '', str(rev))
    time.sleep(10)
    ado.PNU_ISO_(0)
    time.sleep(5)
    ado.OPN()
    time.sleep(1)
    ado.PNU_ISO_(1)
    time.sleep(2)
    ado.PNU_ISO_(0)

    print('Leak Test ', timer)
    time.sleep(1)
    while timer != 0:
        display.lcd_display_string(str(timer), 3)
        time.sleep(1)
        timer -= 1
        print('Leak Test ', timer)
        if timer == 9:
            ado.GDisplay('Bellwether Co. ADO', 'Leak Testing A', '', str(rev))

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
        report.log('Blah', 'ADO_PNU_DROP_DATA', device, '_Piston Ring A', 'N/A', 'FAIL', tag, ado_,
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
        ado.BTN()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    else:
        log('ADO_PNU_DROP_DATA', 'PNU_DROP', '_Piston Ring A', 'N/A' , 'PASS')
        report.log('Blah', 'ADO_PNU_DROP_DATA', device, '_Piston Ring A', 'N/A', 'FAIL', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
    # Side B Cylinder leak Test
    ado.OCO()
    ado.CDA_(0)
    ado.PNU_ISO_(0)
    time.sleep(2)
    ado.CLS()
    ado.CDA_(1)
    ado.PNU_ISO_(1)
    time.sleep(5)
    ado.CDA_(0)
    ado.PNU_ISO_(1)

    ado.GDisplay('Bellwether Co. ADO', 'Leak Testing B', '', str(rev))
    while timer2 != 0:
        display.lcd_display_string(str(timer2), 3)
        time.sleep(1)
        timer2 -= 1
        print('Leak Test ', timer2)
        if timer2 == 9:
            ado.GDisplay('Bellwether Co. ADO', 'Leak Testing B', '', str(rev))
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
        log('ADO_PNU_DROP_DATA', 'PNU_DROP', '_Piston Ring B', 'N/A' , 'FAIL')
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
    else:
        log('ADO_PNU_DROP_DATA', 'PNU_DROP', '_Piston Ring B', 'N/A' , 'PASS')
    ado.PNU_ISO_(1)
def Leak_Housing():
    global fail
    global res
    global button
    print ('Leak Housing')
    test_timer = int(30)
    ado.CDA_(1)
    ado.PNU_ISO_(1)
    ado.OCOn()
    ado.GDisplay('ADO Pressurizing', 'Subassembly', 'Please Wait', str(rev))
    time.sleep(5)
    ado.GDisplay('ADO Subassembly', 'Housing Leak Test', '', str(rev))
    ado.CDA_(0)
    while test_timer != 0:
        print ('Housing Leak Test', test_timer)
        display.lcd_display_string(str(test_timer), 3)
        ML = ado.Min_CDA()
        if test_timer == 9:
            ado.GDisplay('ADO Subassembly', 'Housing Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            ado.GDisplay('ADO Subassembly', 'Housing Leak Found', '', str(rev))
            log('ADO_PNU_DROP_DATA', 'PNU_DROP', 'Subassembly Leak', '_Housing Leak', 'FAIL')
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
            f.write('CheckV ' + '= ' + str(CheckV))
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
                p.digital_write(7, 1)
                time.sleep(.5)
                p.digital_write(7, 0)
                time.sleep(.5)
                button = ado.BTN()
            ado.CDA_(0)
            ado.PNU_ISO_(0)
            ado.OCO()
            ado.B_Off()
            ado.OCO()
            ado.CDA_(0)
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1
    ado.CDA_(1)
    ado.GDisplay('ADO External', 'Leak Test', 'PASS', str(rev))
    log('ADO_PNU_DROP_DATA', 'PNU_DROP', 'Subassembly Leak', '_Housing Leak', 'PASS')

ado.GDisplay('Bellwether Co. ADO', 'ADO PNU Drop', '', str(rev))

time.sleep (2)
while BC_Check != 1:
    ado.GDisplay('Enter Serial #', 'Barcode', '', str(rev))
    ado.B_Yellow()
    BC = input ("Enter SN Barcode ")
    if BC == str('0000'):
        debug = 1
        timer = int(5)
        ST2 = ST2_BW
        print('Debug Enabled via SSN')
    ado.B_Off()
    if prg == BC:
        ado.GDisplay('Bellwether Co. ADO', 'Invalid Serial #', '', str(rev))
        ado.B_Red()
        time.sleep(5)
        ado.B_Off()
        time.sleep(1)
    else:
        display.lcd_display_string(str(BC), 3)
        time.sleep(1)
        display.lcd_clear()
        BC_Check += 1

ado.GDisplay('Begin Testing', '', '', '')

from ADO_ODO_Drop import ssn
from ADO_ODO_Drop import cnt
from ADO_ODO_Drop import res
from ADO_ODO_Drop import fail
from ADO_ODO_Drop import hall



if BC == ssn:
    print("Yes")
    f = open('/home/pi/Bellwether/ADO_ODO_Drop.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' +"'" + str(BC) + "'")
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
    report.log_h('Blah', 'ADO_PNU_DROP_DATA', device, BC)
ado.GDisplay('Bellwether Co. ADO', 'Press Button', 'To Start', str(rev))
if debug == 1:
    button = 1
while button == 0:
    ado.B_Yellow()
    time.sleep(.5)
    ado.B_Off()
    time.sleep(.5)
    button = ado.BTN()
ado.B_Off()
button = 0


#CDA check
# min_psi = ado.Min_CDA() # Removed for small volume compressor
if min_psi == 0:
    cnt += 1
    fail += 1
    res += 1
    print("Bellow 100 PSI")
    report.log('Blah', 'ADO_PNU_DROP_DATA', device, 'N/A', '_Main Pressure Low', 'FAIL', tag, ado_,
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
    ado.B_Off()
    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])


# Hall Adjust
if debug == 1:
    print('No Hall Debug')
else:
    if Drop_Type == 3:
        if hall == 0:
            ado.GDisplay('Bellwether Co. ADO', 'ADO Hall ADJ', 'Press Green', 'Button to Start')
            ado.CDA_(1)
            time.sleep(1)
            if debug == 1:
                button = 1
            while button != 1:
                ado.B_Green()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
            ado.B_Off()
            button = 0

            Open()
            ado.GDisplay('Adjust Open Hall', 'Press Green button', 'When', 'Complete')
            time.sleep(1)

            # Open Hall feedback
            if debug == 1:
                button = 1
            while button != 1:
                if ado.OPN_S() == 1:
                    ado.B_Green()
                else:
                    ado.B_Off()
                button = ado.BTN()
            ado.B_Off()
            button = 0

            Close()
            ado.GDisplay('Adjust Close Hall', 'Press Green button', 'When', 'Complete')
            time.sleep(1)
            print("Hall Open PASS")
            hall = 1

            # Close Hall feedback
            if debug == 1:
                button = 1
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
            f = open('/home/pi/Bellwether/ADO_ODO_Drop.py', "w")
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

#min_psi = 1 #Min Psi bypass
while ST2 != 0:
    if min_psi == 0:
        cnt += 1
        fail += 1
        res += 1
        print("Bellow 100 PSI")
        report.log('Blah', 'ADO_PNU_DROP_DATA', device, '_Main Pressure Low', 'N/A', 'FAIL', tag, ado_,
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
        ado.B_Off()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    if dchk == 0:
        if Drop_Type == 2:
            ado.GDisplay('Bellwether Co. ADO', 'Beginning QA', 'Open', str(rev))
            time.sleep(1)


            # Door QA
            if debug == 1:
                print('No Door Q&A Debug')
            else:
                # Open
                Open()
                while ado.BTN() == 0:
                    ado.B_Green()
                    ado.GDisplay('Did drop Door open?', 'If "Yes" press', 'Green Button', str(rev))
                    time.sleep(bt_time)
                    ado.B_Off()
                    if p.digital_read(7) == 1:
                        ado.B_Off()
                    else:
                        ado.B_Red()
                        ado.GDisplay('Did drop door open?', 'If "No" press', 'Red Button', str(rev))
                        time.sleep(bt_time)
                        ado.B_Off()
                        if ado.BTN() != 0:
                            print("Drop Door Not Open")
                            cnt += 1
                            fail += 1
                            res += 1
                            print('cnt', cnt)
                            print('fail', fail)
                            print('res', res)
                            report.log('Blah', 'ADO_PNU_DROP_DATA', device, 'Beginning',
                                       '_Drop door open failure', 'FAIL', tag, ado_, prg, BC, cnt, res, rev, fail)


                            print("Press Reset")
                            ado.GDisplay('Bellwether Co. ADO', 'Press Reset', '', str(rev))
                            while button != 1:
                                ado.B_Red()
                                time.sleep(.5)
                                ado.B_Off()
                                time.sleep(.5)
                                button = ado.BTN()
                            ado.B_Off()
                            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
                    # Close
                ado.GDisplay('Bellwether Co. ADO', 'Beginning QA', 'Close', str(rev))
                Close()
                while ado.BTN() == 0:
                    ado.B_Green()
                    ado.GDisplay('Did drop door close?', 'If "Yes" press', 'Green Button', str(rev))
                    time.sleep(bt_time)
                    ado.B_Off()
                    if ado.BTN() == 1:
                        ado.B_Off()
                        dchk = 1
                    else:
                        ado.B_Red()
                        ado.GDisplay('Did drop door close?', 'If "No" press', 'Red Button', str(rev))
                        time.sleep(bt_time)
                        ado.B_Off()
                        if ado.BTN() == 1:
                            print("Drop Door Not Close")
                            cnt += 1
                            fail += 1
                            res += 1
                            print('cnt', cnt)
                            print('fail', fail)
                            print('res', res)
                            report.log('Blah', 'ADO_PNU_DROP_DATA', device, 'Beginning',
                                       '_Drop door close failure', 'FAIL', tag, ado_, prg, BC, cnt, res, rev, fail)
                            print("Press Reset")
                            ado.GDisplay('Bellwether Co. ADO', 'Door close Failure', 'Press Reset', str(rev))
                            while button != 1:
                                ado.B_Red()
                                time.sleep(.5)
                                ado.B_Off()
                                time.sleep(.5)
                                button = ado.BTN()
                            ado.B_Off()
                            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    # Open
    ado.GDisplay('Bellwether Co. ADO', 'ADO Drop Count', str(cnt), str(rev))
    Open()
    if Drop_Type == 3:
        if cls != 0:
            print('CLS sensor state not  changed')
            state = ('_CLS Sensor State')
            report.log('Blah', 'ADO_PNU_DROP_DATA', device, 'N/A',
                       '_CLS Sensor State', 'FAIL', tag, ado_, prg, BC, cnt, res, rev, fail)
            ado.GDisplay('Bellwether Co. ADO', 'CLS State', 'Press Reset', str(rev))
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
        if opn != 1:
            cnt += 1
            fail += 1
            res += 1
            print("Fail Open")
            report.log('Blah', 'ADO_PNU_DROP_DATA', device, 'N/A',
                       '_Open Failure', 'FAIL', tag, ado_, prg, BC, cnt, res, rev, fail)
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
            ado.B_Off()
            ado.CLS()
            time.sleep(1)
            ado.OCO()

            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    #Close
    min_psi = ado.Min_CDA()
    if min_psi == 0:
        cnt += 1
        fail += 1
        res += 1
        print("Bellow 100 PSI")
        report.log('Blah', 'ADO_PNU_DROP_DATA', device, 'N/A',
                   '_Main Pressure Low', 'FAIL', tag, ado_, prg, BC, cnt, res, rev, fail)
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
        ado.B_Off()
        ado.CLS()
        time.sleep(1)
        ado.OCO()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    #Close
    ado.OCO()
    Close()
    if Drop_Type == 3:
        if opn != 0:
            print('OPN sensor state not  changed')
            report.log('Blah', 'ADO_PNU_DROP_DATA', device, 'N/A',
                       'OPN Sensor State', 'FAIL', tag, ado_, prg, BC, cnt, res, rev, fail)
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
            report.log('Blah', 'ADO_PNU_DROP_DATA', device, 'N/A',
                       '_Close Failure', 'FAIL', tag, ado_, prg, BC, cnt, res, rev, fail)
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
            ado.B_Off()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    report.log('Blah', 'ADO_PNU_DROP_DATA', device, 'N/A',
               'PASS', 'PASS', tag, ado_, prg, BC, cnt, res, rev, fail)

    time.sleep(5)
    cnt += 1
    ST2 -= 1


    print(cnt)
    ado.GDisplay('Bellwether Co. ADO', 'ADO Drop Count', str(cnt), str(rev))

if Drop_Type == 2:
    ado.GDisplay('Bellwether Co. ADO', 'Beginning QA', 'Open', str(rev))
    time.sleep(1)


    # Door QA
    if debug == 1:
        print('No Door Q&A Debug')
    else:
        # Open
        Open()
        while ado.BTN() == 0:
            ado.B_Green()
            ado.GDisplay('Did drop Door open?', 'If "Yes" press', 'Green Button', str(rev))
            time.sleep(bt_time)
            ado.B_Off()
            if ado.BTN() == 1:
                ado.B_Off()
            else:
                ado.B_Red()
                ado.GDisplay('Did drop door open?', 'If "No" press', 'Red Button', str(rev))
                time.sleep(bt_time)
                ado.B_Off()
                if ado.BTN() != 0:
                    print("Drop Door Not Open")
                    cnt += 1
                    fail += 1
                    res += 1
                    print('cnt', cnt)
                    print('fail', fail)
                    print('res', res)
                    report.log('Blah', 'ADO_PNU_DROP_DATA', device, 'END',
                               '_Drop door open failure', 'FAIL', tag, ado_, prg, BC, cnt, res, rev, fail)
                    print("Press Reset")
                    ado.GDisplay('Bellwether Co. ADO', 'Press Reset', '', str(rev))
                    while button != 1:
                        ado.B_Red()
                        time.sleep(.5)
                        ado.B_Off()
                        time.sleep(.5)
                        button = ado.BTN()
                    ado.B_Off()
                    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
            # Close
        ado.GDisplay('Bellwether Co. ADO', 'Beginning QA', 'Close', str(rev))
        Close()
        while ado.BTN() == 0:
            ado.B_Green()
            ado.GDisplay('Did drop door close?', 'If "Yes" press', 'Green Button', str(rev))
            time.sleep(bt_time)
            ado.B_Off()
            if ado.BTN() == 1:
                ado.B_Green()
                dchk = 1
            else:
                ado.B_Red()
                ado.GDisplay('Did drop door close?', 'If "No" press', 'Red Button', str(rev))
                time.sleep(bt_time)
                ado.B_Off()
                if ado.BTN() == 1:
                    print("Drop Door Not Close")
                    cnt += 1
                    fail += 1
                    res += 1
                    print('cnt', cnt)
                    print('fail', fail)
                    print('res', res)
                    report.log('Blah', 'ADO_PNU_DROP_DATA', device, 'END',
                               '_Drop door close failure', 'FAIL', tag, ado_, prg, BC, cnt, res, rev, fail)
                    print("Press Reset")
                    ado.GDisplay('Bellwether Co. ADO', 'Door close Failure', 'Press Reset', str(rev))
                    while button != 1:
                        ado.B_Red()
                        time.sleep(.5)
                        ado.B_Off()
                        time.sleep(.5)
                        button = ado.BTN()
                    ado.B_Off()
                    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])




# Leak Testing

Leak_Test()
Leak_Housing()
report.log('Blah', 'ADO_PNU_DROP_DATA', device, 'N/A',
                               'PASS', 'PASS', tag, ado_, prg, BC, cnt, res, rev, fail)
report.mlog('Blah','ADO_MASTER_LIST_DATA', device, 'N/A', 'PASS', 'PASS', tag, ado_, prg, BC, cnt, res, rev)
if ST2 == 0:
    f = open('/home/pi/Bellwether/ADO_ODO_Drop.py', "w")
    f.write('cnt = 0')
    f.write('\n')
    f.write('ssn = ""')
    f.write('\n')
    f.write('res = 0')
    f.write('\n')
    f.write('fail = 0')
    f.write('\n')
    if hall == 1:
        f.write('hall ' + '= ' + str(1))
        f.close()
    else:
        f.write('hall ' + '= ' + str(0))
    f.close()

ado.OCO()
ado.CLS()
time.sleep(1)
ado.OCO()
ado.PNU_ISO_(1)
ado.B_Off()
ado.GDisplay('Bellwether', '"Pass" Test Complete', str(cnt), str(rev))
ado.PNU_ISO_(0)
time.sleep(1)
ado.B_Off()
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
display.lcd_clear()
time.sleep(1)
os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])