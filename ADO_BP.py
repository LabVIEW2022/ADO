#!/usr/bin/env python
import ADO_V
import time
import datetime
import csv
import lcddriver
import os
import sys
from ADO_Rev import rev
rev2 = rev [7:]
from ADO_Rev import ST7
from ADO_Rev import ST7_BW
from ADO_PN_Buf import prg
from ADO_Rev import debug
from ADO_Rev import db
from ADO_Rev import TSN
from ADO_D_OLED import D_OLED
from ADO_Unit import ado_
from ADO_Step import ado_step
from ADO import ado

if debug == 1:
    ssn = str('Test')
else:
    from ADO_ODO_BP import ssn
from ADO_ODO_BP import cnt
from ADO_ODO_BP import fail
from ADO_ODO_BP import res


fail3 = int(0)
BC_Check = int(0)
run = str('A')
comp_run = int(2300)
enc_comp = int(100)


open_ = open('/home/pi/Bellwether/ADO_Tag.py', 'rt')
tag = open_.read()
open_.close()

if ado_ == ('ADO5'):
    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
if ado_ == '':
    ado_ = str('NO_NAME')
    print('NO_NAME')
print (ado_)

device = str('BP')
sub = device
BC = str('0000') # todo needs to be changed
latch = int(0)
button = int(0)


buf = datetime.datetime.now()
stime = time.time()
tick = int(0)
ticka = int(0)
tickb = int(0)
con = float(1.58730158) #.788A
path = str('ADO_BP_DATA')
pos_ = int(2300)
pfe = int(100) #Position Following Error todo change back to 100 afte debug

def log(path, sub, ab, enc, delta, state, result):
    now = datetime.datetime.now()
    ddate = (now.strftime("%m-%d-%Y"))
    ttime = (now.strftime("%H:%M:%S"))
    rev2 = rev[7:]
    with open('/home/pi/Bellwether/' + path + '/' + '_' + sub + '_Test_' + BC + '.csv', mode='a') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([ddate, ttime, ado_, rev2, prg, BC, cnt, res, ab, enc, delta, state, result, tag])
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
        Test_writer.writerow([buf, ado_, device, BC, cnt, res, note, state, result, tag, rev2, etime, tag])

        Test_file.flush()
    if db == 1:
        ado.GDisplay_CLR()
        ado.GDisplay('Bellwether Co. ADO', 'Upload to DB          ',
                     '', str(rev),)
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
def Home():
    global enc
    ado.GDisplay('Bellwether Co. ADO', 'Powering ', 'ADO ByPass', str(rev))
    ado.V24Off()
    time.sleep(5)
    ado.V24A()
    time.sleep(5)
    ado.GDisplay('Bellwether Co. ADO', 'Homing ', 'ADO ByPass', str(rev))
    ado_step.home()
    time.sleep(5)
    from ADO_Decoder import Encoder
    enc = Encoder(18, 17)
    enc.zero()
def move(pos):
    global con
    global tic
    global enc
    global pfe
    global cnt
    global fail
    global res
    global run
    button = 0
    time.sleep(2)
    ado_step.goto(pos)
    time.sleep(5)
    tic = enc.read() * con
    tic = int(tic)
    comp[str(run) + str(pos)] = int(tic) #Comparison Data
    duh = (str(run) + str(pos))
    if pos >= tic:
        delta = pos - tic
    else:
        delta = tic - pos
    tich = pos + pfe
    ticl = pos - pfe
    if tic >= tich:
        ado.GDisplay('Bellwether Co. ADO', 'Pos Following Error', 'Press Reset', str(rev))
        print('Fail ' + str(pos) + ' ' + str(tic))
        print('Position Following Error')
        cnt += 1
        fail += 1
        res += 1
        ODO_Publish()
        print('cnt', cnt)
        print('fail', fail)
        print('res', res)

        log('ADO_BP_DATA', device, str(pos), str(tic), str(delta), 'Position Following Error', 'Fail')
        ulog('N/A', 'Position Following Error', 'FAIL')
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
        pass
    if tic <= ticl:
        ado.GDisplay('Bellwether Co. ADO', 'Pos Following Error', 'Press Reset', str(rev))
        print('Fail ' + str(pos) + ' ' + str(tic))
        print('Position Following Error')
        cnt += 1
        fail += 1
        res += 1
        ODO_Publish()
        print('cnt', cnt)
        print('fail', fail)
        print('res', res)
        log('ADO_BP_DATA', device, str(pos), str(tic), str(delta), 'Position Following Error', 'Fail')
        ulog('N/A', 'Position Following Error', 'FAIL')
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
        log('ADO_BP_DATA', device, str(pos), str(tic), str(delta), 'PASS', 'PASS')
    line = str('TIC ' + str(pos) + ' ENC ' + str(tic))
    ado.GDisplay('Bellwether Co. ADO', 'Moving to Position', str(line), str(rev))
    go = ado_step.pos()
    print(str(go) + ' ' + str(tic))

def ODO_Reset():
    f = open('/home/pi/Bellwether/ADO_ODO_' + sub +'.py', "w")
    f.write('cnt = 1')
    f.write('\n')
    f.write('ssn ' + '= ' + "'" + str(BC) + "'")
    f.write('\n')
    f.write('res = 0')
    f.write('\n')
    f.write('fail = 0')
    f.close()
def ODO_Publish():
    f = open('/home/pi/Bellwether/ADO_ODO_' + sub + '.py', "w")
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


ado.GDisplay('Bellwether Co. ADO', '', 'ADO ByPass', str(rev))


'''''''''''''''''''''''''''''''''''''''
Serial ID
'''''''''''''''''''''''''''''''''''''''


while BC_Check != 1:
    ado.GDisplay('Enter Serial #', 'Barcode', '', str(rev))
    ado.B_Yellow()
    if debug == 1:
        BC = str(TSN)
    else:
        BC = input("Enter SN Barcode ")

    if BC == str('0000'):
        BC == str('debug')
        debug = 1
        ST7 = ST7_BW
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

'''''''''''''''''''''''''''''''''''''''
CSV Header
'''''''''''''''''''''''''''''''''''''''

if BC == ssn:
    print('Yes')
    fail2 = fail
else:
    print('No')
    with open('/home/pi/Bellwether/' + path + '/' + '_' + sub + '_Test_' + BC + '.csv', mode='w') as Test_file:
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Time', 'Date', 'ADO', 'ADO_Rev', 'PN', 'SSN', 'Cycle Count', 'Resets', 'Absolute',
                              'Encoder', 'Delta', 'State', 'PASS / FAIL', 'Operator'])

    cnt = 1
    ssn = str(BC)
    res = 0
    fail = 0
    hall = 1
    ODO_Reset()
    fail2 = fail


'''''''''''''''''''''''''''''''''''''''
Start Test
'''''''''''''''''''''''''''''''''''''''
ado.GDisplay('Bellwether Co. ADO', 'Press Button', 'To Start', str(rev))

if debug == 1:
    button = 1
while button == 0:
    ado.B_Green()
    time.sleep(.5)
    ado.B_Off()
    time.sleep(.5)
    button = ado.BTN()
button = 0

Home()
comp = {}
while ST7 != 0:
    while pos_ != 0:
        move(pos_)
        pos_ -= 100
    pos_ = 2300
    move(2300)
    ST7 -= 1
    run = ('B')

with open('/home/pi/Bellwether/' + path + '/' + '_' + sub + '_Test_' + BC + '.csv', mode='a') as Test_file:  # Rpi
    Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    Test_writer.writerow([])
    Test_file.flush()
with open('/home/pi/Bellwether/' + path + '/' + '_' + sub + '_Test_' + BC + '.csv', mode='a') as Test_file:  # Rpi
    Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    Test_writer.writerow(['Position', 'SMPL_A', 'SMPL_B', 'Delta', 'ERROR', 'ENC Error CNT','', 'Error >= Delta (' +
                          str(enc_comp) + ')'])
    Test_file.flush()

while comp_run != 0:
    test_ = comp[str('A' + str(comp_run))]
    test2_ = comp[str('B' + str(comp_run))]
    if test_ >= test2_:
        test3_ = test_ - test2_
    else:
        test3_ = test2_ - test_
    if test3_ >= enc_comp:
        fail2 += 1
        fail3 += 1


    with open('/home/pi/Bellwether/' + path + '/' + '_' + sub + '_Test_' + BC + '.csv', mode='a') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([str(comp_run), str(test_), str(test2_), str(test3_), str(fail3), str(fail2)])
        Test_file.flush()

    comp_run -= 100
    fail3 = 0



if fail2 > fail:
    fail += 1
    f = open('/home/pi/Bellwether/ADO_ODO_' + sub + '.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' + "'" + str(BC) + "'")
    f.write('\n')
    f.write('res ' + '= ' + str(res))
    f.write('\n')
    f.write('fail ' + '= ' + str(fail))
    f.write('\n')
    f.write('hall ' + '= ' + str(1))
    f.close()
    ado.GDisplay('Bellwether Co. ADO', 'Enc Comp Error', 'Press Reset', str(rev))
    print('ENC Comp Error')
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



mlog('ADO_MASTER_LIST_DATA', str(device), 'N/A', 'PASS', 'PASS')
ODO_Reset()
ado.GDisplay('Bellwether Co. ADO', '"Pass" Test Complete', '', str(rev))
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

