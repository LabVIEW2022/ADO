#!/usr/bin/env python
import time
import os
# os.system('sudo nohup python3 /home/pi/Bellwether/ADO_Reset.py &') # Removed due to common mode rejection issues.
import sys
import lcddriver2
from ADO_Unit import ado_
from ADO import ado
button = int(0)
print('BW UI Start')
IC = str('')

time.sleep(.2)

if ado_ == ('ADO5'):
    print ('ADO Unit ', ado_)
else:
    print ('ADO Unit ', ado_)
    time.sleep(.2)
    ado.ISO_(0) # Ensures Iso is off
    time.sleep(1)
    ado.CDA_(0)



#PN List
from ADO_PN import BC_Drum_Assembly
from ADO_PN import BC_Drum_Assembly_BW
from ADO_PN import BC_Drop
from ADO_PN import BC_Drop_BW
from ADO_PN import BC_PNU_Drop
from ADO_PN import BC_PNU_Drop_BW
from ADO_PN import BC_Exit
from ADO_PN import BC_Exit_BW
from ADO_PN import BC_Exhaust
from ADO_PN import BC_Exhaust_BW
from ADO_PN import BC_Panel
from ADO_PN import BC_Panel_BW
from ADO_PN import BC_SLT
from ADO_PN import BC_SLT_BW
from ADO_PN import BC_ST_BW
from ADO_PN import BC_BP
from ADO_PN import BC_BP_BW
from ADO_ID import id





from ADO_Unit import ado_
from ADO_Rev import rev
from ADO_Rev import IC1
from ADO_Rev import IC2
from ADO_Rev import IC2_2
from ADO_Rev import IC3
from ADO_Rev import IC4
from ADO_Rev import IC5
from ADO_Rev import IC6
from ADO_Rev import IC7
from ADO_D_OLED import D_OLED
from ADO_E_IO import E_IO
from ADO_EIO_Detect import E_IO_D

D_OLED = 0
bit = 0

if D_OLED == 1:
    display2 = lcddriver2.lcd2()

def load():
    button = 0
    print('Load')
    ado.GDisplay(''
                 , 'Scan Interface cable          '
                 , "'Load'"
                 , str(rev))
    IC = input('Scan Interface Cable')
    ado.GDisplay_Cnt(str(IC))
    if IC == IC1:
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_Load.py', *sys.argv[1:])
    else:
        ado.GDisplay("Bellwether Co. ADO"
                     , 'Wrong Cable          '
                     , 'Press Reset'
                     , str(rev))
        while button == 0:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        ado.B_Off()
        ado.GDisplay_CLR()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
def drop():
    button = 0
    print("Drop")
    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_PNU_Drop.py', *sys.argv[1:])
def drop_pnu(): # for 1.3.1
    button = 0
    print("Drop PNU")
    ado.GDisplay(''
                 , 'Barcode'
                 , 'Press Reset'
                 , str(rev))
    time.sleep()
    IC = IC2_2
    ado.GDisplay_Cnt(str(IC))
    if IC == IC2_2:
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_PNU_Drop.py', *sys.argv[1:])
    else:
        ado.GDisplay("Bellwether Co. ADO"
                     , 'Wrong Cable          '
                     , 'Press Reset'
                     , str(rev))
        while button == 0:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        ado.B_Off()
        ado.GDisplay_CLR()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
def exit():
    button = 0
    print("Exit")
    ado.GDisplay('Scan Interface cable',
                 '"Exit"',
                 'Barcode',
                 str(rev))
    IC = input('Scan Interface Cable')
    ado.GDisplay_CLR()
    ado.GDisplay_Cnt(str(IC))
    if IC == IC3:
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_Exit.py', *sys.argv[1:])
    else:
        ado.GDisplay("Bellwether Co. ADO"
                     , 'Wrong Cable          '
                     , 'Press Reset'
                     , str(rev))
        while button == 0:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        ado.B_Off()
        button = 0
        display.lcd_clear()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
def exhaust():
    button = 0
    print("Exhaust PWM")
    ado.GDisplay('Scan Interface cable',
                 '"Exhaust 1"',
                 'Barcode',
                 str(rev))
    IC = input('Scan Interface Cable 1')
    ado.GDisplay_CLR()
    ado.GDisplay_Cnt(str(IC))
    if IC == IC4:
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_Exhaust.py', *sys.argv[1:])
    else:
        ado.GDisplay("Bellwether Co. ADO"
                     , 'Wrong Cable          '
                     , 'Press Reset'
                     , str(rev))
        while button == 0:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        ado.B_Off()
        button = 0
        ado.GDisplay_CLR()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
def EIO():
    button = 0
    print("HVC")
    ado.GDisplay('Scan EIO Module',
                 '"HVC"',
                 'Barcode',
                 str(rev))
    IC = input('Scan EIO Module ')
    ado.GDisplay_CLR()
    ado.GDisplay_Cnt(str(IC))
    if ado_ == ('ADO5'):
        if IC == IC5:
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_HVC.py', *sys.argv[1:])
        else:
            ado.GDisplay("Bellwether Co. ADO"
                         , 'Wrong Cable          '
                         , 'Press Reset'
                         , str(rev))
            while button == 0:
                ado.B_Red()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
            ado.B_Off()
            button = 0
            ado.GDisplay_CLR()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])

    else:
        if IC == IC5:
            if E_IO != 1:
                ado.GDisplay('EIO Module not',
                         'Detected',
                         'Please wait....',
                         '')
                time.sleep(2)
                f = open('/home/pi/Bellwether/ADO_EIO_Detect.py', "w")
                f.write('E_IO_D = int(1)')
                f.close()
                f = open('/home/pi/Bellwether/ADO_HW_Bootcheck.py', "w")
                f.write('HW_C = int(1)')
                f.close()
                os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_NET.py', *sys.argv[1:])

            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_HVC.py', *sys.argv[1:])
        else:
            ado.GDisplay("Bellwether Co. ADO"
                         , 'Wrong Cable          '
                         , 'Press Reset'
                         , str(rev))
            while button == 0:
                ado.B_Red()
                time.sleep(.5)
                ado.B_Off()
                time.sleep(.5)
                button = ado.BTN()
            ado.B_Off()
            button = 0
            ado.GDisplay_CLR()
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
def SLT():
    button = 0
    print("SLT")
    ado.GDisplay('Scan SLT Module',
                 'Barcode',
                 '',
                 str(rev))
    IC = input('Scan SLT Module ')
    ado.GDisplay_CLR()
    ado.GDisplay_Cnt(str(IC))
    if IC == IC6:
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_SLT.py', *sys.argv[1:])
    else:
        ado.GDisplay("Bellwether Co. ADO"
                     , 'Wrong Cable          '
                     , 'Press Reset'
                     , str(rev))
        while button == 0:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        ado.B_Off()
        button = 0
        display.lcd_clear()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
def ST_Flash():
    os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_ST_Flash.py', *sys.argv[1:])
def BP():
    button = 0
    print("BP")
    ado.GDisplay('Scan Bypass Driver',
                 'Barcode',
                 '',
                 str(rev))
    IC = input('Scan Stepper Driver ')
    ado.GDisplay_CLR()
    ado.GDisplay_Cnt(str(IC))
    if IC == IC7:
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_BP.py', *sys.argv[1:])
    else:
        ado.GDisplay('Bellwether Co. ADO',
                     'Wrong Device',
                     str(rev))
        while button == 0:
            ado.B_Red()
            time.sleep(.5)
            ado.B_Off()
            time.sleep(.5)
            button = ado.BTN()
        ado.B_Off()
        button = 0
        ado.GDisplay_CLR()
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
# def GDisplay(Line1,Line2,Line3,Line4):
#     if D_OLED == 1:
#         display.lcd_clear()
#         display.lcd_display_string('See EIO Display', 1)
#         display2.lcd2_clear()
#         display2.lcd2_clear()
#         display2.lcd2_display_string(Line1, 1)
#         display2.lcd2_display_string(Line2, 2)
#         display2.lcd2_display_string(Line3, 3)
#         display2.lcd2_display_string(Line4, 4)
#     else:
#         display.lcd_clear()
#         display.lcd_clear()
#         display.lcd_display_string(Line1, 1)
#         display.lcd_display_string(Line2, 2)
#         display.lcd_display_string(Line3, 3)
#         display.lcd_display_string(Line4, 4)
# def GScroll(text='', num_line=1, num_cols=20):
#     if D_OLED == 1:
#         if (len(text) > num_cols):
#             display2.lcd2_display_string(text[:num_cols], num_line)
#             time.sleep(1)
#             for i in range(len(text) - num_cols + 1):
#                 text_to_print = text[i:i + num_cols]
#                 display2.lcd2_display_string(text_to_print, num_line)
#                 time.sleep(0.1)
#             time.sleep(1)
#         else:
#             display2.lcd2_display_string(text, num_line)
#     else:
#         if (len(text) > num_cols):
#             display.lcd_display_string(text[:num_cols], num_line)
#             time.sleep(1)
#             for i in range(len(text) - num_cols + 1):
#                 text_to_print = text[i:i + num_cols]
#                 display.lcd_display_string(text_to_print, num_line)
#                 time.sleep(0.2)
#             time.sleep(1)
#         else:
#             display.lcd_display_string(text, num_line)

def ADO5():
    if ado_ == ('ADO5'):
        ado.GDisplay('Incompatible HW', 'Restarting', '', str(rev))
        time.sleep(2)
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])



if ado_ == ('ADO5'):
    print('')
else:
    ado.CDA_(1)
time.sleep(1)
if ado_ == ('ADO5'):
    print ('')
else:
    ado.CDA_(0)
prg = str("")
prg_ = str("")
prgL = int()


if E_IO_D == 1:
    f = open('/home/pi/Bellwether/ADO_EIO_Detect.py', "w")
    f.write('E_IO_D = int(0)')
    f.close()
    EIO()

while True:
    while bit != 1:
        ado.B_Green()
        ado.GDisplay('Bellwether Co. ADO', 'Scan User ID', 'To Continue.', str(rev))
        user = input('Scan ID Card ')
        tag = id.scan(user)
        if tag != ('Invalid'):
            f = open('/home/pi/Bellwether/ADO_Tag.py', "w")
            print('Here ', tag)
            f.write(str(tag))
            f.close()
            bit += 1
        else:
            pass

    ado.B_Yellow()
    ado.GDisplay('Bellwether Co. ADO', 'Scan PN', 'Barcode', str(rev))
    os.system('clear') #todo Testing 'Clear Screen'
    test = input('Enter PN Barcode ')
    prg = test
    prgL = len(prg)
    if prgL == 9:
        prg_ = prg
    elif prgL >= 5:
        prg_ = prg [:-4]
        print(prg_)
        f = open('/home/pi/Bellwether/ADO_PN_Buf.py', "w")
        f.write('prg ' + '= ' + 'str' + '(' + "'" + str(prg) + "'" + ')')
        f.write('\n')
        f.write('prg_ ' + '= ' + 'str' + '(' + "'" + str(prg) + "'" + ')')
        f.write('\n')
        f.close()
    elif prgL <= 5:
        prg_ = prg

    ado.GDisplay_CLR()
    ado.GDisplay_Cnt(str(prg))
    ado.B_Off()
    if prg_ == BC_Drum_Assembly:
        ADO5()
        load()
    if prg_ == BC_Drum_Assembly_BW:
        ADO5()
        load()
    if prg_ == BC_Drop:
        ADO5()
        drop()
    if prg_ == BC_PNU_Drop_BW:
        ADO5()
        drop()
    if prg_ == BC_PNU_Drop:
        ADO5()
        drop_pnu()
    if prg_ == BC_PNU_Drop_BW:
        ADO5()
        drop_pnu()
    if prg_ == BC_Exit:
        ADO5()
        exit()
    if prg_ == BC_Exit_BW:
        ADO5()
        exit()
    if prg_ == BC_Exhaust:
        ADO5()
        exhaust()
    if prg_ == BC_Exhaust_BW:
        ADO5()
        exhaust()
    if prg_ == BC_Panel:
        EIO()
    if prg_ == BC_Panel_BW:
        EIO()
    if prg_ == BC_SLT:
        ADO5()
        SLT()
    if prg_ == BC_SLT_BW:
        ADO5()
        SLT()
    if prg_ == BC_BP:
        ADO5()
        BP()
    if prg_ == BC_BP_BW:
        ADO5()
        BP()
    if prg_ == BC_ST_BW:
        ST_Flash()
    if prg == '5126':
        os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_BC.py', *sys.argv[1:])
    else:
        ado.B_Red()
        ado.GDisplay('Bellwether Co. ADO',
                     'Invalid PN',
                     '',
                     str(rev))
        time.sleep(5)
        ado.B_Off()




