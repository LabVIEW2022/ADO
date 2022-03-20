import csv
import time
import datetime

class Report:
    def __init__(self):
        pass

    def log(self, path, sub, note, state, result, tag, ado_, prg, BC, cnt, res, rev, fail):
        now = datetime.datetime.now()
        ddate = (now.strftime("%m-%d-%Y"))
        ttime = (now.strftime("%H:%M:%S"))
        rev2 = rev[7:]
        with open('/home/pi/Bellwether/' + path + '/' + '_' + sub + '_Test_' + BC + '.csv',
                  mode='a') as Test_file:  # Rpi
            Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            Test_writer.writerow([ddate, ttime, ado_, rev2, prg, BC, cnt, res, note, state, result, tag])
            Test_file.flush()
            f = open('/home/pi/Bellwether/ADO_ODO_' + sub + '.py', "w")
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

    def log_h(self, path, sub, BC):
        with open('/home/pi/Bellwether/' + path + '/' + '_' + sub + '_Test_' + BC + '.csv',
                  mode='w') as Test_file:  # Rpi
            Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            Test_writer.writerow(['Date', 'Time', 'ADO', 'ADO_Rev', 'PN', 'SSN', 'Cycle Count', 'Resets', 'Note',
                                  'State', 'PASS / FAIL', 'Operator'])


    def mlog(self, path, sub, note, state, result, tag, ado_, prg, BC, cnt, res, rev):
        now = datetime.datetime.now()
        ddate = (now.strftime("%m-%d-%Y"))
        ttime = (now.strftime("%H:%M:%S"))
        rev2 = rev[7:]
        with open('/home/pi/Bellwether/' + path + '/' + sub + '_Master_List.csv', mode='a') as Test_file:  # Rpi
            Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            Test_writer.writerow([ddate, ttime, ado_, rev2, prg, BC, cnt, res, note, state, result, tag])
            Test_file.flush()




report = Report