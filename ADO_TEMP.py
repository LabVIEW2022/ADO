import time
import datetime
import csv
import lcddriver
display = lcddriver.lcd()
from ADO_Unit import ado_
from ds18b20 import DS18B20
from ADO_ODO_Temp import cnt
from ADO_ODO_Temp import fail
from ADO_ODO_Temp import res
from ADO_EIOi import GPBi0
from ADO_Rev import rev
rev2 = rev [7:]
sensor = DS18B20()
sample_rate = int(2.5)
loop = int(0)
low = int(100)
high = int(0)
BC = str('')
prg = str('Bucket Temp')
note = str('')
state = str('')
setpoint = int(100)  # Setpoint for temp default 100
BC_Set = int(0)
buf = datetime.datetime.now()
stime = time.time()
device = str('TEMP')
db = int(0)
def GDisplay(Line1,Line2,Line3,Line4):
    display.lcd_clear()
    display.lcd_display_string(Line1, 1)
    display.lcd_display_string(Line2, 2)
    display.lcd_display_string(Line3, 3)
    display.lcd_display_string(Line4, 4)
def log(path, sub, note, state, result):
    buf = datetime.datetime.now()
    rev2 = rev[7:]
    with open('/home/pi/Bellwether/' + path + '/' + '_' + sub + '_Test_' + BC + '.csv', mode='a') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([buf, ado_, rev2, prg, BC, cnt, res, low, high, result])
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
        f.close()


def ulog(note, state, result):
    rev2 = rev [7:]
    global etime
    # global note
    import time
    end = time.time()
    hours, rem = divmod(end - stime, 3600)
    minutes, seconds = divmod(rem, 60)
    etime = ("{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
    with open('/home/pi/Bellwether/' + str(ado_) + '_' + 'Useage_Log.csv', mode='a') as Test_file: # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([buf, ado_, device, BC, cnt, res, note, state, result, str(rev2), etime])
        Test_file.flush()
    if db == 1:
        GDisplay('','','','')
        display.lcd_display_string("Bellwether Co. ADO", 1)
        display.lcd_display_string('Upload to DB          ', 2)
        display.lcd_display_string(str(rev), 4)
        file_name = (str(ado_) + '_' + 'Useage_Log.csv')
        dropbox_path = '/ADO_Log/'
        dbx = dropbox.Dropbox('TYQkL_IX4lAAAAAAAAABrz9rDoR4S3zXJgLYqiREuqOAVmUK4vvAiEUWVY9LII22')
        with open(file_name, 'r+') as f:
            dbx.files_upload(f.read(), dropbox_path + file_name, mode=dropbox.files.WriteMode.overwrite, mute=True)
def mlog (path, sub, note,state, result):
    # global note
    note = str('N/A')
    buf = datetime.datetime.now()
    with open('/home/pi/Bellwether/' + path + '/' + sub + '_Master_List.csv', mode='a') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([buf, ado_, rev2, prg, BC, cnt, res, note, state, result])
        Test_file.flush()



while BC_Set != 1:
    GDisplay('Bellwether Co. ADO', 'Scan Serial #', 'Barcode', str(rev))
    BC = input('Input Serial Number ')
    if len(BC) >= 6:
        GDisplay('Bellwether Co. ADO', 'Invalid Serial', 'Number', 'Scan Again')
        time.sleep(5)

    else:
        BC_Set = 1
        GDisplay('Waiting for Roaster', 'To Begin', 'Test', 'Please wait....')


with open('/home/pi/Bellwether/ADO_TEMP_DATA/_TEMP_Test_' + BC + '.csv', mode='w') as Test_file:  # Rpi
    Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    Test_writer.writerow(['Time', 'ADO', 'ADO_Rev', 'PN', 'SSN', 'Cycle Count', 'Resets', 'Min',
                          'Max', 'PASS / FAIL'])
    Test_file.flush()
while GPBi0.value == True:
    print ('Wait ', cnt)
    time.sleep(.5)
    cnt += 1
cnt = 0
time.sleep(1)
while GPBi0.value == True:  # needed for debounce
    print ('Wait Retry ', cnt)
    time.sleep(.5)
    cnt += 1
cnt = 0
while GPBi0.value == False:
    buf = datetime.datetime.now()
    date_ = buf.date()
    ldate_ = str(date_)
    time_ = buf.time()
    temp = round(sensor.tempF(0),1)
    note = ('Temp')
    state = temp
    if temp >= high:
        high = temp
    if temp <= low:
        low = temp

    l1 = str('ADO Temp')
    l2 = str('High ' + str(high) + 'F ' + 'Low '+ str(low) + 'F' )
    l3 = str('Sample ' + str(cnt))
    l4 = str('Current Temp '+ str(temp) + 'F')
    GDisplay(str(l1), str(l2), str(l3), str(l4))
    print('Count ', cnt, 'Temp ', temp)
    if temp >= setpoint:
        fail += 1
        cnt += 1
        res += 1
        log('ADO_TEMP_DATA', 'TEMP', 'N/A', str(temp), 'Fail')
    else:
        cnt += 1
        log('ADO_TEMP_DATA', 'TEMP', 'N/A', str(temp), 'Pass')
    time.sleep(sample_rate)

if fail >= 1:
    # mlog('ADO_MASTER_LIST_DATA', 'TEMP', str(low), str(high), 'Fail')
    l3 = str('High ' + str(high) + 'F ' + 'Low ' + str(low) + 'F')
    l4 = str('Sample Count ' + str(cnt))
    GDisplay('Temp Test', 'Failed', str(l3), str (l4))
else:
    mlog('ADO_MASTER_LIST_DATA', 'TEMP', low, high, 'Pass')
    l3 = str('High ' + str(high) + 'F ' + 'Low ' + str(low) + 'F')
    l4 = str('Sample Count ' + str(cnt))
    GDisplay('ADO Temp Test', 'PASS', str(l3), str(l4))
if high <= setpoint:
    result = ('PASS')
else:
    result = ('FAIL')
ulog('N/A', high, result)
print('End')