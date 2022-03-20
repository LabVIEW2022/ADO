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
from ADO import ado
from ADO import ado
from ADO_SLT_Obj import slt
open_ = open('/home/pi/Bellwether/ADO_Tag.py', 'rt')
tag = open_.read()
open_.close()
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
rev2 = rev [7:]
from ADO_PN_Buf import prg
from ADO_Rev import debug
from ADO_Rev import db

#For DropBox
import dropbox
from dropbox.files import WriteMode
access_token = '6c3d849c913a11'


display = lcddriver.lcd()
display2 = lcddriver2

if debug == 1:
    leak_T = int(5)
else:
    leak_T = int (60) # Test timer



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

open_ = open('/home/pi/Bellwether/ADO_Tag.py', 'rt')
tag = open_.read()
open_.close()

from ADO_ODO_SLT import ssn
from ADO_ODO_SLT import cnt
from ADO_ODO_SLT import res
from ADO_ODO_SLT import fail
from ADO_ODO_SLT import hall


from ADO_SLT_List import T1
from ADO_SLT_List import T2
from ADO_SLT_List import T3
from ADO_SLT_List import T4
from ADO_SLT_List import T5
from ADO_SLT_List import T6
from ADO_Report import report



def list():
    global T1
    global T2
    global T3
    global T4
    global T5
    global T1
    global T1
    f = open('/home/pi/Bellwether/ADO_SLT_List.py', "w")
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
    f.close()
def plist():
    f = open('/home/pi/Bellwether/ADO_SLT_List.py', "w")
    f.write('T1 ' + '= ' + 'int(0)')
    f.write('\n')
    f.write('T2 ' + '= ' + 'int(0)')
    f.write('\n')
    f.write('T3 ' + '= ' + 'int(0)')
    f.write('\n')
    f.write('T4 ' + '= ' + 'int(0)')
    f.write('\n')
    f.write('T5 ' + '= ' + 'int(0)')
    f.write('\n')
    f.write('T6 ' + '= ' + 'int(0)')
    f.write('\n')
    f.close()
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
    global debug
    global timer

    while BC_Check != 1:
        GDisplay('Enter Serial #', 'Barcode', '', str(rev))
        ado.B_Yellow()
        BC = input("Enter SN Barcode ")
        # BC = ('222')
        if BC == str('0000'):
            debug = 1
            timer = int(5)
            ST6 = ST6_BW
            print('Debug Enabled via SSN')
        ado.B_Off()
        if prg == BC:
            GDisplay('Bellwether Co. ADO', 'Invalid Serial #', '', str(rev))
            ado.B_Red()
            time.sleep(5)
            ado.B_Off()
            time.sleep(1)
        else:
            GDisplay('', '', str(BC), '')
            time.sleep(1)
            GDisplay('Begin Testing', '', '', '')
            BC_Check += 1
    GDisplay('Begin Testing', '', '', '')
    if BC == ssn:
        print("Yes")
        f = open('/home/pi/Bellwether/ADO_ODO_SLT.py', "w")
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

        # CSV Header
        report.log_h('Self', 'ADO_SLT_DATA', device, BC)
        # with open('/home/pi/Bellwether/ADO_SLT_DATA/_SLT_Test_' + BC + '.csv', mode='w') as Test_file:  # Rpi
        #     Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #     Test_writer.writerow(['Time', 'ADO', 'ADO_Rev', 'PN', 'SSN', 'Cycle Count', 'Resets', 'Note',
        #                           'State', 'PASS / FAIL', 'User'])
        #     Test_file.flush()
        f = open('/home/pi/Bellwether/ADO_ODO_SLT.py', "w")
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
    if debug == 1:
        main_leak_T = int(5)  # Internal Test timer
    else:
        main_leak_T = int(15)  # Internal Test timer
    GDisplay('ADO Internal', 'Leak Test', '', str(rev))
    ado.PNU_ISO_(1)
    ado.CLS()
    time.sleep(1)
    ado.PNU_ISO_(0)
    ado.OCO()
    time.sleep(1)
    ado.CDA_(1)
    time.sleep(5)
    ado.CDA_(0)
    while main_leak_T != 0:
        display.lcd_display_string(str(main_leak_T), 3)
        ML = ado.Min_CDA()
        if main_leak_T == 9:
            GDisplay('ADO Internal', 'Leak Test', str(main_leak_T), str(rev))
        if ML == 0:
            list()
            GDisplay('ADO Internal', 'Leak Found', '', str(rev))
            report.log('Blah', 'ADO_SLT_DATA', device, 'Internal Leak', '_Internal Leak', 'Fail', tag, ado_,
                       prg, BC, cnt, res, rev, fail)
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_SLT.py', "w")
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
                ado.B_Red()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
                if debug == 1:
                    button = 1
            GPIO.cleanup()
            ado.B_Off()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        main_leak_T -= 1
    report.log('Blah', 'ADO_SLT_DATA', device, 'Internal Leak', '_Internal Leak', 'PASS', tag, ado_,
               prg, BC, cnt, res, rev, fail)
    T1 = 1
    list()
    GDisplay('ADO Internal', 'Leak Test', 'PASS', str(rev))
    while button != 1:
        ado.B_Green()
        time.sleep(.5)
        ado.B_Off()
        time.sleep(.5)
        button = ado.BTN()
        if debug == 1:
            button = 1
def Manifold_leak():
    print('Manifold Leak Test')
    if debug == 1:
        test_timer = int(5)
    else:
        test_timer = int(30)
    button = int(0)
    global cnt
    global cnt
    global fail
    global res
    global T2
    GDisplay('ADO External', 'Manifold Leak Test', '', str(rev))
    ado.V24A()  # 24VDC to Relay box
    ado.PNU_ISO_(1)  # Vent Line
    ado.CLS()
    time.sleep(1)

    ado.PNU_ISO_(0) # Close Vent Line

    ado.PNU_ISO_(0)

    ado.OCO() # Close Vent Line
    time.sleep(1)
    ado.OPN()
    ado.CDA_(1)
    GDisplay('ADO Pressurizing', 'System', 'Please Wait', str(rev))
    if debug == 1:
        time.sleep(1)
    else:
        time.sleep(15)
    GDisplay('ADO External', 'Manifold Leak Test', '', str(rev))
    time.sleep(5)
    ado.CDA_(0)
    while test_timer != 0:
        display.lcd_display_string(str(test_timer), 3)
        ML = ado.Min_CDA()
        if test_timer == 9:
            GDisplay('ADO External', 'Manifold Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            ado.CDA_(1)
            GDisplay('ADO External', 'Manifold Leak Found', '', str(rev))
            report.log('Blah', 'ADO_SLT_DATA', device, 'External Leak', '_Load Leak', 'Fail', tag, ado_,
                       prg, BC, cnt, res, rev, fail)
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_SLT.py', "w")
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
                ado.B_Red()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
                if debug == 1:
                    button = 1
            ado.B_Off()
            ado.V24Off()
            ado.OCO()
            slt.V0(0)

            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1
    report.log('Blah', 'ADO_SLT_DATA', device, 'External Leak', '_Manifold Leak', 'PASS', tag, ado_,
               prg, BC, cnt, res, rev, fail)
    T2 = 1
    list()
    ado.V24Off()
    ado.OPN()

    while button != 1:
        ado.B_Green()
        time.sleep(.5)
        ado.B_Off()
        time.sleep(.5)
        button = ado.BTN()
        if debug == 1:
            button = 1
def Load_leak ():
    print ('Load Leak Test')
    if debug == 1:
        test_timer = int(5)
    else:
        test_timer = int(30)
    button = int(0)
    global cnt
    global cnt
    global fail
    global res
    global T3
    GDisplay('ADO External', 'Load Leak Test', '', str(rev))
    ado.V24A()  # 24VDC to Relay box
    ado.CDA_(1)
    ado.PNU_ISO_(1)
    ado.CLS()
    time.sleep(.25)  # Close Vent Line
    ado.PNU_ISO_(0)
    ado.OCO()
    time.sleep(1)
    ado.OPN()
    ado.PNU_ISO_(1)
    slt.V2(1)
    GDisplay('ADO Pressurizing', 'System', 'Please Wait', str(rev))
    if debug == 1:
        time.sleep(1)
    else:
        time.sleep(15)
    GDisplay('ADO External', 'Load Leak Test', '', str(rev))
    time.sleep(5)
    ado.CDA_(0)
    while test_timer != 0:
        display.lcd_display_string(str(test_timer), 3)
        ML = ado.Min_CDA()
        if test_timer == 9:
            GDisplay('ADO External', 'Load Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            ado.CDA_(1)
            GDisplay('ADO External', 'Load Leak Found', '', str(rev))
            report.log('Blah', 'ADO_SLT_DATA', device, 'External Leak', '_Load Leak', 'Fail', tag, ado_,
                       prg, BC, cnt, res, rev, fail)
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_SLT.py', "w")
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
                ado.B_Red()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
                if debug == 1:
                    button = 1
            GPIO.cleanup()
            ado.B_Off()
            ado.V24Off()
            ado.OCO()
            slt.V2(0)
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1
    report.log('Blah', 'ADO_SLT_DATA', device, 'External Leak', '_Load Leak', 'PASS', tag, ado_,
               prg, BC, cnt, res, rev, fail)
    T3 = 1
    list()
    GDisplay('ADO External', 'Leak Test', 'PASS', str(rev))
    ado.V24Off()
    ado.OCO()
    slt.V2(0)
    while button != 1:
        ado.B_Green()
        time.sleep(.5)
        ado.B_Off()
        time.sleep(.5)
        button = ado.BTN()
        if debug == 1:
            button = 1
def BD_leak ():
    print ('BD Leak Test')
    if debug == 1:
        test_timer = int(5)
    else:
        test_timer = int(30)
    button = int(0)
    global cnt
    global fail
    global res
    global T4
    GDisplay('ADO External', 'BD Leak Test', '', str(rev))
    ado.V24A()  # 24VDC to Relay box
    ado.CDA_(1)
    ado.PNU_ISO_(1)
    ado.CLS()
    time.sleep(.25)  # Close Vent Line
    ado.PNU_ISO_(0)
    ado.OCO()
    time.sleep(1)
    ado.OPN()
    ado.PNU_ISO_(1)
    slt.V1(1)
    GDisplay('ADO Pressurizing', 'System', 'Please Wait', str(rev))
    if debug == 1:
        time.sleep(1)
    else:
        time.sleep(15)
    GDisplay('ADO External', 'BD Leak Test', '', str(rev))
    time.sleep(5)
    ado.CDA_(0)
    while test_timer != 0:
        display.lcd_display_string(str(test_timer), 3)
        ML = ado.Min_CDA()
        if test_timer == 9:
            GDisplay('ADO External', 'BD Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            ado.CDA_(1)
            GDisplay('ADO External', 'BD Leak Found', '', str(rev))
            report.log('Blah', 'ADO_SLT_DATA', device, 'External Leak', '_BD Leak', 'Fail', tag, ado_,
                       prg, BC, cnt, res, rev, fail)
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_SLT.py', "w")
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
                ado.B_Red()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
                if debug == 1:
                    button = 1
            GPIO.cleanup()
            ado.B_Off()
            ado.V24Off()
            ado.OCO()
            slt.V1(0)
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1
    report.log('Blah', 'ADO_SLT_DATA', device, 'External Leak', '_BD Leak', 'PASS', tag, ado_,
               prg, BC, cnt, res, rev, fail)
    T4 = 1
    list()
    GDisplay('ADO External', 'Leak Test', 'PASS', str(rev))
    ado.V24Off()
    ado.OCO()
    slt.V1(0)
    while button != 1:
        ado.B_Green()
        time.sleep(.5)
        ado.B_Off()
        time.sleep(.5)
        button = ado.BTN()
        if debug == 1:
            button = 1
def Exit_leak ():
    print ('Exit Leak Test')
    if debug == 1:
        test_timer = int(5)
    else:
        test_timer = int(30)
    button = int(0)
    global cnt
    global cnt
    global fail
    global res
    global T5
    GDisplay('ADO External', 'Exit Leak Test', '', str(rev))
    ado.V24A()
    ado.PNU_ISO_(1)
    ado.CLS()
    time.sleep(1)
    ado.PNU_ISO_(0)
    ado.OCO()
    time.sleep(1)


    ado.OPN()

    ado.OPN()
    ado.CDA_(1)
    slt.V0(1)
    GDisplay('ADO Pressurizing', 'System', 'Please Wait', str(rev))
    if debug == 1:
        time.sleep(1)
    else:
        time.sleep(15)
    GDisplay('ADO External', 'Exit Leak Test', '', str(rev))
    time.sleep(5)




    ado.CDA_(0)
    while test_timer != 0:
        display.lcd_display_string(str(test_timer), 3)
        ML = ado.Min_CDA()
        if test_timer == 9:
            GDisplay('ADO External', 'Exit Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            ado.CDA_(1)
            GDisplay('ADO External', 'EX Leak Found', '', str(rev))
            report.log('Blah', 'ADO_SLT_DATA', device, 'External Leak', '_EX Leak', 'FAIL', tag, ado_,
                       prg, BC, cnt, res, rev, fail)
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_SLT.py', "w")
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
                ado.B_Red()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
                if debug == 1:
                    button = 1
            GPIO.cleanup()
            ado.B_Off()
            ado.V24Off()
            ado.OCO()

            slt.V0(0)

            slt.V1(0)

            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1
    report.log('Blah', 'ADO_SLT_DATA', device, 'External Leak', '_EX Leak', 'PASS', tag, ado_,
               prg, BC, cnt, res, rev, fail)
    T5 = 1
    list()
    GDisplay('ADO External', 'Leak Test', 'PASS', str(rev))
    ado.V24Off()
    ado.OCO()

    slt.V0(0)
    slt.V1(0)
    while button != 1:
        ado.B_Green()
        time.sleep(.5)
        ado.B_Off()
        time.sleep(.5)
        button = ado.BTN()
        if debug == 1:
            button = 1
def Chaff_Can_leak():
    print('Chaff Valve Leak Test')
    if debug == 1:
        test_timer = int(5)
    else:
        test_timer = int(30)
    button = int(0)
    global cnt
    global cnt
    global fail
    global res
    global T6
    GDisplay('ADO External', 'ChaffValve Leak Test', '', str(rev))
    ado.V24A()  # 24VDC to Relay box
    ado.PNU_ISO_(1)  # Vent Line
    ado.CLS()  # Vent Line
    time.sleep(1)
    ado.PNU_ISO_(0)  # Close Vent Line
    ado.OCO()  # Close Vent Line
    time.sleep(1)
    ado.OPN()
    ado.CDA_(1)
    slt.V3(1)
    GDisplay('ADO Pressurizing', 'System', 'Please Wait', str(rev))
    if debug == 1:
        time.sleep(1)
    else:
        time.sleep(15)
    GDisplay('ADO External', 'ChaffValve Leak Test', '', str(rev))
    time.sleep(5)
    ado.CDA_(0)
    while test_timer != 0:
        display.lcd_display_string(str(test_timer), 3)
        ML = ado.Min_CDA()
        if test_timer == 9:
            GDisplay('ADO External', 'ChaffValve Leak Test', str(test_timer), str(rev))
        if ML == 0:
            list()
            ado.CDA_(1)
            GDisplay('ADO External', 'ChaffValve Leak ', 'Found', str(rev))
            report.log('Blah', 'ADO_SLT_DATA', device, 'External Leak', '_Chaff Valve Leak', 'FAIL', tag, ado_,
                       prg, BC, cnt, res, rev, fail)
            fail += 1
            res += 1
            f = open('/home/pi/Bellwether/ADO_ODO_SLT.py', "w")
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
                ado.B_Red()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
                if debug == 1:
                    button = 1
            GPIO.cleanup()
            ado.B_Off()
            ado.V24Off()
            ado.OCO()
            slt.V2(0)
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        time.sleep(1)
        test_timer -= 1
    report.log('Blah', 'ADO_SLT_DATA', device, 'External Leak', '_Chaff Valve Leak', 'PASS', tag, ado_,
               prg, BC, cnt, res, rev, fail)
    T6 = 1
    list()
    GDisplay('ADO External', 'ChaffValve Leak Test', 'PASS', str(rev))
    ado.V24Off()
    ado.OCO()
    slt.V2(0)
    while button != 1:
        ado.B_Green()
        time.sleep(.5)
        ado.B_Off()
        time.sleep(.5)
        button = ado.BTN()
        if debug == 1:
            button = 1





start()
GDisplay('Bellwether Co. SLT', 'System Leak Test', 'Press Start', str(rev))
if debug == 1:
    button = 1
print ('Press Button to start')
while button == 0:
    ado.B_Green()
    time.sleep(.5)
    ado.B_Off()
    time.sleep(.5)
    button = ado.BTN()
ado.B_Off()
button = 0
if debug == 1:
    button = 1
while ST6 != 0:
    if T1 == 0:
        sys_leak()
    if T2 == 0:
        Manifold_leak()
    if T3 == 0:
        Load_leak()
    if T4 == 0:
        BD_leak()
    if T5 == 0:
        Exit_leak()
    if T6 == 0:
        Chaff_Can_leak()
    ST6 -= 1

plist()
report.mlog('Blah','ADO_MASTER_LIST_DATA', device, 'N/A', 'PASS', 'PASS', tag, ado_, prg, BC, cnt, res, rev)
GDisplay('Bellwether Co. ADO', '"Pass" Test Complete', str(cnt), str(rev))

while button != 1:
    ado.B_Green()
    time.sleep(.5)
    ado.B_Off()
    time.sleep(.5)
    button = ado.BTN()


os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])