#!/usr/bin/env python
# Install
# sudo pip install speedtest-cli
# speedtest-cli #Runs Speed Test
# speedtest-cli --simple #Runs Simple Speed Test
# pip install ipwhois <-- ISP lookup
# git clone https://github.com/ActivisionGameScience/pyisp.git

import os
import re
import subprocess
import time
import datetime
import pifacedigitalio as p
import os
import sys
import lcddriver


band = str('')
ping = str('')
download = str('')
upload = str('')
TD = str('')
TT = str('')
cnt = 1
cnt2 = 0
i1 = int(0)
p.init()
display = lcddriver.lcd()

TD = str(datetime.date.today())
print(TD)


display.lcd_display_string("Bellwether ADO", 1)
display.lcd_display_string('Network Speed   RL', 2)
time.sleep(2)



display.lcd_clear()
display.lcd_display_string("Running Speed Test", 1)
display.lcd_display_string("Please Wait", 2)
display.lcd_display_string("....................", 3)
display.lcd_display_string("....................", 4)


response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()
#
#
#
ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

ping1 = ("Ping", ping)
download1 = ("Down", download)
upload1 = ("Up", upload)


response = subprocess.Popen('iwlist wlan0 frequency', shell=True, stdout=subprocess.PIPE).stdout.read()
# print response
band = re.findall('Frequency:\d\D\d', response, re.MULTILINE)

display.lcd_clear()
display.lcd_display_string(str(band), 1)
display.lcd_display_string(str(ping1), 2)
display.lcd_display_string(str(download1), 3)
display.lcd_display_string(str(upload1), 4)

os.execv('/home/pi/Bellwether/ADO_Exhaust.py', sys.argv)

while i1 == False:
    i1 = p.digital_read(0)
    time.sleep(.5)

import BW_UI

