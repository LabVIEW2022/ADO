#!/usr/bin/env python
# Install
# sudo pip install speedtest-cli
# speedtest-cli #Runs Speed Test
# speedtest-cli --simple #Runs Simple Speed Test
# pip install ipinfo
# pip install dropbox

"""
NOTE:  TO INSTALL ON MACHINE INSTALL:
sudo pip install dropbox
sudo pip install speedtest-cli
sudo pip install ipinfo

Create directory "Bellwether" and install:
ADO_Wifi_Speed_Test
ADO_Unit (Add Machine Number)
"""

import dropbox
from dropbox.files import WriteMode
from ADO_Unit import ado_
import re
import subprocess
import datetime
import csv
import ipinfo
import time
import os
import sys
band = str('')
ping = str('')
download = str('')
upload = str('')
TD = str('')
TT = str('')
cnt = 1
cnt2 = 0
unt = int(1) # <----- Deployed Unit

TD = str(datetime.date.today())

print(TD)

time.sleep(30)



access_token = '6c3d849c913a11'
handler = ipinfo.getHandler(access_token)
# ip_address = ''
details = handler.getDetails()
city = details.city
state = details.region
postal = details.postal
ISP = details.org
ip2 = details.ip




print(city)
print(state)
print(postal)
print(ISP)
print(ip2)

while cnt != 0:



    response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read()

    ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
    download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
    upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)
    response = subprocess.Popen('iwlist wlan0 frequency', shell=True, stdout=subprocess.PIPE).stdout.read()
    band = re.findall('Frequency:\d\D\d', response, re.MULTILINE)


    # with open('Wifi_Sniff/_WiFi_' + str(city) + '_' + str(postal) + '.csv', mode='a') as TD_file:  # Rpi
    with open('_WiFi_' + str(city) + '_' + str(postal) + '.csv', mode='a') as TD_file:  # Rpi
        TT = datetime.datetime.now()
        print(TT)
        print(TT)
        TD_writer = csv.writer(TD_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # TD_writer.writerow(['Info', 'ISP', ISP, 'IP', ip2, 'City', city, 'State', state, 'Postal', postal ])
        TD_writer.writerow([TT,'Band',band, 'Ping', ping, 'Down', download, 'UP', upload , 'ISP', ISP, 'IP', ip2, 'City', city, 'State', state, 'Postal', postal ])
        TD_file.flush()
    # file_name = ('Wifi_Sniff/_WiFi_' + str(city) + '_' + str(postal) + '.csv')
    file_name = ('_WiFi_' + str(city) + '_' + str(postal) + '.csv')
    dropbox_path = '/WifiTest/' + ado_ + '/'
    dbx = dropbox.Dropbox('TYQkL_IX4lAAAAAAAAABrz9rDoR4S3zXJgLYqiREuqOAVmUK4vvAiEUWVY9LII22')
    with open(file_name, 'r+') as f:
        dbx.files_upload(f.read(), dropbox_path + file_name,mode=dropbox.files.WriteMode.overwrite, mute=True)

    print((city, state, postal, ISP, ip2))
    print((TT ,'Band', band, 'Ping', ping, 'Down', download,'Up', upload))
    print("Uploaded to Dropbox")


    cnt -=1
    cnt2 +=1
    print(cnt2)



os.execv('/home/pi/Bellwether/ADO_UI.py', sys.argv)




