#!/usr/bin/env python
import ADO_V
import time
import datetime
import csv
import lcddriver
import lcddriver2
import os
import sys
import RPi.GPIO as GPIO
from ADO import ado
from ADO_WatchDog import WD

ssn = str('')
cnt = int(0)
buf = datetime.datetime.now()
stime = time.time()
ExhaustTest_writer = str("")
spool_time = int(10) #Default 10s

# Feature Select
fancnt = int(1) # 2 = 1.3, 1 = 2.0
pwm_line = int (0)
tach_test = int(1)



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
from ADO_Report import report
open_ = open('/home/pi/Bellwether/ADO_Tag.py', 'rt')
tag = open_.read()
open_.close()

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

def fancycle(pwm, rpm):
    global cnt
    global reset
    global fail
    global button
    global res

    pwm2 = 100 - pwm
    ss = str(str(pwm)+'%')
    ado.GDisplay('Bellwether Co. ADO',
             'Exhaust Test (PWM)',
             str(ss),
             str(rev))
    fantest(pwm2)
    fan1line = ('Fan 1 RPM ' + ' ' + str(RPM_1))
    if fancnt == 2:
        fan2line = ('Fan 2 RPM ' + ' ' + str(RPM_2))
        ss = str('PWM ' + str(pwm) + '%')
        ado.GDisplay(ss,
                 str(fan1line),
                 str(fan2line),
                 str(rev))
    else:
        ss = str('PWM ' + str(pwm) + '%')
        ado.GDisplay(ss,
                 str(fan1line),
                 '',
                 str(rev))
    if RPM_1 <= rpm:
        time.sleep(5)
        report.log('Blah', 'ADO_EXHAUST_DATA', device, str(pwm), '_Fan 1 Too Slow', 'Fail', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
        ss = str('@ ' + str(pwm) + '% PWM')
        ado.GDisplay('Bellwether Co. ADO',
                 'Fan 1 Too Slow',
                 str(ss),
                 str(rev))
        ado.V48Off()
        #pwm.stop()
        if debug == 1:
            button = 1
        while button != 1:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        cnt += 1
        res += 1
        fail += 1
        cntlog()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    if fancnt == 2:
        if RPM_2 <= rpm:
            time.sleep(5)
            report.log('Blah', 'ADO_EXHAUST_DATA', device, str(pwm), '_Fan 2 Too Slow', 'Fail', tag, ado_,
                       prg, BC, cnt, res, rev, fail)
            ss = str('@ ' + str(pwm) + ' PWM')
            ado.GDisplay('Bellwether Co. ADO',
                     'Fan 2 Too Slow',
                     str(ss),
                     str(rev))
            ado.V48Off()
            #pwm.stop()
            if debug == 1:
                button = 1
            while button != 1:
                ado.B_Red()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
            cnt += 1
            res += 1
            fail += 1
            cntlog()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    time.sleep(5)


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

ado.GDisplay('Bellwether Co. ADO',
             'Exhaust Test',
             '',
             str(rev))


time.sleep(2)
ado.B_Yellow()
while BC_Check != 1:
    ado.GDisplay('Enter Serial #',
             'Barcode',
             '',
             str(rev))
    ado.B_Yellow()
    BC = input('Enter SN Barcode') #todo enable after debug
    if BC == str('0000'):
        debug = 1
        timer = int(5)
        ST4 = ST4_BW
        print('Debug Enabled via SSN')
    ado.B_Off()
    if prg_ == BC:
        ado.GDisplay('Bellwether Co. ADO',
                 'Invalid Serial #',
                 '',
                 str(rev))
        ado.B_Red()
        time.sleep(5)
        ado.B_Off()
        time.sleep(1)
    else:
        ado.GDisplay('',
                 '',
                 str(BC),
                 '')
        time.sleep(1)
        ado.GDisplay('Begin Testing',
                 '',
                 '',
                 '')
        BC_Check += 1


time.sleep(1)
ado.GDisplay('Begin Testing',
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
    report.log_h('self', 'ADO_EXHAUST_DATA', device, BC)


ado.GDisplay('Bellwether Co. ADO',
         'Press Green Button',
         'To Start',
         str(rev))


if debug == 1:
    button = 1
while button == 0:
    ado.B_Green()
    time.sleep(.5)
    ado.B_Off()
    time.sleep(.5)
    button = ado.BTN()

button = 0
time.sleep(2)

ado.GDisplay('Verify Wiring',
         'Press Green Button',
         'To Start',
         str(rev))

if debug == 1:
    button = 1
while button == 0:
    ado.B_Green()
    time.sleep(.5)
    ado.B_Off()
    time.sleep(.5)
    button = ado.BTN()

button = 0
time.sleep(2)

ado.GDisplay('Pin 1 Red -> Red',
         'Pin 2 BLK -> BLK',
         'Pin 3 WHT -> YLW',
         'Pin 4 GRN -> BLU')

if debug == 1:
    button = 1
while button == 0:
    ado.B_Green()
    time.sleep(.5)
    ado.B_Off()
    time.sleep(.5)
    button = ado.BTN()

button = 0
time.sleep(2)

if pwm_line == 1:
    #PWM Line Test # todo enable after debug
    ado.GDisplay('Bellwether Co. ADO',
             'PWM Line Test',
             '',
             str(rev))

    ado.V48()
    time.sleep(2)
    fan1 = GPIO.input(17)
    if fancnt == 2:
        fan2 = GPIO.input(18)
    ado.V48Off()

    print('PWM Line Test')
    button = 0
    if fancnt == 2:
        if fan1 != 1 and fan2 != 1:
            cnt += 1
            fail += 1
            res += 1
            ado.B_Red()
            print("Fan 1 and 2 PWM Line")
            report.log('Blah', 'ADO_EXHAUST_DATA', device, 'N/A', '_Fan 1 & 2 PWM Fail', 'Fail', tag, ado_,
                       prg, BC, cnt, res, rev, fail)

            ado.GDisplay('!!!!!!FAILURE!!!!!!!',
                     'Fan 1 & 2 PWM Line',
                     'Press Reset',
                     str(rev))
            ado.V48Off()
            #pwm.stop()
            if debug == 1:
                button = 1
            while button == 0:
                button = ado.BTN()
            ado.B_Off()
            #pwm.stop()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    if fan1 != 1:
        cnt += 1
        fail += 1
        res += 1
        ado.B_Red()
        print("Fan 1 PWM Line")
        report.log('Blah', 'ADO_EXHAUST_DATA', device, 'N/A', '_Fan 1 PWM Fail', 'Fail', tag, ado_,
                   prg, BC, cnt, res, rev, fail)

        ado.GDisplay('!!!!!!FAILURE!!!!!!!',
                 'Fan 1 PWM Line',
                 'Press Reset',
                 str(rev))
        ado.V48Off()
        if debug == 1:
            button = 1
        if button == 1:
            button = 1
        while button == 0:
            button = ado.BTN()
        ado.B_Off()
        #pwm.stop()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    if fancnt == 2:
        if fan2 != 1:
            cnt += 1
            fail += 1
            res += 1
            ado.B_Red()
            print("Fan 2 PWM Line")
            report.log('Blah', 'ADO_EXHAUST_DATA', device, 'N/A', '_Fan 2 PWM Fail', 'Fail', tag, ado_,
                       prg, BC, cnt, res, rev, fail)

            ado.GDisplay('!!!!!!FAILURE!!!!!!!',
                     'Fan 2 PWM Line',
                     'Press Reset',
                     str(rev))
            ado.V48Off()
            #pwm.stop()
            if button == 1:
                button = 1
            while button == 0:
                button = ado.BTN()
            ado.BTN()
            #pwm.stop()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    print('PWM Line Pass')

    print("Exhaust PWM")
    while IC != IC4_2:
        ado.GDisplay('Replace Cable With',
                 '"Exhaust 2"',
                 '',
                 str(rev))
        ado.B_Yellow()
        print('Replace Cable')
        print('Scan Exhaust 2')
        time.sleep(10)

        ado.GDisplay('Scan interface cable',
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
            ado.B_Off()
            ado.GDisplay('Bellwther Co. ADO',
                     'Wrong Cable',
                     'Press Reset',
                     str(rev))
            while button == 0:
                ado.B_Red()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
            ado.B_Off()
            button = 0
            display.lcd_clear()
else:
    print('PWM Line Test Pass')
    ado.V48()

button = 0 # todo change to "0" after debug


if tach_test == 1:
    # Tach Test
    ado.GDisplay('Bellwether Co. ADO',
             'Exhaust Test (Tach)',
             '5%',
             str(rev))

    ado.V48()
    pwm.start(95) # <-- 5% PWM
    time.sleep(10) #todo Change to "10" after Debug

    while ttime != 0:
        pulse = GPIO.input(26)
        if pulse == 0:
            fan1 += 1
        ttime -= 1

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
            ado.B_Red()
            print("Fail Fan 1 and Fan 2")
            report.log('Blah', 'ADO_EXHAUST_DATA', device, 'N/A', '_Fan 1 & 2 Failure', 'Fail', tag, ado_,
                       prg, BC, cnt, res, rev, fail)

            ado.GDisplay('!!!!!!FAILURE!!!!!!!',
                     'Fan 1 and Fan 2',
                     'Press Reset',
                     str(rev))
            ado.V48Off()
            #pwm.stop()
            #GPIO.cleanup()
            if debug == 1:
                button = 1
            while button == 0:
                button = ado.BTN()
            ado.B_Off()
            #pwm.stop()
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
            ado.B_Red()
            print("Fail Fan 1 and Fan 2 Power Fail")
            report.log('Blah', 'ADO_EXHAUST_DATA', device, 'N/A', '_Fan 1 & 2 Power Fail', 'Fail', tag, ado_,
                       prg, BC, cnt, res, rev, fail)

            ado.GDisplay('!!!!!!FAILURE!!!!!!!',
                     'Fan 1,2 Power Fail',
                     'Press Rest',
                     str(rev))
            ado.V48Off()
            #pwm.stop()
            #GPIO.cleanup()
            if debug == 1:
                button = 1
            while button == 0:
                button = ado.BTN()
            ado.B_Off()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    #Fan 1 Power Failure
    if fan1 == 2000:
        cnt += 1
        fail += 1
        res += 1
        ado.B_Red()
        print("Fail Fan 1 Power Fail")
        report.log('Blah', 'ADO_EXHAUST_DATA', device, 'N/A', '_Fan 1 Power Fail', 'Fail', tag, ado_,
                   prg, BC, cnt, res, rev, fail)

        ado.GDisplay('!!!!!!FAILURE!!!!!!!',
                 'Fan 1 PW/Tach Fail',
                 'Press Reset',
                 str(rev))
        ado.V48Off()
        #pwm.stop()
        if debug == 1:
            button = 1
        while button == 0:
            button = ado.BTN()
        ado.B_Off()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    #Fan 2 Power Failure
    if fancnt == 2:
        if fan2 == 2000:
            cnt += 1
            fail += 1
            res += 1
            ado.B_Red()
            print("Fail Fan 2 Power Fail")
            report.log('Blah', 'ADO_EXHAUST_DATA', device, 'N/A', '_Fan 2 Power Fail', 'Fail', tag, ado_,
                       prg, BC, cnt, res, rev, fail)

            ado.GDisplay('!!!!!!FAILURE!!!!!!!',
                     'Fan 2 PW/Tach Fail',
                     'Press Reset',
                     str(rev))

            ado.V48Off()
            #pwm.stop()
            if debug == 1:
                button = 1
            while button == 0:
                button = ado.BTN()
            ado.B_Off()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])


    #Fan 1 Tach
    if fan1 <= 10:
        cnt += 1
        fail += 1
        res += 1
        ado.B_Red()
        print("Fail Fan 1")
        report.log('Blah', 'ADO_EXHAUST_DATA', device, 'N/A', '_Fan 1 Failure', 'Fail', tag, ado_,
                   prg, BC, cnt, res, rev, fail)

        ado.GDisplay('!!!!!!FAILURE!!!!!!!',
                 'Fan 1',
                 'Press Reset',
                 str(rev))
        ado.V48Off()
        #pwm.stop()
        if debug == 1:
            button = 1
        while button == 0:
            button = ado.BTN()
        ado.B_Off()

        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    else:
        print("Pass Fan 1")

    if fancnt == 2:
        if fan2 <= 10:
            cnt += 1
            fail += 1
            res += 1
            ado.B_Red()
            print("Fail Fan 2")
            report.log('Blah', 'ADO_EXHAUST_DATA', device, 'N/A', '_Fan 2 Failure', 'Fail', tag, ado_,
                       prg, BC, cnt, res, rev, fail)

            ado.GDisplay('!!!!!!FAILURE!!!!!!!',
                     'Fan 2',
                     'Press Reset',
                     str(rev))
            ado.V48Off()
            #pwm.stop()
            if debug == 1:
                button = 1
            while button == 0:
                button = ado.BTN()
            ado.B_Off()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        else:
            print("Pass Fan 2")


    time.sleep(10)
else:
    print('Tach Test Pass')

# Here
while ST4 != 0:
    fancycle(15, 2200) # Second variable is minimum speed
    fancycle(20, 2300)
    fancycle(40, 4600)

    ado.GDisplay('Bellwether Co. ADO',
             'Exhasut Test (PWM)',
             '"Off"',
             str(rev))
    ST4 -= 1
ado.V48Off()
#pwm.stop()
time.sleep(2)
cnt += 1

report.log('Blah', 'ADO_EXHAUST_DATA', device, 'N/A', 'PASS', 'PASS', tag, ado_,
                   prg, BC, cnt, res, rev, fail)
report.mlog('Blah','ADO_MASTER_LIST_DATA', device, 'N/A', 'PASS', 'PASS', tag, ado_, prg, BC, cnt, res, rev)
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

ado.GDisplay('Bellwether Co. ADO',
         'Test Complete',
         'Press Reset',
         str(rev))
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
button = 0 # todo Change to "0" after debug
display.lcd_clear()

time.sleep(1)
#pwm.stop()
GPIO.cleanup()
os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
