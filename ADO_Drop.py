#!/usr/bin/env python
import ADO_V
import time
import datetime
import csv
import lcddriver
import lcddriver2
import pifacedigitalio as p
import os
import sys
from ADO_Unit import ado_
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
from ADO_PN import BC_Drop
from ADO_ODO_Drop import ssn
from ADO_ODO_Drop import res
from ADO_ODO_Drop import cnt
from ADO_ODO_Drop import fail
from ADO_Rev import debug
from ADO_Rev import db
from ADO_D_OLED import D_OLED
from ADO_E_IO import E_IO

from ADO_EIOi import GPAi0 
GPAi0.value = False #Logic Iso on



#For DropBox
import dropbox
from dropbox.files import WriteMode
access_token = '6c3d849c913a11'


if debug == 1:
    D_OLED = 0
    ST2 = ST2_BW
    print('Debug via Rev.')
dchk = int(0)

p.init()

latch = int(0)
button = int(0)
display = lcddriver.lcd()
if D_OLED == 1:
    display2 = lcddriver2.lcd2()

button = int(0)
oc_time = int(6)
bt_time = int(1.5)

BC = str('')
BC_Check = int(0)

buf = datetime.datetime.now()
stime = time.time()
device = str('Drop')
state = str('')
note = str('')

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
GDisplay('Bellwether Co. ADO', 'ADO Drop','', str(rev))



while BC_Check != 1:
    GDisplay('Enter Serial #', 'Barcode','',  str(rev))
    p.digital_write(6, 1)
    p.digital_write(7, 1)
    BC = input ("Enter SN Barcode ")
    if BC == str('0000'):
        debug = 1
        timer = int(5)
        ST2 = ST2_BW
        print('Debug Enabled via SSN')
    p.digital_write(6, 0)
    p.digital_write(7, 0)
    print(BC_Drop, BC)
    if prg == BC:
        print('Invalid Serial #')
        GDisplay('Bellwether Co. ADO', 'Invalid Serial #', '', str(rev))
        p.digital_write(7, 1)
        time.sleep(4)
        p.digital_write(7, 0)
        time.sleep(1)
    else:
        GDisplay('Bellwether Co. ADO', '', str(BC), str(rev))
        time.sleep(1)
        GDisplay('Begin Testing', '', '', '')
        BC_Check += 1


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
    f.write('hall ' + '= ' + str(0))
    f.close()
else:
    print("No")
    cnt = 0
    res = 0
    fail = 0
    with open('/home/pi/Bellwether/ADO_DROP_DATA/_Drop_Test_' + BC + '.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Time', 'ADO', 'ADO_Rev', 'PN', 'SSN', 'Cycle Count', 'Resets', 'Note',
                              'State', 'PASS / FAIL'])
        Test_file.flush()
    f = open('/home/pi/Bellwether/ADO_ODO_Drop.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' + "'" + str(BC) + "'")
    f.write('\n')
    f.write('res ' + '= ' + str(res))
    f.write('\n')
    f.write('fail ' + '= ' + str(fail))
    f.write('\n')
    f.write('hall ' + '= ' + str(0))
    f.close()

GDisplay('Bellwether Co. ADO', 'Drop', '', str(rev))
time.sleep(2)
GDisplay('Bellwether Co. ADO', 'Press Green Button', 'To Start', str(rev))

if debug == 1:
    button = int(1)

while button != 1:
    p.digital_write(6, 1)
    time.sleep(.5)
    p.digital_write(6, 0)
    time.sleep(.5)
    button = p.digital_read(7)
p.digital_write(6, 1)
button = 0

GDisplay('Bellwether Co. ADO', 'Beginning QA', 'Open', str(rev))
time.sleep(1)



#Door QA
if debug == 1:
    print('No Door Q&A Debug')
else:
    #Open
    p.digital_write(1, 1)
    time.sleep(.2)
    p.digital_write(0, 0)
    time.sleep(oc_time)
    p.digital_write(1, 0) #todo EMI Test
    while p.digital_read(7) == 0:
            p.digital_write(6, 1)
            GDisplay('Did drop Door open?', 'If "Yes" press', 'Green Button', str(rev))
            time.sleep(bt_time)
            p.digital_write(6, 0)
            if p.digital_read(7) == 1:
                p.digital_write(6, 0)
                dchk == 1
            else:
                p.digital_write(7, 1)
                GDisplay('Did drop door open?', 'If "No" press', 'Red Button', str(rev))
                time.sleep(bt_time)
                p.digital_write(7, 0)
                if p.digital_read(7) != 0:
                    print("Drop Door Not Open")
                    cnt += 1
                    fail += 1
                    res += 1
                    print('cnt', cnt)
                    print('fail', fail)
                    print('res', res)

                    log('ADO_DROP_DATA', 'Drop', 'N/A', '_Drop door open failure', 'FAIL')
                    ulog('N/A', '_Drop door open failure', 'FAIL')

                    print("Press Reset")
                    GDisplay('Bellwether Co. ADO', 'Press Reset', '', str(rev))
                    while button != 1:
                        p.digital_write(7, 1)
                        time.sleep(.5)
                        p.digital_write(7, 0)
                        time.sleep(.5)
                        button = p.digital_read(7)
                    p.digital_write(7, 0)
                    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    #Close
    GDisplay('Bellwether Co. ADO', 'Beginning QA', 'Close', str(rev))
    p.digital_write(1, 0)
    time.sleep(.2)
    p.digital_write(0, 1)
    time.sleep(oc_time)
    p.digital_write(0,0) #todo EMI Test
    while p.digital_read(7) == 0:
            p.digital_write(6, 1)
            GDisplay('Did drop door close?', 'If "Yes" press', 'Green Button', str(rev))
            time.sleep(bt_time)
            p.digital_write(6, 0)
            if p.digital_read(7) == 1:
                p.digital_write(6, 0)
                dchk == 1
            else:
                p.digital_write(7, 1)
                GDisplay('Did drop door close?', 'If "No" press', 'Red Button', str(rev))
                time.sleep(bt_time)
                p.digital_write(7, 0)
                if p.digital_read(7) == 1:
                    print("Drop Door Not Close")
                    cnt += 1
                    fail += 1
                    res += 1
                    print('cnt', cnt)
                    print('fail', fail)
                    print('res', res)


                    log('ADO_DROP_DATA', 'Drop', 'N/A', '_Drop door close failure', 'FAIL')
                    ulog('N/A', '_Drop Door close failure', 'FAIL')

                    print("Press Reset")
                    GDisplay('Bellwether Co. ADO', 'Door close Failure', 'Press Reset', str(rev))
                    while button != 1:
                        p.digital_write(7, 1)
                        time.sleep(.5)
                        p.digital_write(7, 0)
                        time.sleep(.5)
                        button = p.digital_read(7)
                    # GPIO.output(32, 1)
                    # GPIO.cleanup()
                    p.digital_write(7, 0)
                    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])




while ST2 != 0:
    # Open
    p.digital_write(0, 0)
    time.sleep(.2)
    p.digital_write(1, 1)
    GDisplay('Bellwether Co. ADO', 'Drop Door Open', str(cnt), str(rev))
    time.sleep(oc_time)
    p.digital_write(1, 0)

    # Close
    time.sleep(.2)
    p.digital_write(0, 1)
    time.sleep(.2)
    p.digital_write(1, 0)
    GDisplay('Bellwether Co. ADO', 'Drop Door Close', str(cnt), str(rev))
    time.sleep(oc_time) #todo change to "4" after Debug
    p.digital_write(0, 0)  # todo EMI Test
    cnt += 1
    ST2 -= 1
    print("Stop")
    print(ST2)



# Door QA End
if debug == 1:
    print('No Door Q&A Debug')
else:
    # Open
    p.digital_write(1, 1)
    time.sleep(.2)
    p.digital_write(0, 0)
    time.sleep(oc_time)
    while p.digital_read(7) == 0:
        p.digital_write(6, 1)
        GDisplay('Did drop door open?', 'If "Yes" press', 'Green Button', str(rev))
        time.sleep(bt_time)
        p.digital_write(6, 0)
        if p.digital_read(7) == 1:
            p.digital_write(6, 0)
            dchk == 1
        else:
            p.digital_write(7, 1)
            GDisplay('Did drop door open?', 'If "No" press', 'Red Button', str(rev))
            time.sleep(bt_time)
            p.digital_write(7, 0)
            if p.digital_read(7) == 1:
                print("Drop Door Not Open")
                cnt += 1
                fail += 1
                res += 1
                print('cnt', cnt)
                print('fail', fail)
                print('res', res)

                log('ADO_DROP_DATA', 'Drop', 'N/A', '_Drop door open failure END', 'FAIL')
                ulog('N/A', '_Drop door open failure END', 'FAIL')

                print("Press Reset")
                GDisplay('Bellwether Co. ADO', 'Door Open Failure', 'Press Reset', str(rev))

                while button != 1:
                    p.digital_write(7, 1)
                    time.sleep(.5)
                    p.digital_write(7, 0)
                    time.sleep(.5)
                    button = p.digital_read(7)
                # GPIO.output(32, 1)
                # GPIO.cleanup()
                p.digital_write(7, 0)
                os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    # Close
    GDisplay('Bellwether Co. ADO', 'Beginning QA', 'Close', str(rev))
    p.digital_write(1, 0)
    time.sleep(.2)
    p.digital_write(0, 1)
    time.sleep(oc_time)
    p.digital_write(0, 0)  #todo test EMI
    while p.digital_read(7) == 0:
        p.digital_write(6, 1)
        GDisplay('Did drop door close?', 'If "Yes" press', 'Green Button', str(rev))
        time.sleep(bt_time)
        p.digital_write(6, 0)
        if p.digital_read(7) == 1:
            p.digital_write(6, 0)
            dchk == 1
        else:
            p.digital_write(7, 1)
            GDisplay('Did drop door close?', 'If "No" press', 'Red Button', str(rev))
            time.sleep(bt_time)
            p.digital_write(7, 0)
            if p.digital_read(7) == 1:
                print("Drop Door Not Close")
                cnt += 1
                fail += 1
                res += 1
                print('cnt', cnt)
                print('fail', fail)
                print('res', res)

                log('ADO_DROP_DATA', 'Drop', 'N/A', '_Drop door close failure END', 'FAIL')
                ulog('N/A', '_Door Close Failure', 'FAIL')
                print("Press Reset")
                GDisplay('Bellwether Co. ADO', 'Door Close Failure', 'Press Reset', str(rev))

                while button != 1:
                    p.digital_write(7, 1)
                    time.sleep(.5)
                    p.digital_write(7, 0)
                    time.sleep(.5)
                    button = p.digital_read(7)

                # GPIO.output(32, 1)
                # GPIO.cleanup()
                p.digital_write(7, 0)

                os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])


p.digital_write(0, 0)
p.digital_write(1, 0)
GDisplay('Bellwether Co. ADO', 'Test Complete', str(cnt), str(rev))

log('ADO_DROP_DATA', 'Drop', 'N/A', 'PASS', 'PASS')
ulog('N/A', 'PASS', 'PASS')
mlog('ADO_MASTER_LIST_DATA', 'Drop', 'N/A', 'PASS', 'PASS')


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
    f.write('hall ' + '= ' + str(0))
    f.close()
p.digital_write(2, 0)
p.digital_write(3, 0)

if debug == 1:
    button = int(1)

while button == 0:
    p.digital_write(6, 1)
    time.sleep(.5)
    p.digital_write(6,0)
    time.sleep(.5)
    button = p.digital_read(7)
p.digital_write(6, 0)
button = 0
display.lcd_clear()

time.sleep(1)
# GPIO.output(32,1)
os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
# GPIO.cleanup()