#!/usr/bin/env python
import ADO_V
import time
import datetime
import csv
import lcddriver
import lcddriver2
import os
import RPi.GPIO as GPIO
import pifacedigitalio as p
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


p.init()
ado.CDA()
ado.PNU_ISO()
latch = int(0)
button = int(0)
display = lcddriver.lcd()
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
def log(path, sub, note, state, result):
    buf = datetime.datetime.now()
    rev2 = rev[7:]
    with open('/home/pi/Bellwether/' + path + '/' + '_' + sub + '_Test_' + BC + '.csv', mode='a') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([buf, ado_, rev2, prg, BC, cnt, res, note, state, result])
        Test_file.flush()
        f = open('/home/pi/Bellwether/ADO_ODO_' + sub +'.py', "w")
        f.write('cnt ' + '= ' + str(cnt))
        f.write('\n')
        f.write('ssn ' + '= ' + "'" + str(BC) + "'")
        f.write('\n')
        f.write('res ' + '= ' + str(res))
        f.write('\n')
        f.write('fail ' + '= ' + str(fail))
        f.write('\n')
        f.write('fail ' + '= ' + str(fail))
        f.write('\n')
        f.write('hall ' + '= ' + str(1))
        f.close()
def ulog(note, state, result):
    rev2 = rev [8:]
    global etime
    import time
    end = time.time()
    hours, rem = divmod(end - stime, 3600)
    minutes, seconds = divmod(rem, 60)
    etime = ("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
    with open('/home/pi/Bellwether/' + str(ado_) + '_' + 'Useage_Log.csv', mode='a') as Test_file: # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([buf, ado_, device, BC, cnt, res, note, state, result, rev2, etime])

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
def mlog (path, sub, note,state, result):
    with open('/home/pi/Bellwether/' + path + '/' + sub + '_Master_List.csv', mode='a') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([buf, ado_, rev2, prg, BC, cnt, res, note, state, result])
        Test_file.flush()
def GDisplay(Line1,Line2,Line3,Line4):
    if D_OLED == 1:
        display.lcd_clear()
        display.lcd_display_string('See EIO Display', 1)
        display2.lcd2_clear()
        display2.lcd2_clear()
        display2.lcd2_display_string(Line1, 1)
        display2.lcd2_display_string(Line2, 2)
        display2.lcd2_display_string(Line3, 3)
        display2.lcd2_display_string(Line4, 4)
    else:
        display.lcd_clear()
        display.lcd_clear()
        display.lcd_display_string(Line1, 1)
        display.lcd_display_string(Line2, 2)
        display.lcd_display_string(Line3, 3)
        display.lcd_display_string(Line4, 4)
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

GDisplay('Bellwether Co. ADO', '', 'ADO Load', str(rev))

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
    GDisplay('Bellwether Co. ADO', 'Leak Testing', '', str(rev))
    print('Leak Test ', timer)
    time.sleep(1)
    while timer != 0:
        display.lcd_display_string(str(timer), 3)
        time.sleep(1)
        timer -= 1
        print('Leak Test ', timer)
        if timer == 9:
            GDisplay('Bellwether Co. ADO', 'Leak Testing', '', str(rev))
            log('ADO_LOAD_DATA', 'Load', 'N/A', '_Piston Ring', 'PASS')
    GDisplay('Bellwether Co. ADO', 'Leak Testing', 'Complete', str(rev))
    ado.PNU_ISO()

    leak_psi = GPIO.input(6)
    if leak_psi == 0:
        cnt += 1
        fail += 1
        res += 1
        p.digital_write(2, 0)
        p.digital_write(3, 1)
        time.sleep(1)
        p.digital_write(3, 0)
        print("Cylinder Leak")
        state = ('_Cylinder Leak')
        log('ADO_LOAD_DATA', 'Load', 'N/A', '_Piston Ring', 'FAIL')
        ulog('N/A', '_Cylinder Leak', 'FAIL')
        GDisplay('Bellwether Co. ADO', 'Pressure Leak!', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            p.digital_write(7, 1)
            time.sleep(.5)
            p.digital_write(7, 0)
            time.sleep(.5)
            button = p.digital_read(7)
        GPIO.cleanup()
        p.digital_write(7, 0)
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
def Leak_Housing():
    global timer
    global cnt
    global fail
    global res
    global button
    print ('Leak Housing')
    test_timer = int(30)
    ado.OCOn()
    GDisplay('ADO Pressurizing', 'Subassembly', 'Please Wait', str(rev))
    time.sleep(5)
    GDisplay('ADO Subassembly', 'Housing Leak Test', '', str(rev))
    ado.CDA()
    while test_timer != 0:
        print ('Housing Leak Test', test_timer)
        display.lcd_display_string(str(test_timer), 3)
        ML = GPIO.input(5)
        if test_timer == 9:
            GDisplay('ADO Subassembly', 'Housing Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            GDisplay('ADO Subassembly', 'Housing Leak Found', '', str(rev))
            log('ADO_LOAD_DATA', 'Load', 'Subassembly Leak', '_Housing Leak', 'FAIL')
            ulog('EX CLS Leak', 'FAIL', 'FAIL')
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
            ado.CDA()
            ado.PNU_ISO()
            ado.OCO()
            # GPAi1.value = True  # Close
            # GPAi2.value = True  # Close
            # p.digital_write(2, 0)
            # p.digital_write(3, 0)
            while button != 1:
                ado.B_Red()
                # p.digital_write(7, 1)
                time.sleep(.5)
                ado.B_Off()
                p.digital_write(7, 0)
                time.sleep(.5)
                button = ado.BTN()
            # GPAi1.value = True  # Close
            # GPAi2.value = True  # Close
            # p.digital_write(2, 0)
            # p.digital_write(3, 0)
            GPIO.cleanup()
            ado.B_Off()
            ado.OCO()
            # p.digital_write(2, 0)
            # GPAp1.value = True
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1

    GDisplay('ADO External', 'Leak Test', 'PASS', str(rev))
    log('ADO_LOAD_DATA', 'Load', 'Subassembly Leak', '_Housing Leak', 'PASS')
    ulog('Load Housing Leak', 'PASS ', 'PASS')
time.sleep(2)

while BC_Check != 1:
    GDisplay('Enter Serial #', 'Barcode', '', str(rev))
    p.digital_write(6, 1)
    p.digital_write(7, 1)
    BC = input("Enter SN Barcode ") #todo Enable after debug
    # BC = ('2222') #todo Remove after debug
    # BC = ('0000') #todo Remove after debug
    if BC == str('0000'):
        BC == str('debug')
        debug = 1
        timer = int(60) # debug leak timer
        ST1 = ST1_BW
        print('Debug Enabled via SSN')
    p.digital_write(6, 0)
    p.digital_write(7, 0)
    if prg == BC:
        GDisplay('Bellwether Co. ADO', 'Invalid Serial #', '', str(rev))
        p.digital_write(7, 1)
        time.sleep(5)
        p.digital_write(7, 0)
        time.sleep(1)
    else:
        GDisplay('', '', str(BC), '')
        time.sleep(1)
        GDisplay('Begin Testing', '', '', '')
        BC_Check += 1

GDisplay('Begin Testing', '', '', '')

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

    # CSV Header
    with open('/home/pi/Bellwether/ADO_LOAD_DATA/_Load_Test_' + BC + '.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Time', 'ADO', 'ADO_Rev', 'PN', 'SSN', 'Cycle Count', 'Resets', 'Note',
                              'State', 'PASS / FAIL'])
        Test_file.flush()
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


GDisplay('Bellwether Co. ADO', 'Press Button', 'To Start', str(rev))

if debug == 1:
    button = 1
while button == 0:
    p.digital_write(6, 1)
    time.sleep(.5)
    p.digital_write(6, 0)
    time.sleep(.5)
    button = p.digital_read(7)
p.digital_write(6, 0)
button = 0

if debug == 1:
    print('No Hall Debug')
else:
    if hall == 0:
        GDisplay('Bellwether Co. ADO', 'ADO Hall ADJ', 'Press Green', 'Button to Start')
        time.sleep(1)
        while button != 1:
            p.digital_write(6, 1)
            time.sleep(.5)
            p.digital_write(6, 0)
            time.sleep(.5)
            button = p.digital_read(7)
        p.digital_write(6, 0)
        button = 0
        Close()
        GDisplay('Adjust Close Hall', 'Press Green Button', 'When', 'Complete')
        time.sleep(1)


        # Close Hall feedback
        while button != 1:
            if p.digital_read(3) == 1:
                p.digital_write(6, 1)
            else:
                p.digital_write(6, 0)
            button = p.digital_read(7)
        p.digital_write(6, 0)
        button = 0
        print("Hall Close PASS")
        GDisplay('Hall Adjustment', '', 'Complete', '')
        hall = 1

if debug == 1:
    print('No Hopper Test Debug')
else:
    if hopper == 0:
        ado.B_Yellow()
        GDisplay('Bellwether Co. ADO', 'Insert Hopper', '', str(rev))
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
    GDisplay('Bellwether Co. ADO', 'ADO Load', 'Shoe Door', 'Test')
    time.sleep(1)


    # Shoe Door Q&A
    ado.Mag()
    while p.digital_read(7) == 0:
        p.digital_write(6, 1)
        GDisplay('Did shoe door open?', 'If "Yes" press', 'Green Button', str(rev))
        time.sleep(bt_time)
        p.digital_write(6, 0)
        if p.digital_read(7) == 1:
            p.digital_write(6, 0)
        else:
            p.digital_write(7, 1)
            GDisplay('Did shoe door open?', 'If "No" press', 'Red Button', str(rev))
            time.sleep(bt_time)
            p.digital_write(7, 0)
            if p.digital_read(7) == 1:
                print("Shoe Door Not Close")
                cnt += 1
                fail += 1
                res += 1
                print('cnt', cnt)
                print('fail', fail)
                print('res', res)
                log('ADO_LOAD_DATA', 'Load', 'N/A', '_Shoe Door open FAILURE', 'FAIL')
                ulog('N/A', '_Shoe Door open FAILURE', 'FAIL')
                print("Press Reset")
                GDisplay('Bellwether Co. ADO', 'Shoe Door Open Failure', 'Press Reset', str(rev))
                while button != 1:
                    p.digital_write(7, 1)
                    time.sleep(.5)
                    p.digital_write(7, 0)
                    time.sleep(.5)
                    button = p.digital_read(7)
                GPIO.cleanup()
                p.digital_write(7, 0)
                os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])


#Open
while ST1 != 0:
    min_psi = ado.Min_CDA()
    if min_psi == 0:
        cnt += 1
        fail += 1
        res += 1
        print("Bellow 100 PSI")
        log('ADO_LOAD_DATA', 'Load', 'N/A', '_Main Pressure Low', 'FAIL')
        ulog('N/A', '_Main Pressure Low', 'FAIL')
        print("Press Reset")
        GDisplay('Bellwether Co. ADO', 'Bellow 100 PSI', 'Press Reset', str(rev))
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
        # p.digital_write(3, 1)
        ado.CLS()
        time.sleep(1)
        ado.OCO()
        # p.digital_write(3, 0)
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    GDisplay('Bellwether Co. ADO', 'ADO Load Count', str(cnt), str(rev))
    Open()
    if cls != 0:
        print('CLS sensor state not  changed')
        log('ADO_LOAD_DATA', 'Load', 'N/A', '_CLS Sensor State', 'FAIL')
        ulog('N/A', '_CLS Sensor State', 'FAIL')
        GDisplay('Bellwether Co. ADO', 'CLS State', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            p.digital_write(7, 1)
            time.sleep(.5)
            p.digital_write(7, 0)
            time.sleep(.5)
            button = p.digital_read(7)
        GPIO.cleanup()
        p.digital_write(7, 0)
        p.digital_write(2, 0)
        p.digital_write(3, 1)
        time.sleep(1)
        p.digital_write(3, 0)

        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    if opn != 1:
        cnt += 1
        fail += 1
        res += 1
        print("Fail Open")
        log('ADO_LOAD_DATA', 'Load', 'N/A', '_Open Failure', 'FAIL')
        ulog('N/A', '_Open Failure', 'FAIL')
        GDisplay('Bellwether Co. ADO', 'Open Fail!', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            p.digital_write(7, 1)
            time.sleep(.5)
            p.digital_write(7, 0)
            time.sleep(.5)
            button = p.digital_read(7)
        GPIO.cleanup()
        p.digital_write(7, 0)
        p.digital_write(2, 0)
        p.digital_write(3, 1)
        time.sleep(1)
        p.digital_write(3, 0)
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])


    # Close
    min_psi = GPIO.input(5)
    if min_psi == 0:
        cnt += 1
        fail += 1
        res += 1
        print("Bellow 100 PSI")
        log('ADO_LOAD_DATA', 'Load', 'N/A', '_Main Pressure Low', 'FAIL')
        ulog('N/A', '_Main Pressure Low', 'FAIL')
        print("Press Reset")
        GDisplay('Bellwether Co. ADO', 'Bellow 100 PSI', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            p.digital_write(7, 1)
            time.sleep(.5)
            p.digital_write(7, 0)
            time.sleep(.5)
            button = p.digital_read(7)
        GPIO.cleanup()
        p.digital_write(7, 0)
        p.digital_write(2, 0)
        p.digital_write(3, 1)
        time.sleep(1)
        p.digital_write(3, 0)
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    # Close
    p.digital_write(7, 0)
    p.digital_write(6, 0)
    Close()
    if opn != 0:
        print('OPN sensor state not  changed')
        log('ADO_LOAD_DATA', 'Load', 'N/A', '_OPN Sensor State', 'FAIL')
        ulog('N/A', '_OPN Sensor State', 'FAIL')
        GDisplay('Bellwether Co. ADO', 'OPN State', 'Press Reset', str(rev))
        if debug == 1:
            button = 1
        while button != 1:
            p.digital_write(7, 1)
            time.sleep(.5)
            p.digital_write(7, 0)
            time.sleep(.5)
            button = p.digital_read(7)
        GPIO.cleanup()
        p.digital_write(7, 0)
        p.digital_write(2, 0)
        p.digital_write(3, 1)
        time.sleep(1)
        p.digital_write(3, 0)
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    if cls != 1:
        cnt += 1
        fail += 1
        res += 1
        print("Fail Close")
        log('ADO_LOAD_DATA', 'Load', 'N/A', '_Close Failure', 'FAIL')
        ulog('N/A', '_Close Failure', 'FAIL')
        print("Press Reset")
        GDisplay('Bellwether Co. ADO', 'Close Fail!', 'Press Reset', str(rev))

        if debug == 1:
            button = 1
        while button != 1:
            p.digital_write(7, 1)
            time.sleep(.5)
            p.digital_write(7, 0)
            time.sleep(.5)
            button = p.digital_read(7)
        GPIO.cleanup()
        p.digital_write(6, 0)
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        log('ADO_LOAD_DATA', 'Load', 'N/A', 'PASS', 'PASS')

    time.sleep(1)
    cnt += 1
    ST1 -= 1




print(cnt)
GDisplay('Bellwether Co. ADO', 'ADO Load Count', str(cnt), str(rev))

#Leak Test
Leak_Test() #todo enable after debug
Leak_Housing()



print('Leak Test Complete')
log('ADO_LOAD_DATA', 'Load', 'N/A', 'PASS', 'PASS')
ulog('N/A', 'PASS', 'PASS')
mlog('ADO_MASTER_LIST_DATA', 'Load', 'N/A', 'PASS', 'PASS')




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
# p.digital_write(2, 0)
# p.digital_write(3, 0)
ado.OCO()

time.sleep(1)
ado.PNU_ISO()
# # GPAi2.value = False
# p.digital_write(7, 0)
ado.B_Off()
GDisplay('Bellwether Co. ADO', '"Pass" Test Complete', str(cnt), str(rev))
print('Test Complete')
ado.PNU_ISO()
# GPAi2.value = True
time.sleep(1)
# p.digital_write(7, 0)
# p.digital_write(6, 0)
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
display.lcd_clear()
time.sleep(1)
os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
GPIO.cleanup()
