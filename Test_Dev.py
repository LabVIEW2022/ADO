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
import RPi.GPIO as GPIO
from ADO_WatchDog import WD

ssn = str('')
cnt = int(0)
buf = datetime.datetime.now()
stime = time.time()
ExhaustTest_writer = str("")
spool_time = int(10) #Default 10s

fancnt = int(1) # 2 = 1.3, 1 = 2.0

RPM_1 = int(0)
RPM_2 = int(0)
fan1line = str('')
fan2line = str('')
from ADO_ODO_Exhaust import ssn
from ADO_ODO_Exhaust import cnt
from ADO_ODO_Exhaust import res
from ADO_ODO_Exhaust import fail
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
from ADO_Rev import ST4
from ADO_Rev import ST4_BW
from ADO_Rev import IC4
from ADO_Rev import IC4_2
from ADO_PN import BC_Panel
from ADO_PN import BC_Panel_BW
from ADO_PN_Buf import prg
from ADO_PN_Buf import prg_
from ADO_Rev import debug
from ADO_Rev import db
from ADO_D_OLED import D_OLED
from ADO_E_IO import E_IO

open_ = open('/home/pi/Bellwether/ADO_Tag.py', 'rt')
tag = open_.read()
open_.close()

p.init()

#For DropBox
import dropbox
from dropbox.files import WriteMode
access_token = '6c3d849c913a11'

if debug == 1:
    ST4 = ST4_BW
    D_OLED = 0
    print('Debug via Rev.')

device = str('Exhaust')
state = str('')

latch = int(0)
display = lcddriver.lcd()
if D_OLED == 1:
    display2 = lcddriver2.lcd2()

def log(path, sub, note, state, result):
    buf = datetime.datetime.now()
    rev2 = rev[7:]
    with open('/home/pi/Bellwether/' + path + '/' + '_' + sub + '_Test_' + BC + '.csv', mode='a') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([buf, ado_, rev2, prg, BC, cnt, res, note, state, result, tag])
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
        Test_writer.writerow([buf, ado_, rev2, prg, BC, cnt, res, note, state, result, tag])
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

def cntlog():
    global cnt
    global ssn
    global res
    global fail
    f = open('/home/pi/Bellwether/ADO_ODO_Exhaust.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' +"'" + str(BC) + "'")
    f.write('\n')
    f.write('res ' + '= ' + str(res))
    f.write('\n')
    f.write('fail ' + '= ' + str(fail))
    f.close()

def fantest(pwms):
    global RPM_1
    global RPM_2
    RPM_1 = 0
    RPM_2 = 0
    pwm.start(pwms)
    time.sleep(spool_time)
    try:  # watch dog
        with WD(5):  # watch dog timer
            print('Fan 1 WD')
            while True:
                GPIO.wait_for_edge(26, GPIO.FALLING)
                RPM_1 += 1
    except WD:
        print('End Fan 1')

    if fancnt == 2:
        try:  # watch dog
            with WD(5):  # watch dog timer
                print('Fan 2 WD')
                while True:
                    GPIO.wait_for_edge(19, GPIO.FALLING)
                    RPM_2 += 1
        except WD:
            print('End Fan 2')

    RPM_1 /= 2
    RPM_1 *= 12

    if fancnt == 2:
        RPM_2 /= 2
        RPM_2 *= 12

    print('Fan 1 ', RPM_1)
    if fancnt == 2:
        print('Fan 2 ', RPM_2)


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Sets Physical Pin
GPIO.setup(13,GPIO.OUT) #<PWM
GPIO.setup(26,GPIO.IN, pull_up_down=GPIO.PUD_UP) #<--- Fan 1 Tach
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #<--- PWM Fan 1 Pull up Check todo change to pull down after debug

if fancnt == 2:
    GPIO.setup(19,GPIO.IN, pull_up_down=GPIO.PUD_UP) #<--- Fan 2 Tach
    GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #<--- PWM Fan 2 Pull up Check todo change to pull down after debug
pwm = GPIO.PWM(13, 100)
pwm1 = int(0)
if fancnt == 2:
    pwm2 = int(0)
button = int(0) #todo change to "0"after debug
fan1 = int(0000) #todo change to "0" after debug
if fancnt == 2:
    fan2 = int(0000)#todo change to "0" after debug
pulse = int(0)
ttime = int(2000) #todo Change to "2000" after Debug
note = int(1)
buf = datetime.datetime.now()
BC_Check = int(0)
IC = str('')

GDisplay('Bellwether Co. ADO',
             'Exhaust Test',
             '',
             str(rev))


time.sleep(2)
p.digital_write(6, 1)
p.digital_write(7, 1)
while BC_Check != 1:
    GDisplay('Enter Serial #',
             'Barcode',
             '',
             str(rev))
    p.digital_write(6, 1)
    p.digital_write(7, 1)
    BC = input('Enter SN Barcode') #todo enable after debug
    if BC == str('0000'):
        debug = 1
        timer = int(5)
        ST4 = ST4_BW
        print('Debug Enabled via SSN')
    p.digital_write(6, 0)

    p.digital_write(7, 0)
    if prg_ == BC:
        GDisplay('Bellwether Co. ADO',
                 'Invalid Serial #',
                 '',
                 str(rev))
        p.digital_write(7, 1)
        time.sleep(5)
        p.digital_write(7, 0)
        time.sleep(1)
    else:
        GDisplay('',
                 '',
                 str(BC),
                 '')
        time.sleep(1)
        GDisplay('Begin Testing',
                 '',
                 '',
                 '')
        BC_Check += 1


time.sleep(1)
GDisplay('Begin Testing',
         '',
         '',
         '')


if BC == ssn:
    print("Yes")
    f = open('/home/pi/Bellwether/ADO_ODO_Exhaust.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' +"'" + str(BC) + "'")
    f.write('\n')
    f.write('res ' + '= ' + str(res))
    f.write('\n')
    f.write('fail ' + '= ' + str(fail))
    f.close()

else:
    print("No")
    print(BC)
    cnt = 0
    res = 0
    fail = 0
    with open('/home/pi/Bellwether/ADO_EXHAUST_DATA/_Exhaust_Test_' + BC + '.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Time', 'ADO', 'ADO_Rev', 'PN', 'SSN', 'Cycle Count', 'Resets', 'Note',
                              'State', 'PASS / FAIL'])
        Test_file.flush()

    f = open('/home/pi/Bellwether/ADO_ODO_Exhaust.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' + "'" + str(BC) + "'")
    f.write('\n')
    f.write('res ' + '= ' + str(res))
    f.write('\n')
    f.write('fail ' + '= ' + str(fail))
    f.close()

GDisplay('Bellwether Co. ADO',
         'Press Green Button',
         'To Start',
         str(rev))

if debug == 1:
    button = 1
while button == 0:
    p.digital_write(6, 1)
    time.sleep(.5)
    p.digital_write(6, 0)
    time.sleep(.5)
    button = p.digital_read(7)

#PWM Line Test # todo enable after debug
GDisplay('Bellwether Co. ADO',
         'PWM Line Test',
         '',
         str(rev))

p.digital_write(5, 1)
time.sleep(2)
fan1 = GPIO.input(17)
if fancnt == 2:
    fan2 = GPIO.input(18)
p.digital_write(5, 0)

print('PWM Line Test')
button = 0
if fancnt == 2:
    if fan1 != 1 and fan2 != 1:
        cnt += 1
        fail += 1
        res += 1
        p.digital_write(7, 1)
        p.digital_write(6, 0)
        print("Fan 1 and 2 PWM Line")
        log('ADO_EXHAUST_DATA',
            'Exhaust', 'N/A',
            '_Fan 1 & 2 PWM Fail',
            'FAIL')
        ulog('N/A', '_Fan 1 & 2 PWM Fail', 'FAIL')

        GDisplay('!!!!!!FAILURE!!!!!!!',
                 'Fan 1 & 2 PWM Line',
                 'Press Reset',
                 str(rev))
        p.digital_write(5, 0)
        pwm.stop()
        if debug == 1:
            button = 1
        while button == 0:
            button = p.digital_read(7)
        p.digital_write(7, 0)
        p.digital_write(6, 0)
        pwm.stop()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
if fan1 != 1:
    cnt += 1
    fail += 1
    res += 1
    p.digital_write(7, 1)
    p.digital_write(6, 0)
    print("Fan 1 PWM Line")
    log('ADO_EXHAUST_DATA',
        'Exhaust', 'N/A',
        '_Fan 1 PWM Fail',
        'FAIL')
    ulog('N/A', '_Fan 1 PWM Fail', 'FAIL')
    GDisplay('!!!!!!FAILURE!!!!!!!',
             'Fan 1 PWM Line',
             'Press Reset',
             str(rev))
    p.digital_write(5, 0)
    if debug == 1:
        button = 1
    if button == 1:
        button = 1
    while button == 0:
        button = p.digital_read(7)
    p.digital_write(7, 0)
    p.digital_write(6, 0)
    pwm.stop()
    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

if fancnt == 2:
    if fan2 != 1:
        cnt += 1
        fail += 1
        res += 1
        p.digital_write(7, 1)
        p.digital_write(6, 0)
        print("Fan 2 PWM Line")
        log('ADO_EXHAUST_DATA',
            'Exhaust', 'N/A',
            '_Fan 2 PWM Fail',
            'FAIL')
        ulog('N/A', '_Fan 2 PWM Fail', 'FAIL')

        GDisplay('!!!!!!FAILURE!!!!!!!',
                 'Fan 2 PWM Line',
                 'Press Reset',
                 str(rev))
        p.digital_write(5, 0)
        pwm.stop()
        if button == 1:
            button = 1
        while button == 0:
            button = p.digital_read(7)
        p.digital_write(7, 0)
        p.digital_write(6, 0)
        pwm.stop()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

print('PWM Line Pass')

print("Exhaust PWM")
while IC != IC4_2:
    GDisplay('Replace Cable With',
             '"Exhaust 2"',
             '',
             str(rev))
    p.digital_write(6, 1)
    p.digital_write(7, 1)
    print('Replace Cable')
    print('Scan Exhaust 2')
    time.sleep(10)

    GDisplay('Scan interface cable',
             '"Exhaust 2"',
             'Barcode',
             str(rev))
    IC = input('interface cable 2')
    if IC == str('Test'):
        IC = IC4_2
        print(IC, IC4_2)
    if IC == IC4_2:
        print('Correct Cable')
    else:
        print('Incorrect Cable')
        p.digital_write(6, 0)
        p.digital_write(7, 0)
        GDisplay('Bellwther Co. ADO',
                 'Wrong Cable',
                 'Press Reset',
                 str(rev))
        while button == 0:
            p.digital_write(7, 1)
            time.sleep(.5)
            p.digital_write(7, 0)
            time.sleep(.5)
            button = p.digital_read(7)
        p.digital_write(7, 0)
        button = 0
        display.lcd_clear()


# ##########
#
button = 0 # todo change to "0" after debug

GDisplay('Bellwether Co. ADO',
         'Exhaust Test (Tach)',
         '5%',
         str(rev))

# Tach Test
p.digital_write(5, 1)
pwm.start(95) # <-- 5% PWM
time.sleep(10) #todo Change to "10" after Debug

while ttime != 0:
    pulse = GPIO.input(26)
    if pulse == 0:
        fan1 += 1
    ttime -= 1
    # time.sleep(00.1)
ttime = 2000 #todo Change to "2000" after Debug

if fancnt == 2:
    while ttime != 0:
        pulse = GPIO.input(19)
        if pulse == 0:
            fan2 += 1
        ttime -= 1


if fancnt == 2:
    print("Fan 1", fan1, "Fan 2", fan2)
else:
    print("Fan 1", fan1)




#Both Fan Failuire Tach

if fancnt == 2:
    if fan1 <= 10 and fan2 <= 10:
        cnt += 1
        fail += 1
        res += 1
        p.digital_write(7, 1)
        p.digital_write(6, 0)
        print("Fail Fan 1 and Fan 2")
        log('ADO_EXHAUST_DATA',
            'Exhaust', 'N/A',
            '_Fan 1 and Fan 2 Failure',
            'FAIL')
        ulog('N/A', '_Fan 1 and Fan 2 Failure', 'FAIL')

        GDisplay('!!!!!!FAILURE!!!!!!!',
                 'Fan 1 and Fan 2',
                 'Press Reset',
                 str(rev))
        p.digital_write(5, 0)
        pwm.stop()
        #GPIO.cleanup()
        if debug == 1:
            button = 1
        while button == 0:
            button = p.digital_read(7)
        p.digital_write(7, 0)
        p.digital_write(6, 0)
        pwm.stop()
        #GPIO.cleanup()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    else:
        print("Pass Fan Both")

#Both Fan Power Fail
if fancnt == 2:
    if fan1 == 2000 and fan2 == 2000:
        cnt += 1
        fail += 1
        res += 1
        p.digital_write(7, 1)
        p.digital_write(6, 0)
        print("Fail Fan 1 and Fan 2 Power Fail")
        log('ADO_EXHAUST_DATA',
            'Exhaust', 'N/A',
            '_Fan 1 Fan 2 Power Fail',
            'FAIL')
        ulog('N/A', '_Fan 1 Fan 2 Power Fail', 'FAIL')

        GDisplay('!!!!!!FAILURE!!!!!!!',
                 'Fan 1,2 Power Fail',
                 'Press Rest',
                 str(rev))
        p.digital_write(5, 0)
        pwm.stop()
        #GPIO.cleanup()
        if debug == 1:
            button = 1
        while button == 0:
            button = p.digital_read(7)
        p.digital_write(7, 0)
        p.digital_write(6, 0)
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

#Fan 1 Power Failure
if fan1 == 2000:
    cnt += 1
    fail += 1
    res += 1
    p.digital_write(7, 1)
    p.digital_write(6, 0)
    print("Fail Fan 1 Power Fail")
    log('ADO_EXHAUST_DATA',
        'Exhaust', 'N/A',
        '_Fan 1 Power Fail',
        'FAIL')
    ulog('N/A', '_Fan 1 Power Fail', 'FAIL')

    GDisplay('!!!!!!FAILURE!!!!!!!',
             'Fan 1 PW/Tach Fail',
             'Press Reset',
             str(rev))
    p.digital_write(5, 0)
    pwm.stop()
    if debug == 1:
        button = 1
    while button == 0:
        button = p.digital_read(7)
    p.digital_write(7, 0)
    p.digital_write(6, 0)
    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

#Fan 2 Power Failure
if fancnt == 1:
    if fan2 == 2000:
        cnt += 1
        fail += 1
        res += 1
        p.digital_write(7, 1)
        p.digital_write(6, 0)
        print("Fail Fan 2 Power Fail")
        log('ADO_EXHAUST_DATA',
            'Exhaust', 'N/A',
            '_Fan 2 Power Fail',
            'FAIL')
        ulog('N/A', '_Fan 2 Power Fail', 'FAIL')

        GDisplay('!!!!!!FAILURE!!!!!!!',
                 'Fan 2 PW/Tach Fail',
                 'Press Reset',
                 str(rev))

        p.digital_write(5, 0)
        pwm.stop()
        if debug == 1:
            button = 1
        while button == 0:
            button = p.digital_read(7)
        p.digital_write(7, 0)
        p.digital_write(6, 0)
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])


#Fan 1 Tach
if fan1 <= 10:
    cnt += 1
    fail += 1
    res += 1
    p.digital_write(7, 1)
    p.digital_write(6, 0)
    print("Fail Fan 1")
    log('ADO_EXHAUST_DATA',
        'Exhaust', 'N/A',
        '_Fan 1 Failure',
        'FAIL')
    ulog('N/A', '_Fan 1 Failure', 'FAIL')

    GDisplay('!!!!!!FAILURE!!!!!!!',
             'Fan 1',
             'Press Reset',
             str(rev))
    p.digital_write(5, 0)
    pwm.stop()
    if debug == 1:
        button = 1
    while button == 0:
        button = p.digital_read(7)
    p.digital_write(7, 0)
    p.digital_write(6, 0)

    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
else:
    print("Pass Fan 1")

if fancnt == 2:
    if fan2 <= 10:
        cnt += 1
        fail += 1
        res += 1
        p.digital_write(7, 1)
        p.digital_write(6, 0)
        print("Fail Fan 2")
        log('ADO_EXHAUST_DATA',
            'Exhaust', 'N/A',
            '_Fan 2 Failure',
            'FAIL')
        ulog('N/A', '_Fan 2 Failure', 'FAIL')

        GDisplay('!!!!!!FAILURE!!!!!!!',
                 'Fan 2',
                 'Press Reset',
                 str(rev))
        p.digital_write(5, 0)
        pwm.stop()
        if debug == 1:
            button = 1
        while button == 0:
            button = p.digital_read(7)
        p.digital_write(7, 0)
        p.digital_write(6, 0)
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    else:
        print("Pass Fan 2")


time.sleep(10)

# Here
while ST4 != 0:
    # 15%
    GDisplay('Bellwether Co. ADO',
             'Exhaust Test (PWM)',
             '15%',
             str(rev))
    fantest(85)
    fan1line = ('Fan 1 RPM ' + ' ' + str(RPM_1))
    if fancnt == 1:
        fan2line = ('Fan 2 RPM ' + ' ' + str(RPM_2))
        GDisplay('PWM 15%',
                 str(fan1line),
                 str(fan2line),
                 str(rev))
    else:
        GDisplay('PWM 15%',
                 str(fan1line),
                 '',
                 str(rev))
    if RPM_1 <= 2300:
        time.sleep(5)
        log('ADO_EXHAUST_DATA',
            'Exhaust', '15% PWM',
            '_Fan 1 Too Slow',
            'FAIL')
        ulog('N/A', '_Fan 1', 'FAIL')
        GDisplay('Bellwether Co. ADO',
                 'Fan 1 Too Slow',
                 '@ 15% PWM',
                 str(rev))
        p.digital_write(5, 0)
        pwm.stop()
        if debug == 1:
            button = 1
        while button != 1:
            p.digital_write(7, 1)
            time.sleep(.5)
            p.digital_write(7, 0)
            time.sleep(.5)
            button = p.digital_read(7)
        cnt += 1
        res += 1
        fail += 1
        cntlog()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    if fancnt == 2:
        if RPM_2 <= 2300:
            time.sleep(5)
            log('ADO_EXHAUST_DATA',
                'Exhaust', '15% PWM',
                '_Fan 2 Too Slow',
                'FAIL')
            ulog('N/A', '_Fan 2', 'FAIL')
            GDisplay('Bellwether Co. ADO',
                     'Fan 2 Too Slow',
                     '@ 15% PWM',
                     str(rev))
            p.digital_write(5, 0)
            pwm.stop()
            if debug == 1:
                button = 1
            while button != 1:
                p.digital_write(7, 1)
                time.sleep(.5)
                p.digital_write(7, 0)
                time.sleep(.5)
                button = p.digital_read(7)
            cnt += 1
            res += 1
            fail += 1
            cntlog()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    time.sleep(5)

    # 20%
    GDisplay('Bellwether Co. ADO',
             'Exhaust Test (PWM)',
             '20%',
             str(rev))
    fantest(80)
    if fancnt == 2:
        fan1line = ('Fan 1 RPM ' + ' ' + str(RPM_1))
        fan2line = ('Fan 2 RPM ' + ' ' + str(RPM_2))
        GDisplay('PWM 20%',
                 str(fan1line),
                 str(fan2line),
                 str(rev))
    else:
        fan1line = ('Fan 1 RPM ' + ' ' + str(RPM_1))
        GDisplay('PWM 20%',
                 str(fan1line),
                 '',
                 str(rev))
    if RPM_1 <= 2500:
        time.sleep(5)
        log('ADO_EXHAUST_DATA',
            'Exhaust', '20% PWM',
            '_Fan 1 Too Slow',
            'FAIL')
        ulog('N/A', '_Fan 1', 'FAIL')
        GDisplay('Bellwether Co. ADO',
                 'Fan 1 Too Slow',
                 '@ 20% PWM',
                 str(rev))
        p.digital_write(5, 0)
        pwm.stop()
        if debug == 1:
            button = 1
        while button != 1:
            p.digital_write(7, 1)
            time.sleep(.5)
            p.digital_write(7, 0)
            time.sleep(.5)
            button = p.digital_read(7)
        cnt += 1
        res += 1
        fail += 1
        cntlog()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    if fancnt == 1:
        if RPM_2 <= 2500:
            time.sleep(5)
            log('ADO_EXHAUST_DATA',
                'Exhaust', '20% PWM',
                '_Fan 2 Too Slow',
                'FAIL')
            ulog('N/A', '_Fan 2', 'FAIL')
            GDisplay('Bellwether Co. ADO',
                     'Fan 2 Too Slow',
                     '@ 20% PWM',
                     str(rev))
            p.digital_write(5, 0)
            pwm.stop()
            if debug == 1:
                button = 1
            while button != 1:
                p.digital_write(7, 1)
                time.sleep(.5)
                p.digital_write(7, 0)
                time.sleep(.5)
                button = p.digital_read(7)
            cnt += 1
            res += 1
            fail += 1
            cntlog()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    time.sleep(5)

    # 40%
    GDisplay('Bellwether Co. ADO',
             'Exhaust Test (PWM)',
             '40%',
             str(rev))
    fantest(60)
    if fancnt == 2:
        fan1line = ('Fan 1 RPM ' + ' ' + str(RPM_1))
        fan2line = ('Fan 2 RPM ' + ' ' + str(RPM_2))
        GDisplay('PWM 40%',
                 str(fan1line),
                 str(fan2line),
                 str(rev))
    else:
        fan1line = ('Fan 1 RPM ' + ' ' + str(RPM_1))
        GDisplay('PWM 40%',
                 str(fan1line),
                 '',
                 str(rev))
    if RPM_1 <= 4800:
        time.sleep(5)
        log('ADO_EXHAUST_DATA',
            'Exhaust', '40% PWM',
            '_Fan 1 Too Slow',
            'FAIL')
        ulog('N/A', '_Fan 1', 'FAIL')
        GDisplay('Bellwether Co. ADO',
                 'Fan 1 Too Slow',
                 '@ 40% PWM',
                 str(rev))
        p.digital_write(5, 0)
        pwm.stop()
        if debug == 1:
            button = 1
        while button != 1:
            p.digital_write(7, 1)
            time.sleep(.5)
            p.digital_write(7, 0)
            time.sleep(.5)
            button = p.digital_read(7)
        cnt += 1
        res += 1
        fail += 1
        cntlog()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    if fancnt == 2:
        if RPM_2 <= 4800:
            time.sleep(5)
            log('ADO_EXHAUST_DATA',
                'Exhaust', '40% PWM',
                '_Fan 2 Too Slow',
                'FAIL')
            ulog('N/A', '_Fan 2', 'FAIL')
            GDisplay('Bellwether Co. ADO',
                     'Fan 2 Too Slow',
                     '@ 40% PWM',
                     str(rev))
            p.digital_write(5, 0)
            pwm.stop()
            if debug == 1:
                button = 1
            while button != 1:
                p.digital_write(7, 1)
                time.sleep(.5)
                p.digital_write(7, 0)
                time.sleep(.5)
                button = p.digital_read(7)
            cnt += 1
            res += 1
            fail += 1
            cntlog()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    time.sleep(5)

    GDisplay('Bellwether Co. ADO',
             'Exhasut Test (PWM)',
             '"Off"',
             str(rev))
    ST4 -= 1


p.digital_write(5, 0)
pwm.stop()
time.sleep(2)
cnt += 1

log('ADO_EXHAUST_DATA',
        'Exhaust', 'N/A',
        'PASS',
        'PASS')
ulog('N/A', 'PASS', 'PASS')
mlog('ADO_MASTER_LIST_DATA', 'Exhaust', 'N/A', 'PASS', 'PASS')

print('ST4 = ', ST4)
if ST4 == 0:
    f = open('/home/pi/Bellwether/ADO_ODO_Exhaust.py', "w")
    f.write('cnt = 0')
    f.write('\n')
    f.write('ssn = ""')
    f.write('\n')
    f.write('res = 0')
    f.write('\n')
    f.write('fail = 0')
    f.close()



ST4 -=1




print("Count", cnt)
print("Stop")

GDisplay('Bellwether Co. ADO',
         'Test Complete',
         'Press Reset',
         str(rev))
p.digital_write(7, 0)


if debug == 1:
    button = 1
while button == 0:

    p.digital_write(6, 1)
    time.sleep(.5)
    p.digital_write(6,0)
    time.sleep(.5)
    button = p.digital_read(7)
p.digital_write(6, 0)
button = 0 # todo Change to "0" after debug
display.lcd_clear()

time.sleep(1)
pwm.stop()
GPIO.cleanup()
os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
