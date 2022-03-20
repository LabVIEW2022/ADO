import os
import datetime
import csv
d = datetime.datetime.now()
dirPath = "/home/pi/TMP/logs"
fileList = os.listdir(dirPath)
for fileName in fileList:
    os.remove(dirPath + "/" + fileName)

with open('/home/pi/TMP/logs/Temps.csv', mode='w') as Test_file:  # Rpi
    Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    Test_writer.writerow(['Creation Date', d])
    Test_writer.writerow(['Date', 'Time', 'Indoor', 'Outdoor', 'Delta', 'Sample'])

f = open('/home/pi/TMP/SNum.py', "w")
f.write('num = int(1)')
f.write('\n')
f.close()