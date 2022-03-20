#!/usr/bin/env python
import ADO_V
import datetime
import csv
import time
import sys
import lcddriver
import lcddriver2
import pifacedigitalio as p
import os
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
from ADO_Unit import ado_
if ado_ == '':
    ado_ = str('NO_NAME')
    print ('NO_NAME')
from ADO_Rev import rev
rev2 = rev [7:]
from ADO_Rev import ST5
from ADO_Rev import ST5_BW
from ADO_PN_Buf import prg
from ADO_Rev import debug
from ADO_Rev import db
from ADO_D_OLED import D_OLED
from ADO_E_IO import E_IO
from ADO_ODO_HVC import cnt
from ADO_ODO_HVC import ssn
from ADO_Unit import ado_
from ADO import ado
open_ = open('/home/pi/Bellwether/ADO_Tag.py', 'rt')
tag = open_.read()
open_.close()

from ADO_ODO_HVC import res
from ADO_ODO_HVC import fail
from ADO_HVC_LOG import ctest1
from ADO_HVC_LOG import ctest2
from ADO_HVC_LOG import ctest3
from ADO_HVC_LOG import ctest4
from ADO_HVC_LOG import ctest5
stime = time.time()


# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)
eio = MCP23017(i2c, address=0x22)  # MCP23017
BC_Check = int(0)
p.init()



# Sets pins
GPA0 = eio.get_pin(0)  # GPA0
GPA1 = eio.get_pin(1)  # GPA1
GPA2 = eio.get_pin(2)  # GPA2
GPA3 = eio.get_pin(3)  # GPA3
GPA4 = eio.get_pin(4)  # GPA4
GPA5 = eio.get_pin(5)  # GPA5
GPA6 = eio.get_pin(6)  # GPA6
GPA7 = eio.get_pin(7)  # GPA7

GPB0 = eio.get_pin(8)  # GPB0
GPB1 = eio.get_pin(9)  # GPB1
GPB2 = eio.get_pin(10)  # GPB2
GPB3 = eio.get_pin(11)  # GPB3
GPB4 = eio.get_pin(12)  # GPB4
GPB5 = eio.get_pin(13)  # GPB5
GPB6 = eio.get_pin(14)  # GPB6
GPB7 = eio.get_pin(15)  # GPB7



display = lcddriver.lcd()
if D_OLED == 1:
    display2 = lcddriver2.lcd2()

if ado_ == ('ADO5'):
    print ('')
else:
    if E_IO != 1:
        display.lcd_clear()
        display.lcd_display_string('See Display on EIO', 2)
        display.lcd_display_string('Module',3)
        if D_OLED == 1:
            display2.lcd2_clear()
            display2.lcd2_display_string('Expanded IO Module', 1)
            display2.lcd2_display_string('Not Detected', 2)
            display2.lcd2_display_string('Reboot......',4)


        f = open('ADO_HW_Bootcheck.py', "w")
        f.write('HW_C = int(1)')
        f.write('\n')
        f.close()

        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_NET.py', *sys.argv[1:])
    else:
        f = open('ADO_HW_Bootcheck.py', "w")
        f.write('HW_C = int(0)')
        f.write('\n')
        f.close()
#Truth Table

# L1
T11 = int()
T12 = int()
T13 = int()
T1E = int()
# L2
T21 = int()
T22 = int()
T23 = int()
T2E = int()
# L3
T31 = int()
T32 = int()
T33 = int()
T3E = int()
# Earth
TE1 = int()
TE2 = int()
TE3 = int()
TEE = int()


L1 = int(0)
L2 = int(0)
L3 = int(0)

fl1 = str()
fl2 = str()
fl3 = str()
fl4 = str()

L1_Byte = str()
L2_Byte = str()
L3_Byte = str()
Earth_Byte = str()

Earth = int(0)
button = int(0)
button2 = int(0)
cnt = int(0)
cnt2 = int(0)
buz =int(0)
ERR_Buf = int(1)
ERR_Buf2 = int(0)
note =str('')
test = str('')
device = str('Panel')

ERR_L1 =int()
ERR_L2 =int()
ERR_L3 =int()
ERR_Earth =int()
cntdwn = int(5) # Count down timer
buz = int(2)






def D_Results():
    global buz
    while buz != 0:
        GPB5.value = False
        time.sleep(.1)
        GPB5.value = True
        time.sleep(.1)
        buz -= 1
    buz = 2
    if D_OLED == 1:
        print('')
        display2.lcd2_clear()
        display2.lcd2_clear()
        display2.lcd2_display_string(str(fl1), 1)
        display2.lcd2_display_string(str(fl2), 2)
        display2.lcd2_display_string(str(fl3), 3)
        display2.lcd2_display_string(str(fl4), 4)
        print(fl1)
        print(fl2)
        print(fl3)
        print(fl4)
    else:
        print ('')
        display.lcd_clear()
        display.lcd_clear()
        display.lcd_display_string(str(fl1), 1)
        display.lcd_display_string(str(fl2), 2)
        display.lcd_display_string(str(fl3), 3)
        display.lcd_display_string(str(fl4), 4)
        print(fl1)
        print(fl2)
        print(fl3)
        print(fl4)
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
    buf = datetime.datetime.now()
    global etime
    import time
    end = time.time()
    hours, rem = divmod(end - stime, 3600)
    minutes, seconds = divmod(rem, 60)
    etime = ("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
    with open('/home/pi/Bellwether/' + str(ado_) + '_' + 'Useage_Log.csv', mode='a') as Test_file: # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([buf, ado_, device, BC, cnt, res, note, state, result, rev2, etime, tag])
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
def mlog (path, sub,note , state, result):
    buf = datetime.datetime.now()
    with open('/home/pi/Bellwether/' + path + '/' + sub + '_Master_List.csv', mode='a') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([buf, ado_, rev2, prg, BC, cnt, res,note, state, result, tag])
        Test_file.flush()
def L1(test):
    # L1
    global cnt
    global res
    global fail
    global hall
    global ERR_Buf
    global fl1
    global note
    global ERR_L1
    ERR_Buf = 0
    # global test
    GPB1.value = 0
    # GPIO.setup(35, GPIO.IN) #L2_O pin change for short test
    GPB2.direction = digitalio.Direction.INPUT
    GPB2.pull = digitalio.Pull.UP
    # GPIO.setup(38, GPIO.IN) #L3_O pin change for short test
    GPB3.direction = digitalio.Direction.INPUT
    GPB3.pull = digitalio.Pull.UP
    # GPIO.setup(24, GPIO.IN) #Earth_O pin change for short test
    GPB0.direction = digitalio.Direction.INPUT
    GPB0.pull = digitalio.Pull.UP

    T11 = GPA1.value
    if T11 == True:
        T11 = 0
    else:
        T11 = 1
    print('T11', T11)

    T12 = GPA2.value
    if T12 == True:
        T12 = 0
    else:
        T12 = 1
    print('T12', T12)

    T13 = GPA3.value
    if T13 == True:
        T13 = 0
    else:
        T13 = 1
    print('T13', T13)

    T1E = GPA0.value
    if T1E == True:
        T1E = 0
    else:
        T1E = 1
    print('T1E', T1E)

    # GPIO.setup(35, GPIO.OUT) #L2_O pin change for short test
    GPB2.switch_to_output(value=True)  # todo check GPIO state for equivelent
    # GPIO.setup(38, GPIO.OUT) #L3_O pin change for short test
    GPB3.switch_to_output(value=True)
    # GPIO.setup(24, GPIO.OUT) #Earth_O pin change for short test
    GPB0.switch_to_output(value=True)
    # GPIO.output(31, 0)
    GPB1.value = False
    L1_Byte = str(T11) + str(T12) + str(T13) + str(T1E)
    print('L1   ', T11, T12, T13, T1E)

    if L1_Byte == '0000':
        fl1 = 'L1        Open'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 Open', 'FAIL')
        ulog('L1 Open', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '0001':
        fl1 = 'L1 X Earth'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 X Earth', 'FAIL')
        ulog('L1 X Earth', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '0010':
        fl1 = 'L1 X L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 X L3', 'FAIL')
        ulog('L1 X L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '0011':
        fl1 = 'L1 OPN, Short L3,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 OPN, Short L3,E', 'FAIL')
        ulog('L1 OPN, Short L3,E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '0100':
        fl1 = 'L1 X L2'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 X L2', 'FAIL')
        ulog('L1 X L2', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '0101':
        fl1 = 'L1 OPN, Short L2,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 OPN, Short L2,E', 'FAIL')
        ulog('L1 OPN, Short L2,E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '0110':
        fl1 = 'L1 OPN, Short L2,L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 OPN, Short L2,L3', 'FAIL')
        ulog('L1 OPN, Short L2,L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '0111':
        fl1 = 'L1 OPN Short L2,L3,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 OPN Short L2,L3,E', 'FAIL')
        ulog('L1 OPN Short L2,L3,E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '1000':
        fl1 = 'L1              Pass'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 PASS', 'PASS')
        ulog('L1 PASS', 'PASS', 'PASS')
        # ERR_Buf += 1
    if L1_Byte == '1001':
        fl1 = 'L1 Short E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 Short E', 'FAIL')
        ulog('L1 Short E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '1010':
        fl1 = 'L1 Short L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 Short L3', 'FAIL')
        ulog('L1 Short L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '1011':
        fl1 = 'L1 Short L3,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 Short L3,E', 'FAIL')
        ulog('L1 Short L3,E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '1100':
        fl1 = 'L1 Short L2'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 Short L2', 'FAIL')
        ulog('L1 Short L2', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '1101':
        fl1 = 'L1 Short L2,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 Short L2,E', 'FAIL')
        ulog('L1 Short L2,E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '1110':
        fl1 = 'L1 Short L2,L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L1 Short L2,L3', 'FAIL')
        ulog('L1 Short L2,L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L1_Byte == '1111':
        fl1 = 'L1        All Short'
        log('ADO_HVC_DATA', 'HVC', str(test), 'All Short', 'FAIL')
        ulog('All Short', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if ERR_Buf >= 1:
        ERR_L1 = 1
def L2(test):
    # L2
    # GPIO.output(35, 1)
    global cnt
    global res
    global fail
    global hall
    global fl2
    global ERR_Buf
    global note
    global ERR_L2
    ERR_Buf = 0
    GPB2.value = False
    # GPIO.setup(31, GPIO.IN) #L1_O pin change for short test
    GPB1.direction = digitalio.Direction.INPUT
    GPB1.pull = digitalio.Pull.UP
    # GPIO.setup(38, GPIO.IN) #L3_O pin change for short test
    GPB3.direction = digitalio.Direction.INPUT
    GPB3.pull = digitalio.Pull.UP
    # GPIO.setup(24, GPIO.IN) #Earth_O pin change for short test
    GPB0.direction = digitalio.Direction.INPUT
    GPB0.pull = digitalio.Pull.UP

    # T21 = GPIO.input(29)
    T21 = GPA1.value
    if T21 == True:
        T21 = 0
    else:
        T21 = 1
    print('T21', T21)

    # T22 =  GPIO.input(33)
    T22 = GPA2.value
    if T22 == True:
        T22 = 0
    else:
        T22 = 1
    print('T22', T22)

    # T23 = GPIO.input(36)
    T23 = GPA3.value
    if T23 == True:
        T23 = 0
    else:
        T23 = 1
    print('T23', T23)

    # T2E = GPIO.input(22)
    T2E = GPA0.value
    if T2E == True:
        T2E = 0
    else:
        T2E = 1
    print ('T2E', T2E)

    # GPIO.setup(31, GPIO.OUT) #L1_O pin change for short test
    GPB1.switch_to_output(value=True)
    # GPIO.setup(38, GPIO.OUT) #L3_O pin change for short test
    GPB3.switch_to_output(value=True)
    # GPIO.setup(24, GPIO.OUT) #Earth_O pin change for short test
    GPB0.switch_to_output(value=True)
    # GPIO.output(35, 0)
    GPB2.value = True
    L2_Byte = str(T21)+str(T22)+ str(T23)+ str(T2E)
    print ('L2   ',T21,T22,T23,T2E)

    if L2_Byte == '0000':
        fl2 = 'L2        Open'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 Open', 'FAIL')
        ulog('L2 Open', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '0001':
        fl2 = 'L2 X Earth'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 X Earth', 'FAIL')
        ulog('L2 X Earth', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '0010':
        fl2 = 'L2 X L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 X L3', 'FAIL')
        ulog('L2 X L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '0011':
        fl2 = 'L2 OPN, Short L3,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 OPN, Short L3,E', 'FAIL')
        ulog('L2 OPN, Short L3,E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '0100':
        fl2 = 'L2              Pass'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 PASS', 'PASS')
        ulog('L2 PASS', 'PASS', 'PASS')
        # ERR_Buf += 1
    if L2_Byte == '0101':
        fl2 = 'L2 Short E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 Shore E', 'FAIL')
        ulog('L2 Shore E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '0110':
        fl2 = 'L2 Short L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 Shore L3', 'FAIL')
        ulog('L2 Shore L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '0111':
        fl2 = 'L2 Short L3, E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 Shore L3, E', 'FAIL')
        ulog('L2 Shore L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '1000':
        fl2 = 'L2 X L1'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 X L1', 'FAIL')
        ulog('L2 X L1', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '1001':
        fl2 = 'L2 OPN, Short L1,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 OPN, Short L1, E', 'FAIL')
        ulog('L2 OPN, Short L1', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '1010':
        fl2 = 'L2 OPN, Short L1,L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 OPN, Short L1, L3','FAIL')
        ulog('L2 OPN, Short L1, L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '1011':
        fl2 = 'L2 OPN Short L1,L3,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 OPN Short L1,L3,E', 'FAIL')
        ulog('L2 OPN Short L1,L3,E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '1100':
        fl2 = 'L2 Short L1'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 Shore L1', 'FAIL')
        ulog('L2 Shore L1', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '1101':
        fl2 = 'L2 Short L1, E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 Short L1, E', 'FAIL')
        ulog('L2 Short L1, E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '1110':
        fl2 = 'L2 Short L1, L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L2 Short L1, L3', 'FAIL')
        ulog('L2 Short L1, L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L2_Byte == '1111':
        fl2 = 'L2        All Short'#
        log('ADO_HVC_DATA', 'HVC', str(test), 'All Short', 'FAIL')
        ulog('All Short', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if ERR_Buf >= 1:
        ERR_L2 = 1
def L3(test):
    # L3
    global cnt
    global res
    global fail
    global hall
    global fl3
    global ERR_Buf
    global note
    global ERR_L3
    ERR_Buf = 0
    GPB3.value = False
    # GPIO.setup(31, GPIO.IN) #L1_O pin change for short test
    GPB1.direction = digitalio.Direction.INPUT
    GPB1.pull = digitalio.Pull.UP
    # GPIO.setup(35, GPIO.IN) #L2_O pin change for short test
    GPB2.direction = digitalio.Direction.INPUT
    GPB2.pull = digitalio.Pull.UP
    # GPIO.setup(24, GPIO.IN) #Earth_O pin change for short test
    GPB0.direction = digitalio.Direction.INPUT
    GPB0.pull = digitalio.Pull.UP

    # T31 = GPIO.input(29)
    T31 = GPA1.value
    if T31 == True:
        T31 = 0
    else:
        T31 = 1
    print('T31', T31)

    # T32 =  GPIO.input(33)
    T32 = GPA2.value
    if T32 == True:
        T32 = 0
    else:
        T32 = 1
    print('T32', T32)

    # T33 = GPIO.input(36)
    T33 = GPA3.value
    if T33 == True:
        T33 = 0
    else:
        T33 = 1
    print('T33', T33)

    # T3E = GPIO.input(22)
    T3E = GPA0.value
    if T3E == True:
        T3E = 0
    else:
        T3E = 1
    print('T3E', T31)

    # GPIO.setup(31, GPIO.OUT) #L1_O pin change for short test
    GPB1.switch_to_output(value=True)
    # GPIO.setup(35, GPIO.OUT) #L2_O pin change for short test
    GPB2.switch_to_output(value=True)
    # GPIO.setup(24, GPIO.OUT) #Earth_O pin change for short test
    GPB0.switch_to_output(value=True)

    # GPIO.output(38, 0)
    GPB3.value = True
    L3_Byte = str(T31)+str(T32)+ str(T33)+ str(T3E)
    print ('L3   ',T31,T32,T33,T3E)

    if L3_Byte == '0000':
        fl3 = 'L3        Open'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 Open', 'FAIL')
        ulog('L3 Open', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '0001':
        fl3 = 'L3 X Earth'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 X Earth', 'FAIL')
        ulog('L3 X Earth', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '0010':
        fl3 = 'L3              Pass'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 PASS', 'PASS')
        ulog('L3 PASS', 'PASS', 'PASS')
        # ERR_Buf += 1
    if L3_Byte == '0011':
        fl3 = 'L3 Short E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 Short E', 'FAIL')
        ulog('L3 Short E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '0100':
        fl3 = 'L3 X L2'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 X L2', 'FAIL')
        ulog('L3 X L2', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '0101':
        fl3 = 'L3 OPN, Short L2,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 OPN, Short L2,E', 'FAIL')
        ulog('L3 OPN, Short L2,E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '0110':
        fl3 = 'L3 Short L2'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 Short L2', 'FAIL')
        ulog('L3 Short L2', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '0111':
        fl3 = 'L3 Short L2,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 Short L2,E', 'FAIL')
        ulog('L3 Short L2,E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '1000':
        fl3 = 'L3 X L1'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 X L1', 'FAIL')
        ulog('L3 X L1', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '1001':
        fl3 = 'L3 OPN, Short L1,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 OPN, Short L1,E', 'FAIL')
        ulog('L3 OPN, Short L1,E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '1010':
        fl3 = 'L3 Short L1'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 Short L1', 'FAIL')
        ulog('L3 Short L1', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '1011':
        fl3 = 'L3 Short L1,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 Short L1,E', 'FAIL')
        ulog('L3 Short L1,E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '1100':
        fl3 = 'L3 OPN, Short L1,L2'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 OPN, Short L1,L2', 'FAIL')
        ulog('L3 OPN, Short L1,L2', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '1101':
        fl3 = 'L3 OPN Short L1,L2,E'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 OPN Short L1,L2,E', 'FAIL')
        ulog('L3 OPN Short L1,L2,E', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '1110':
        fl3 = 'L3 Short L1, L2'
        log('ADO_HVC_DATA', 'HVC', str(test), 'L3 Short L1, L2', 'FAIL')
        ulog('L3 Short L1, L2', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if L3_Byte == '1111':
        fl3 = 'L3        All Short'
        log('ADO_HVC_DATA', 'HVC', str(test), 'All Short', 'FAIL')
        ulog('All Short', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if ERR_Buf >= 1:
        ERR_L3 = 1
def Earth(test):
    # Earth
    global cnt
    global res
    global fail
    global hall
    global fl4
    global ERR_Buf
    global note
    global ERR_Earth
    ERR_Buf = 0
    GPB0.value = False
    # GPIO.setup(31, GPIO.IN) #L1_O pin change for short test
    GPB1.direction = digitalio.Direction.INPUT
    GPB1.pull = digitalio.Pull.UP
    # GPIO.setup(35, GPIO.IN) #L2_O pin change for short test
    GPB2.direction = digitalio.Direction.INPUT
    GPB2.pull = digitalio.Pull.UP
    # GPIO.setup(38, GPIO.IN) #L3_O pin change for short test
    GPB3.direction = digitalio.Direction.INPUT
    GPB3.pull = digitalio.Pull.UP

    # TE1 = GPIO.input(29)
    TE1 = GPA1.value
    if TE1 == True:
        TE1 = 0
    else:
        TE1 = 1
    print('TE1', TE1)

    # TE2 =  GPIO.input(33)
    TE2 = GPA2.value
    if TE2 == True:
        TE2 = 0
    else:
        TE2 = 1
    print('TE2', TE2)

    # TE3 = GPIO.input(36)
    TE3 = GPA3.value
    if TE3 == True:
        TE3 = 0
    else:
        TE3 = 1
    print('TE3', TE3)

    # TEE = GPIO.input(22)
    TEE = GPA0.value
    if TEE == True:
        TEE = 0
    else:
        TEE = 1
    print('TEE', TEE)

    # GPIO.output(24, 0)
    GPB0.value = True

    # GPIO.setup(31, GPIO.OUT) #L1_O pin change for short test
    GPB1.switch_to_output(value=True)
    # GPIO.setup(35, GPIO.OUT) #L2_O pin change for short test
    GPB2.switch_to_output(value=True)
    # GPIO.setup(38, GPIO.OUT) #L3_O pin change for short test
    GPB3.switch_to_output(value=True)

    Earth_Byte = str(TE1)+str(TE2)+ str(TE3)+ str(TEE)
    print (' E   ',TE1,TE2,TE3,TEE)

    if Earth_Byte == '0000':
        fl4 = ' E        Open'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E Open', 'FAIL')
        ulog('E Open', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '0001':
        fl4 = ' E              Pass'
        log('ADO_HVC_DATA', 'HVC', str(test), 'Earth PASS', 'PASS')
        ulog('Earth', 'PASS', 'PASS')
        # ERR_Buf += 1
    if Earth_Byte == '0010':
        fl4 = ' E X L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E X L3', 'FAIL')
        ulog('E X L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '0011':
        fl4 = ' E Short L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E Short L3', 'FAIL')
        ulog('E Short L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '0100':
        fl4 = ' E X L2'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E X L2', 'FAIL')
        ulog('E X L2', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '0101':
        fl4 = ' E Short L2'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E Short L2', 'FAIL')
        ulog('E Short L2', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '0110':
        fl4 = ' E OPN, Short L2,L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E OPN, Short L2, L3', 'FAIL')
        ulog('E OPN, Short L2, L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '0111':
        fl4 = ' E Short L2,L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E Short L2,L3', 'FAIL')
        ulog('E Short L2, L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '1000':
        fl4 = ' E X L1'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E X L1', 'FAIL')
        ulog('E X L1', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '1001':
        fl4 = ' E Short L1'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E Short L1', 'FAIL')
        ulog('E Short L1', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '1010':
        fl4 = ' E OPN, Short L1,L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E OPN, Short L1,L3', 'FAIL')
        ulog('E OPN, Short L1,L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '1011':
        fl4 = ' E Short L1,L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E Short L1,L3', 'FAIL')
        ulog('E Short L1,L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '1100':
        fl4 = ' E OPN, Short L1,L2'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E OPN, Short L1,L2', 'FAIL')
        ulog('E OPN, Short L1,L2', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '1101':
        fl4 = ' E Short L1,L2'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E Short L1,L2', 'FAIL')
        ulog('E Short L1,L2', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '1110':
        fl4 = 'E OPN Short L1,L2,L3'
        log('ADO_HVC_DATA', 'HVC', str(test), 'E OPN Short L1,L2,L3', 'FAIL')
        ulog('E OPN Short L1,L2,L3', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if Earth_Byte == '1111':
        fl4 = ' E        All Short'
        log('ADO_HVC_DATA', 'HVC', str(test), 'All Short', 'FAIL')
        ulog('All Short', 'FAIL', 'FAIL')
        ERR_Buf += 1
    if ERR_Buf >= 1:
        ERR_Earth = 1
def CDT():
    cnt2 = cntdwn
    if D_OLED != 1:
        GDisplay('Test Will', 'Begin In:', '', 'Seconds')
        print ('CNT2', cnt2)
        while cnt2 != 0:
            display.lcd_display_string(str(cnt2), 3)
            cnt2 -= 1
            time.sleep(1)

    else:
        GDisplay('Test Will', 'Begin In:', '', 'Seconds')
        while cnt2 != 0:
            display2.lcd2_display_string(str(cnt2), 3)
            time.sleep(1)
            cnt2 -= 1


def Test(title):
    L1(title)
    L2(title)
    L3(title)
    Earth(title)






# EIO Buttons
GPA7.direction = digitalio.Direction.INPUT  # Green Button
GPA7.pull = digitalio.Pull.UP
GPB7.switch_to_output(value=False)

GPA6.direction = digitalio.Direction.INPUT  # Red Button
GPA6.pull = digitalio.Pull.UP
GPB6.switch_to_output(value=False)

# HVC Buzzer
GPB5.switch_to_output(value=True)

# HVC I/O
GPA0.direction = digitalio.Direction.INPUT #EIO Earth Input
GPA0.pull = digitalio.Pull.UP
GPB0.switch_to_output(value=True) # EIO Earth Output


GPA1.direction = digitalio.Direction.INPUT #EIO L1 Input
GPA1.pull = digitalio.Pull.UP
GPB1.switch_to_output(value=True) #EIO L1 Output


GPA2.direction = digitalio.Direction.INPUT #EIO L2 Input
GPA2.pull = digitalio.Pull.UP
GPB2.switch_to_output(value=True) #EIO L2 Output



GPA3.direction = digitalio.Direction.INPUT #EIO L3 Input
GPA3.pull = digitalio.Pull.UP
GPB3.switch_to_output(value=True) #EIO L3 Output

while buz != 0:
    GPB5.value = False
    time.sleep(.1)
    GPB5.value = True
    time.sleep(.1)
    buz -= 1
buz = 2



GDisplay('Bellwether Co. HVC', 'HV Continuity Test', 'Starting...', rev)
time.sleep(2)
# button = True
# while button != False:
#     button = GPA7.value


while BC_Check != 1:
    GDisplay('Enter Serial #', 'Barcode','',  str(rev))
    p.digital_write(6, 1)
    p.digital_write(7, 1)
    BC = input("Enter SN Barcode ")
    if BC == str('0000'):
        debug = 1
        timer = int(5)
        ST5 = ST5_BW
        print ('Debug Enabled via SSN')
    p.digital_write(6, 0)
    p.digital_write(7, 0)
    if prg == BC:
        GDisplay('Bellwether Co. ADO', 'Invalid Serial #','',rev)
        p.digital_write(7, 1)
        time.sleep(5)
        p.digital_write(7, 0)
        time.sleep(1)
    else:
        GDisplay('Bellwether Co. ADO', 'Press Green ', 'Button to ', 'Begin Testing')
        BC_Check += 1

        button = True
        while button != False:
            button = GPA7.value
if BC == ssn:
    print("Yes")

    f = open('/home/pi/Bellwether/ADO_ODO_HVC.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' +"'" + str(BC) + "'")
    f.write('\n')
    f.write('res ' + '= ' + str(res))
    f.write('\n')
    f.write('fail ' + '= ' + str(fail))
    f.close()
else:
    cnt = 0
    res = 0
    fail = 0
    ctest1 = 0
    ctest2 = 0
    ctest3 = 0
    ctest4 = 0
    ctest5 = 0
    f = open('/home/pi/Bellwether/ADO_HVC_LOG.py', "w")
    f.write('ctest1 = int(0)')
    f.write('\n')
    f.write('ctest2 = int(0)')
    f.write('\n')
    f.write('ctest3 = int(0)')
    f.write('\n')
    f.write('ctest4 = int(0)')
    f.write('\n')
    f.write('ctest5 = int(0)')
    f.write('\n')
    print('BC', BC)
    with open('/home/pi/Bellwether/ADO_HVC_DATA/_HVC_Test_' + BC + '.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Time','ADO','ADO_Rev', 'PN','SSN', 'Cycle Count', 'Resets', 'Note',
                              'State', 'PASS / FAIL', 'Operator'])
        Test_file.flush()

    f = open('/home/pi/Bellwether/ADO_ODO_HVC.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' + "'" + str(BC) + "'")
    f.write('\n')
    f.write('res ' + '= ' + str(res))
    f.write('\n')
    f.write('fail ' + '= ' + str(fail))
    f.close()
    print ('BC', BC)

def results1():
    f = open('/home/pi/Bellwether/ADO_HVC_LOG.py', "w")
    f.write('ctest1 = int(1)')
    f.write('\n')
    f.write('ctest2 = int(0)')
    f.write('\n')
    f.write('ctest3 = int(0)')
    f.write('\n')
    f.write('ctest4 = int(0)')
    f.write('\n')
    f.write('ctest5 = int(0)')
    f.write('\n')
    f.close()
def results2():
    f = open('/home/pi/Bellwether/ADO_HVC_LOG.py', "w")
    f.write('ctest1 = int(1)')
    f.write('\n')
    f.write('ctest2 = int(1)')
    f.write('\n')
    f.write('ctest3 = int(0)')
    f.write('\n')
    f.write('ctest4 = int(0)')
    f.write('\n')
    f.write('ctest5 = int(0)')
    f.write('\n')
    f.close()
def results3():
    f = open('/home/pi/Bellwether/ADO_HVC_LOG.py', "w")
    f.write('ctest1 = int(1)')
    f.write('\n')
    f.write('ctest2 = int(1)')
    f.write('\n')
    f.write('ctest3 = int(1)')
    f.write('\n')
    f.write('ctest4 = int(0)')
    f.write('\n')
    f.write('ctest5 = int(0)')
    f.write('\n')
    f.close()
def results4():
    f = open('/home/pi/Bellwether/ADO_HVC_LOG.py', "w")
    f.write('ctest1 = int(1)')
    f.write('\n')
    f.write('ctest2 = int(1)')
    f.write('\n')
    f.write('ctest3 = int(1)')
    f.write('\n')
    f.write('ctest4 = int(1)')
    f.write('\n')
    f.write('ctest5 = int(0)')
    f.write('\n')
    f.close()
def results5():
    f = open('/home/pi/Bellwether/ADO_HVC_LOG.py', "w")
    f.write('ctest1 = int(1)')
    f.write('\n')
    f.write('ctest2 = int(1)')
    f.write('\n')
    f.write('ctest3 = int(1)')
    f.write('\n')
    f.write('ctest4 = int(1)')
    f.write('\n')
    f.write('ctest5 = int(1)')
    f.write('\n')
    f.close()
def test_body(title,):

    global button
    global button2
    global ERR_Buf2
    global ERR_Buf
    global res
    global ERR_L1
    global ERR_L2
    global ERR_L3
    global ERR_Earth
    button = False
    button2 = False
    ERR_Buf = 1


    GDisplay('Press Green Button', 'To Begin Test', '', title)
    button = True
    while button != False:
        button = GPA7.value



    while ERR_Buf != 0:
        CDT()
        ERR_Buf = 1
        ERR_Buf2 = 0
        Test(title)
        if ERR_L1 or ERR_L2 or ERR_L3 or ERR_Earth == True:
            ERR_Buf2 = 1
            ERR_L1 = 0
            ERR_L2 = 0
            ERR_L3 = 0
            ERR_Earth = 0
        D_Results()
        button = True
        while button != False:
            button = GPA7.value
        button = True
        button2 = 0
        # Pass
        if ERR_Buf2 == 0:
            button = True
            button2 = True

            GDisplay(title,
                     'Test PASS',
                     '"Green" Continue',
                     '"Red" Exit')
            # GDisplay(title, 'Complete', 'Press Green Button', '')
            # GScroll('Press Green Button to Continue and Save',3)
            # GScroll('Press Red Button to End HVC Test', 4)

            while button != False:
                button = GPA7.value
                button2 = GPA6.value
                if button2 != True:
                    res += 1
                    f = open('/home/pi/Bellwether/ADO_ODO_HVC.py', "w")
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
                    GDisplay('', '', '', '')
                    os.execl(sys.executable, 'python3',
                             '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        # FAIL
        elif ERR_Buf2 >= 1:
            button = True
            button2 = True
            GDisplay(title, 'Failed', '', '')
            GScroll('Press Green Button to Re - Test (Green)   ',3)
            GScroll('Press Red Button to Exit Test (Red)     ', 4)
            ERR_Buf = 1
            ERR_Buf2 = 0
            res += 1
            while button != False:
                button = GPA7.value
                button2 = GPA6.value
                ERR_Buf2 = 0
                if button2 == False:
                    f = open('/home/pi/Bellwether/ADO_ODO_HVC.py', "w")
                    res += 1
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
                    GDisplay('', '', '', '')
                    os.execl(sys.executable, 'python3',
                             '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])


while ST5 != 0:
    if ctest1 !=1:
        test_body('AC MAINS Test')
        print('AC MAINS Test')
        f = open('/home/pi/Bellwether/ADO_HVC_LOG.py', "w")
        f.write('ctest1 = int(1)')
        f.write('\n')
        f.write('ctest2 = int(0)')
        f.write('\n')
        f.write('ctest3 = int(0)')
        f.write('\n')
        f.write('ctest4 = int(0)')
        f.write('\n')
        f.write('ctest5 = int(0)')
        f.write('\n')
        f.close()

    if ctest2 != 1:
        test_body('Heater CT1 Test')
        print('Heater CT1 Test')
        f = open('/home/pi/Bellwether/ADO_HVC_LOG.py', "w")
        f.write('ctest1 = int(1)')
        f.write('\n')
        f.write('ctest2 = int(1)')
        f.write('\n')
        f.write('ctest3 = int(0)')
        f.write('\n')
        f.write('ctest4 = int(0)')
        f.write('\n')
        f.write('ctest5 = int(0)')
        f.write('\n')
        f.close()
    if ctest3 != 1:
        test_body('AUX Heater F4 Test')
        print('AUX Heater F4 Test')
        f = open('/home/pi/Bellwether/ADO_HVC_LOG.py', "w")
        f.write('ctest1 = int(1)')
        f.write('\n')
        f.write('ctest2 = int(1)')
        f.write('\n')
        f.write('ctest3 = int(1)')
        f.write('\n')
        f.write('ctest4 = int(0)')
        f.write('\n')
        f.write('ctest5 = int(0)')
        f.write('\n')
        f.close()

    if ctest4 != 1:
        test_body('AUX CT2 Test')
        print('AUX CT2 Test')
        f = open('/home/pi/Bellwether/ADO_HVC_LOG.py', "w")
        f.write('ctest1 = int(1)')
        f.write('\n')
        f.write('ctest2 = int(1)')
        f.write('\n')
        f.write('ctest3 = int(1)')
        f.write('\n')
        f.write('ctest4 = int(1)')
        f.write('\n')
        f.write('ctest5 = int(0)')
        f.write('\n')
        f.close()

    if ctest5 != 1:
        test_body('SW Output Test')
        print('SW Output Test')
        f = open('/home/pi/Bellwether/ADO_HVC_LOG.py', "w")
        f.write('ctest1 = int(1)')
        f.write('\n')
        f.write('ctest2 = int(1)')
        f.write('\n')
        f.write('ctest3 = int(1)')
        f.write('\n')
        f.write('ctest4 = int(1)')
        f.write('\n')
        f.write('ctest5 = int(1)')
        f.write('\n')
        f.close()
    ST5 -= 1
print ('END')

    # ST5 -=1
GDisplay('','','','')

mlog('ADO_MASTER_LIST_DATA', 'HVC', 'N/A' ,'PASS', 'PASS')
ulog('N/A', 'PASS', 'PASS')


f = open('/home/pi/Bellwether/ADO_HVC_LOG.py', "w")
f.write('ctest1 = int(0)')
f.write('\n')
f.write('ctest2 = int(0)')
f.write('\n')
f.write('ctest3 = int(0)')
f.write('\n')
f.write('ctest4 = int(0)')
f.write('\n')
f.write('ctest5 = int(0)')
f.write('\n')
f.close()
print ('BC', BC)

GDisplay('HVC Testing ',
         'Complete',
         'Rebooting.....',
         '')

f = open('/home/pi/Bellwether/ADO_D_OLED.py', "w")
f.write('D_OLED = int (0)')
f.write('\n')
f.close()
f = open('/home/pi/Bellwether/ADO_E_IO.py', "w")
f.write('E_IO = int (0)')
f.write('\n')
f.close()
E_IO = 1
print('Expanded IO ADO')
time.sleep(2)
GDisplay('', '', '', '')
os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py',
         *sys.argv[1:])