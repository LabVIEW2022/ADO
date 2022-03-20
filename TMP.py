#Beta 2
import time
import datetime
import csv
import lcddriver
display = lcddriver.lcd()
from ds18b20 import DS18B20
from SNum import num
import dropbox
from dropbox.files import WriteMode
access_token = '6c3d849c913a11'
# Internal probe 28-0312977916ed ADD 0
# External probe 28-03129779d336 ADD 1
# test temperature sensors
sensor = DS18B20()
D_OLED = int(0)
rev = str('RL  Rev 1.0.0.00.00B')
loop = int(0)
counter = str('')
db = int(0)
debug = int(0)

sample_rate = int(60)  #sample rate in seconds


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




GDisplay('BW ADO Project', 'Temp Differential ','Indoor / Outdoor', rev)
time.sleep(5)



while loop != 1:

    buf = datetime.datetime.now()
    date_ = buf.date()
    time_ = buf.time()
    cal = round(sensor.tempF(0),1)   # Calibration
    cal = round(cal, 1)
    indoor = ('Indoor Temp  ' + str(cal) + 'F')
    cal2 = round(sensor.tempF(1),1) + 3.8  # Calibration
    cal2 = round(cal2, 1)
    outdoor = ('Outdoor Temp ' + str(cal2) + 'F')
    diff = round(cal - cal2, 1)
    diff =abs(diff)
    diff2 = ('Difference    ' + str(diff) + 'F')
    GDisplay(indoor,outdoor,diff2,'')
    if sample_rate >= 3600:
        srate = sample_rate / 3600
        srate = round(srate,2)
        sm = str('H')
    elif sample_rate >= 60:
        srate = sample_rate / 60
        srate = round(srate, 2)
        sm = str('m')
    else:
        srate = sample_rate
        sm = str('s')
    scroll=('Sample Rate ' + str(srate)+ sm + ' ' +  'Current Sample ' + str(num) +'      ' +
            '        Sample ' + str(num))
    GScroll(scroll, 4)

    if debug != 1:
        with open('/home/pi/TMP/logs/Temps.csv', mode='a') as Test_file:  # Rpi
            Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            Test_writer.writerow([str(date_), str(time_), str(cal), str(cal2), str(diff), str(num)])
            num += 1
            Test_file.flush()
        f = open('/home/pi/TMP/SNum.py', "w")
        f.write('num ' + '= ' + str(num))
        f.write('\n')
        f.close()

    print(num)
    if db == 1:

        file_name = ('/home/pi/TMP/logs/Temps.csv')
        dropbox_path = '/ADO_Log/'
        dbx = dropbox.Dropbox('TYQkL_IX4lAAAAAAAAABrz9rDoR4S3zXJgLYqiREuqOAVmUK4vvAiEUWVY9LII22')
        with open(file_name, 'r+') as f:
            dbx.files_upload(f.read(), dropbox_path + file_name, mode=dropbox.files.WriteMode.overwrite, mute=True)
        print('Uploaded to DB')
        print('Iteration ', num)


    time.sleep(sample_rate)






