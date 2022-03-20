#!/usr/bin/env python3
import ADO_V
import os
import sys
import csv
import time
import datetime
import board
import busio
import lcddriver
import lcddriver2
from ADO_Unit import ado_
if ado_ == ('ADO5'):
    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
if ado_ == '':
    ado_ = str('NO_NAME')
    print('NO_NAME')
print (ado_)
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Main Pressure
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Leak Pressure
from ADO_Rev import rev
from ADO_D_OLED import D_OLED

from ADO_Rev import ST6
from ADO_Rev import ST6_BW
rev2 = rev [8:]
from ADO_PN_Buf import prg
from ADO_Rev import debug
from ADO_Rev import db

#For DropBox
import dropbox
from dropbox.files import WriteMode
access_token = '6c3d849c913a11'


display = lcddriver.lcd()
display2 = lcddriver2

leak_T = int (60) # Test timer
from adafruit_mcp230xx.mcp23017 import MCP23017
import pifacedigitalio as p
p.init()
i2c = busio.I2C(board.SCL, board.SDA) #todo obsolete?
loop = int(5)
loop2 = int(5)
device = str('SLT')
button = int(0)
ML = int(0)
OC_Timer = int(3)
BC_Check = int(0)
bt_time = int(1.5)
stime = time.time()
buf = datetime.datetime.now()


from ADO_ODO_PNU import ssn
from ADO_ODO_PNU import cnt
from ADO_ODO_PNU import res
from ADO_ODO_PNU import fail
from ADO_ODO_PNU import hall

from ADO_EIOp import GPAp0
from ADO_EIOp import GPAp1
from ADO_EIOp import GPAp2
from ADO_EIOp import GPAp3
from ADO_EIOp import GPAp4
from ADO_EIOp import GPAp5
from ADO_EIOp import GPAp6
from ADO_EIOp import GPAp7


from ADO_EIOi import GPAi0
from ADO_EIOi import GPAi1
from ADO_EIOi import GPAi2
from ADO_EIOi import GPAi3
from ADO_EIOi import GPAi4
from ADO_EIOi import GPAi5
from ADO_EIOi import GPAi6
from ADO_EIOi import GPAi7

from ADO_PNU_List import T1
from ADO_PNU_List import T2
from ADO_PNU_List import T3
from ADO_PNU_List import T4
from ADO_PNU_List import T5
from ADO_PNU_List import T6
from ADO_PNU_List import T7


def list():
    global T1
    global T2
    global T3
    global T4
    global T5
    global T1
    global T1
    f = open('/home/pi/Bellwether/ADO_PNU_List.py', "w")
    f.write('T1 ' + '= ' + str(T1))
    f.write('\n')
    f.write('T2 ' + '= ' + str(T2))
    f.write('\n')
    f.write('T3 ' + '= ' + str(T3))
    f.write('\n')
    f.write('T4 ' + '= ' + str(T4))
    f.write('\n')
    f.write('T5 ' + '= ' + str(T5))
    f.write('\n')
    f.write('T6 ' + '= ' + str(T6))
    f.write('\n')
    f.write('T7 ' + '= ' + str(T7))
    f.write('\n')
    f.close()
def plist():
    f = open('/home/pi/Bellwether/ADO_PNU_List.py', "w")
    f.write('T1 ' + '= ' + "int(0)")
    f.write('\n')
    f.write('T2 ' + '= ' + "int(0)")
    f.write('\n')
    f.write('T3 ' + '= ' + "int(0)")
    f.write('\n')
    f.write('T4 ' + '= ' + "int(0)")
    f.write('\n')
    f.write('T5 ' + '= ' + "int(0)")
    f.write('\n')
    f.write('T6 ' + '= ' + "int(0)")
    f.write('\n')
    f.write('T7 ' + '= ' + "int(0)")
    f.write('\n')
    f.close()
def log(path, sub, note, state, result):
    buf = datetime.datetime.now()
    rev2 = rev[8:]
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
def start():
    global BC
    global ssn
    global cnt
    global res
    global fail
    global hall
    global BC_Check
    global ST6
    global ST6_BW
    global T1
    global T2
    global T3
    global T4
    global T5
    global T6
    global T7

    while BC_Check != 1:
        GDisplay('Enter Serial #', 'Barcode', '', str(rev))
        p.digital_write(6, 1)
        p.digital_write(7, 1)
        BC = input("Enter SN Barcode ") #todo debug
        if BC == str('0000'):
            debug = 1
            timer = int(5)
            ST6 = ST6_BW
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
    if BC == ssn:
        print("Yes")
        f = open('/home/pi/Bellwether/ADO_ODO_PNU.py', "w")
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
        # f.close()
    else:
        print("No")
        cnt = 0
        res = 0
        fail = 0
        T1 = 0
        T2 = 0
        T3 = 0
        T4 = 0
        T5 = 0
        T6 = 0
        T7 = 0

        # CSV Header
        with open('/home/pi/Bellwether/ADO_PNU_DATA/_SLT_Test_' + BC + '.csv', mode='w') as Test_file:  # Rpi
            Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            Test_writer.writerow(['Time', 'ADO', 'ADO_Rev', 'PN', 'SSN', 'Cycle Count', 'Resets', 'Note',
                                  'State', 'PASS / FAIL'])
            Test_file.flush()
        f = open('/home/pi/Bellwether/ADO_ODO_PNU.py', "w")
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
        # f.close()
def sys_leak ():
    print ('System Leak Test')
    button = int(0)
    global cnt
    global cnt
    global fail
    global res
    global T1
    main_leak_T = int(15)  # Internal Test timer
    GDisplay('ADO Internal', 'Leak Test', '', str(rev))
    GPAi2.value=False
    p.digital_write(3, 1)
    time.sleep(1)
    GPAi2.value = True
    p.digital_write(3, 0)
    time.sleep(1)
    GPAi1.value=False
    time.sleep(5)
    GPAi1.value=True
    while main_leak_T != 0:
        display.lcd_display_string(str(main_leak_T), 3)
        ML = GPIO.input(5)
        if main_leak_T == 9:
            GDisplay('ADO Internal', 'Leak Test', str(main_leak_T), str(rev))
        if ML == 0:
            list()
            GDisplay('ADO Internal', 'Leak Found', '', str(rev))
            ulog('Internal Leak', 'FAIL', 'FAIL')
            log('ADO_PNU_DATA', 'SLT', 'Internal Leak', '_Internal Leak', 'FAIL')
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_PNU.py', "w")
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
            while button != 1:
                p.digital_write(7, 1)
                time.sleep(.5)
                p.digital_write(7, 0)
                time.sleep(.5)
                button = p.digital_read(7)
            GPIO.cleanup()
            p.digital_write(7, 0)
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        main_leak_T -= 1
    log('ADO_PNU_DATA', 'SLT', 'Internal Leak', '_Internal Leak', 'PASS')
    T1 = 1
    list()
    GDisplay('ADO Internal', 'Leak Test', 'PASS', str(rev))
    while button != 1:
        p.digital_write(6, 1)
        time.sleep(.5)
        p.digital_write(6, 0)
        time.sleep(.5)
        button = p.digital_read(7)
def Manifold_leak():
    print('Manifold Leak Test')
    test_timer = int(30)
    button = int(0)
    global cnt
    global cnt
    global fail
    global res
    global T2
    GDisplay('ADO External', 'Manifold Leak Test', '', str(rev))
    p.digital_write(0, 1)  # 24VDC to Relay box
    GPAi2.value = False  # Vent Line
    p.digital_write(3, 1)  # Vent Line
    time.sleep(1)
    GPAi2.value = True  # Close Vent Line
    p.digital_write(3, 0)  # Close Vent Line
    time.sleep(1)
    p.digital_write(2, 1)
    GPAi1.value = False
    GDisplay('ADO Pressurizing', 'System', 'Please Wait', str(rev))
    time.sleep(15)
    GDisplay('ADO External', 'Manifold Leak Test', '', str(rev))
    time.sleep(5)
    GPAi1.value = True
    while test_timer != 0:
        display.lcd_display_string(str(test_timer), 3)
        ML = GPIO.input(5)
        if test_timer == 9:
            GDisplay('ADO External', 'Manifold Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            GPAi1.value = False
            GDisplay('ADO External', 'Manifold Leak Found', '', str(rev))
            ulog('Manifold Leak', 'FAIL', 'FAIL')
            log('ADO_PNU_DATA', 'SLT', 'External Leak', '_Load Leak', 'FAIL')
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_PNU.py', "w")
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
            while button != 1:
                p.digital_write(7, 1)
                time.sleep(.5)
                p.digital_write(7, 0)
                time.sleep(.5)
                button = p.digital_read(7)
            GPIO.cleanup()
            p.digital_write(7, 0)
            p.digital_write(0, 0)
            p.digital_write(2, 0)
            GPAp0.value = True
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1
    log('ADO_PNU_DATA', 'SLT', 'External Leak', '_Manifold Leak', 'PASS')
    T2 = 1
    list()
    GDisplay('ADO External', 'Manifold Test', 'PASS', str(rev))
    T2 == 1
    p.digital_write(0, 0)
    p.digital_write(2, 0)
    while button != 1:
        p.digital_write(6, 1)
        time.sleep(.5)
        p.digital_write(6, 0)
        time.sleep(.5)
        button = p.digital_read(7)
def Load_leak ():
    print ('Load Leak Test')
    test_timer = int(30)
    button = int(0)
    global cnt
    global cnt
    global fail
    global res
    global T3
    GDisplay('ADO External', 'Load Leak Test', '', str(rev))
    p.digital_write(0, 1)  # 24VDC to Relay box
    GPAi2.value = False  # Vent Line
    p.digital_write(3, 1)  # Vent Line
    time.sleep(1)
    GPAi2.value = True  # Close Vent Line
    p.digital_write(3, 0)  # Close Vent Line
    time.sleep(1)
    p.digital_write(2, 1)
    GPAi1.value = False
    GPAp0.value = False
    GDisplay('ADO Pressurizing', 'System', 'Please Wait', str(rev))
    time.sleep(15)
    GDisplay('ADO External', 'Load Leak Test', '', str(rev))
    time.sleep(5)
    GPAi1.value = True
    while test_timer != 0:
        display.lcd_display_string(str(test_timer), 3)
        ML = GPIO.input(5)
        if test_timer == 9:
            GDisplay('ADO External', 'Load Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            GPAi1.value = False
            GDisplay('ADO External', 'Load Leak Found', '', str(rev))
            ulog('Load Leak', 'FAIL', 'FAIL')
            log('ADO_PNU_DATA', 'SLT', 'External Leak', '_Load Leak', 'FAIL')
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_PNU.py', "w")
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
            while button != 1:
                p.digital_write(7, 1)
                time.sleep(.5)
                p.digital_write(7, 0)
                time.sleep(.5)
                button = p.digital_read(7)
            GPIO.cleanup()
            p.digital_write(7, 0)
            p.digital_write(0, 0)
            p.digital_write(2, 0)
            GPAp0.value = True
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1
    log('ADO_PNU_DATA', 'SLT', 'External Leak', '_Load Leak', 'PASS')
    T3 = 1
    list()
    GDisplay('ADO External', 'Leak Test', 'PASS', str(rev))
    T3 == 1
    p.digital_write(0, 0)
    p.digital_write(2, 0)
    GPAp0.value = True
    while button != 1:
        p.digital_write(6, 1)
        time.sleep(.5)
        p.digital_write(6, 0)
        time.sleep(.5)
        button = p.digital_read(7)
def Exit_OPN_leak ():
    print ('Exit Open Leak Test')
    test_timer = int(30)
    button = int(0)
    global cnt
    global cnt
    global fail
    global res
    global T4
    GDisplay('ADO External', 'Exit OPN Leak Test', '', str(rev))
    p.digital_write(0, 1)  # 24VDC to Relay box
    GPAi2.value = False  # Vent Line
    p.digital_write(3, 1)  # Vent Line
    time.sleep(1)
    GPAi2.value = True  # Close Vent Line
    p.digital_write(3, 0)  # Close Vent Line
    time.sleep(1)
    p.digital_write(2, 1)
    GPAi1.value = False
    GPAp1.value = False
    GDisplay('ADO Pressurizing', 'System', 'Please Wait', str(rev))
    time.sleep(15)
    GDisplay('ADO External', 'Exit OPN Leak Test', '', str(rev))
    time.sleep(5)
    GPAi1.value = True
    while test_timer != 0:
        display.lcd_display_string(str(test_timer), 3)
        ML = GPIO.input(5)
        if test_timer == 9:
            GDisplay('ADO External', 'Exit OPN Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            GPAi1.value = False
            GDisplay('ADO External', 'EX OPN Leak Found', '', str(rev))
            log('ADO_PNU_DATA', 'SLT', 'External Leak', '_EX OPN Leak', 'FAIL')
            ulog('EX OPN Leak', 'FAIL', 'FAIL')
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_PNU.py', "w")
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
            while button != 1:
                p.digital_write(7, 1)
                time.sleep(.5)
                p.digital_write(7, 0)
                time.sleep(.5)
                button = p.digital_read(7)
            GPIO.cleanup()
            p.digital_write(7, 0)
            p.digital_write(0, 0)
            p.digital_write(2, 0)
            GPAp1.value = True
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1
    log('ADO_PNU_DATA', 'SLT', 'External Leak', '_EX OPN Leak', 'PASS')
    T4 = 1
    list()
    GDisplay('ADO External', 'Leak Test', 'PASS', str(rev))
    T4 == 1
    p.digital_write(0, 0)
    p.digital_write(2, 0)
    GPAp1.value = True
    while button != 1:
        p.digital_write(6, 1)
        time.sleep(.5)
        p.digital_write(6, 0)
        time.sleep(.5)
        button = p.digital_read(7)
def Exit_CLS_leak ():
    print ('Close Leak Test')
    test_timer = int(30)
    button = int(0)
    global cnt
    global cnt
    global fail
    global res
    global T5
    GDisplay('ADO External', 'Exit CLS Leak Test', '', str(rev))
    p.digital_write(0, 1)  # 24VDC to Relay box
    GPAi2.value = False  # Vent Line
    p.digital_write(3, 1)  # Vent Line
    time.sleep(1)
    GPAi2.value = True  # Close Vent Line
    p.digital_write(3, 0)  # Close Vent Line
    time.sleep(1)
    p.digital_write(2, 1)
    GPAi1.value = False
    GPAp2.value = False
    GDisplay('ADO Pressurizing', 'System', 'Please Wait', str(rev))
    time.sleep(15)
    GDisplay('ADO External', 'Exit CLS Leak Test', '', str(rev))
    time.sleep(5)
    GPAi1.value = True
    while test_timer != 0:
        display.lcd_display_string(str(test_timer), 3)
        ML = GPIO.input(5)
        if test_timer == 9:
            GDisplay('ADO External', 'Exit CLS Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            GPAi1.value = False
            GDisplay('ADO External', 'EX CLS Leak Found', '', str(rev))
            log('ADO_PNU_DATA', 'SLT', 'External Leak', '_EX CLS Leak', 'FAIL')
            ulog('EX CLS Leak', 'FAIL', 'FAIL')
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_PNU.py', "w")
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
            while button != 1:
                p.digital_write(7, 1)
                time.sleep(.5)
                p.digital_write(7, 0)
                time.sleep(.5)
                button = p.digital_read(7)
            GPIO.cleanup()
            p.digital_write(7, 0)
            p.digital_write(0, 0)
            p.digital_write(2, 0)
            GPAp1.value = True
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1
    log('ADO_PNU_DATA', 'SLT', 'External Leak', '_EX CLS Leak', 'PASS')
    T5
    list()
    GDisplay('ADO External', 'Leak Test', 'PASS', str(rev))
    T5 == 1
    p.digital_write(0, 0)
    p.digital_write(2, 0)
    GPAp2.value = True
    while button != 1:
        p.digital_write(6, 1)
        time.sleep(.5)
        p.digital_write(6, 0)
        time.sleep(.5)
        button = p.digital_read(7)
def Check_Valve_leak():
    print('Check Valve Leak Test')
    test_timer = int(60)
    button = int(0)
    global cnt
    global cnt
    global fail
    global res
    global T6
    GDisplay('ADO External', 'CheckValve Leak Test', '', str(rev))
    p.digital_write(0, 1)  # 24VDC to Relay box
    GPAi2.value = False  # Vent Line
    p.digital_write(3, 1)  # Vent Line
    time.sleep(1)
    GPAi2.value = True  # Close Vent Line
    p.digital_write(3, 0)  # Close Vent Line
    time.sleep(1)
    p.digital_write(2, 1)
    GPAi1.value = False
    GPAp4.value = False
    GDisplay('ADO Pressurizing', 'System', 'Please Wait', str(rev))
    time.sleep(15)
    GDisplay('ADO External', 'CheckValve Leak Test', '', str(rev))
    time.sleep(5)
    GPAi1.value = True
    while test_timer != 0:
        display.lcd_display_string(str(test_timer), 3)
        ML = GPIO.input(5)
        if test_timer == 9:
            GDisplay('ADO External', 'CheckValve Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            GPAi1.value = False
            GDisplay('ADO External', 'CheckValve Leak ', 'Found', str(rev))
            log('ADO_PNU_DATA', 'SLT', 'External Leak', '_Check Valve Leak', 'FAIL')
            ulog('CheckValve Leak', 'FAIL', 'FAIL')
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_PNU.py', "w")
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
            while button != 1:
                p.digital_write(7, 1)
                time.sleep(.5)
                p.digital_write(7, 0)
                time.sleep(.5)
                button = p.digital_read(7)
            GPIO.cleanup()
            p.digital_write(7, 0)
            p.digital_write(0, 0)
            p.digital_write(2, 0)
            GPAp3.value = True
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1
    log('ADO_PNU_DATA', 'SLT', 'External Leak', '_Check Valve Leak', 'PASS')
    T6 = 1
    list()
    GDisplay('ADO External', 'CheckValve Leak Test', 'PASS', str(rev))
    p.digital_write(0, 0)
    p.digital_write(2, 0)
    GPAp4.value = True
    while button != 1:
        p.digital_write(6, 1)
        time.sleep(.5)
        p.digital_write(6, 0)
        time.sleep(.5)
        button = p.digital_read(7)
def CDA_Purge():
    print('Check Valve Leak Test')
    test_timer = int(30)
    button = int(0)
    global cnt
    global cnt
    global fail
    global res
    global T7
    GDisplay('ADO External', 'CDA Purge Test', '', str(rev))
    p.digital_write(0, 1)  # 24VDC to Relay box
    GPAi2.value = False  # Vent Line
    p.digital_write(3, 1)  # Vent Line
    time.sleep(1)
    GPAi2.value = True  # Close Vent Line
    p.digital_write(3, 0)  # Close Vent Line
    time.sleep(1)
    p.digital_write(2, 1)
    GPAi1.value = False
    GDisplay('ADO Pressurizing', 'System', 'Please Wait', str(rev))
    time.sleep(15)
    GDisplay('ADO External', 'CDA Purge Test', '', str(rev))
    time.sleep(5)
    GPAi1.value = True
    time.sleep(1)
    GDisplay('ADO External', 'Purging Now', '', str(rev))
    GPAp3.value=False
    time.sleep(5)
    GPAp3.value=True
    ML = GPIO.input(5)
    if ML == 1:
        list()
        GDisplay('ADO External', 'CDA Purge Fail', '', str(rev))
        log('ADO_PNU_DATA', 'SLT', 'External Test', '_CDA Purge', 'FAIL')
        ulog('CDA Purge', 'FAIL', 'FAIL')
        fail += 1
        res += 1
        f = open('/home/pi/Bellwether/ADO_ODO_PNU.py', "w")
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
        while button != 1:
            p.digital_write(7, 1)
            time.sleep(.5)
            p.digital_write(7, 0)
            time.sleep(.5)
            button = p.digital_read(7)
        GPIO.cleanup()
        p.digital_write(7, 0)
        p.digital_write(0, 0)
        p.digital_write(2, 0)
        GPAp3.value = True
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
    time.sleep(1)
    test_timer -= 1
    log('ADO_PNU_DATA', 'SLT', 'External Test', '_CDA Purge', 'PASS')
    GDisplay('ADO External', 'CDA Purge Test', 'PASS', str(rev))
    T7 = 1
    list()
    p.digital_write(0, 0)
    p.digital_write(2, 0)
    GPAp3.value = True
    while button != 1:
        p.digital_write(6, 1)
        time.sleep(.5)
        p.digital_write(6, 0)
        time.sleep(.5)
        button = p.digital_read(7)






start()
GDisplay('Bellwether Co. SLT', 'System Leak Test', 'Press Start', str(rev))
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

while ST6 != 0:
    if T1 == 0:
        sys_leak()
    if T2 == 0:
        Manifold_leak()
    if T3 == 0:
        Load_leak()
    if T4 == 0:
        Exit_OPN_leak()
    if T5 == 0:
        Exit_CLS_leak()
    if T6 == 0:
        CDA_Purge()
    # if T7 == 0: #todo removed for 1.3.0 Validation
    #     Check_Valve_leak()
    ST6 -= 1

plist()
ulog('N/A', 'PASS', 'PASS')
mlog('ADO_MASTER_LIST_DATA', 'SLT', 'N/A', 'PASS', 'PASS')
GDisplay('Bellwether Co. ADO', '"Pass" Test Complete', str(cnt), str(rev))

while button != 1:
    p.digital_write(6, 1)
    time.sleep(.5)
    p.digital_write(6, 0)
    time.sleep(.5)
    button = p.digital_read(7)


os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])