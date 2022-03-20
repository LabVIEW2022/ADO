import os
import lcddriver
import lcddriver2
import time
import sys
import pifacedigitalio as p
import glob
import datetime
import csv
from ADO_Unit import ado_
prg = str('ST_Flash')

#init io board
if ado_ == ('ADO5'):
    import digitalio
    import busio
    import board
    from adafruit_mcp230xx.mcp23017 import MCP23017
    i2c = busio.I2C(board.SCL, board.SDA)
    EIOi = MCP23017(i2c, address=0x22)  # MCP23017
    GPAi6 = EIOi.get_pin(6)  # GPAi6 # Red Button ADO5
    GPAi7 = EIOi.get_pin(7)  # GPAi7 # Green Button ADO5
    GPAi6.direction = digitalio.Direction.INPUT
    GPAi6.pull = digitalio.Pull.UP
    GPAi7.direction = digitalio.Direction.INPUT
    GPAi7.pull = digitalio.Pull.UP

    GPBi6 = EIOi.get_pin(14)  # GPBi6
    GPBi7 = EIOi.get_pin(15)  # GPBi7
    GPBi6.switch_to_output(value=False)
    GPBi7.switch_to_output(value=False)

BC_Check = int(0)
p.init()
from ADO_D_OLED import D_OLED
from ADO_ODO_ST import cnt
from ADO_Rev import rev
rev2 = rev [7:]
from ADO_Unit import ado_
button = int(0)
bt_time = int(1.5)
filename = str('')
def get_filepaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths
def listToString(s):
    str1 = ""
    for ele in s:
        str1 += ele
    return str1
full_file_paths = get_filepaths("/home/pi/ST_FW")
ST_FW = (listToString(full_file_paths))
ST_FW = (ST_FW.replace('/home/pi/ST_FW/', ''))
BC_Check = int(0)
SSN_Check = int(0)
res = int(0)
note = str('ST_Flash')
state = ST_FW
result = str('PASS')
sub = str('ST')



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

FW = str('sudo cp /home/pi/ST_FW/' + ST_FW + ' /home/pi/ST')
display = lcddriver.lcd()

if D_OLED == 1:
    display2 = lcddriver2.lcd2()



while BC_Check != 1:
    p.digital_write(6, 1)
    p.digital_write(7, 1)
    while SSN_Check != 1:
        GDisplay('Enter Serial #', 'Barcode', '', str(rev))
        BC = input("Enter SN Barcode ")
        # BC= str('556555')
        if len(BC) != 5:
            GDisplay('Bellwether Co. ADO', 'Invalid Serial', 'Number', 'Scan Again')
            time.sleep(5)
        else:
            GDisplay('Bellwether Co. ADO', 'Valid Serial', 'Number', '')
            SSN_Check = int(1)
            time.sleep(2)
        # BC = str('5555')
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


p.digital_write(6, 0)
p.digital_write(7, 0)

if ado_ == ('ADO5'): # ADO5 Operation
    while GPAi7.value == True:
        GDisplay('Flash ST?', 'If "Yes" press', 'Green Button', '')
        GScroll(str(ST_FW), 4)
        time.sleep(bt_time)
        p.digital_write(6, 0)
        print(ST_FW)
        if GPAi7.value == False:
            p.digital_write(6, 1)
            p.digital_write(7, 1)
            GDisplay('Flashing', 'Please Wait.....', '', '')
            GScroll(str(ST_FW), 4)
            os.system('sudo mount /dev/sda /home/pi/ST')
            os.system(FW)
            os.system('sudo umount /dev/sda')
            p.digital_write(7, 0)
            cnt += 1
            f = open('/home/pi/Bellwether/ADO_ODO_ST.py', "w")
            f.write('cnt = int(' + str(cnt) + ')')
            f.close()
            GDisplay('Flash Complete', 'Returning To', 'ADO Main', '')
            buf = datetime.datetime.now()
            date_ = buf.date()
            time_ = buf.time()
            with open('/home/pi/Bellwether/ADO_MASTER_LIST_DATA/ST_Master_List.csv',
                      mode='a') as Test_file:  # Rpi
                Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                Test_writer.writerow([buf, ado_, rev2, prg, BC, '1', res, note, state, result])
                Test_file.flush()
                f = open('/home/pi/Bellwether/ADO_ODO_' + sub + '.py', "w")
                f.write('cnt ' + '= ' + str(cnt))
                f.write('\n')
                f.close()

            time.sleep(2)
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        else:
            GDisplay('Flash ST?', 'If "No" press', 'Red Button', '')
            GScroll(str(ST_FW), 4)
            time.sleep(bt_time)
            p.digital_write(7, 0)
            if GPAi6.value == False:
                GDisplay('Canceled', 'Returning To', 'ADO Main', '')
                time.sleep(2)
                os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])


else: # Standard ADO operation
    while p.digital_read(7) == 0:
        p.digital_write(6, 1)
        GDisplay('Flash ST?', 'If "Yes" press', 'Green Button', '')
        GScroll(str(ST_FW), 4)
        time.sleep(bt_time)
        p.digital_write(6, 0)
        print(ST_FW)
        if p.digital_read(7) == 1:
            p.digital_write(6, 1)
            p.digital_write(7, 1)
            GDisplay('Flashing', 'Please Wait.....', '', '')

            os.system('sudo mount /dev/sda /home/pi/ST')
            os.system(FW)
            os.system('sudo umount /dev/sda')
            p.digital_write(7, 0)
            # time.sleep(5)
            cnt += 1
            f = open('/home/pi/Bellwether/ADO_ODO_ST.py', "w")
            f.write('cnt = int(' + str(cnt) + ')')
            f.close()
            GDisplay('Flash Complete', 'Returning To', 'ADO Main', '')
            buf = datetime.datetime.now()
            date_ = buf.date()
            time_ = buf.time()
            with open('/home/pi/Bellwether/ADO_MASTER_LIST_DATA/ST_Master_List.csv',
                      mode='a') as Test_file:  # Rpi
                Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                # Test_writer.writerow(['ADO', 'Date', 'Time', 'SSN', 'ADO_Rev'])
                Test_writer.writerow([buf, ado_, rev2, prg, BC, '1', res, note, state, result])
                # Test_writer.writerow([ado_, date_, time, ssn, ado_, res, note, state, result])
                Test_file.flush()
                f = open('/home/pi/Bellwether/ADO_ODO_' + sub + '.py', "w")
                f.write('cnt ' + '= ' + str(cnt))
                f.write('\n')
                f.close()

            time.sleep(2)
            os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])
        else:
            p.digital_write(7, 1)
            GDisplay('Flash ST?', 'If "No" press', 'Red Button', '')
            GScroll(str(ST_FW), 4)
            time.sleep(bt_time)
            p.digital_write(7, 0)
            if p.digital_read(7) == 1:
                GDisplay('Canceled', 'Returning To', 'ADO Main', '')
                time.sleep(2)
                os.execl(sys.executable, 'python3', '/home/pi/Bellwether/ADO_UI.py', *sys.argv[1:])







