import csv
import os
from ADO_Unit import ado_

reset = int()
cnt = int(0)
BC = str("")
res = int(0)
fail = int(0)
reset = eval(input ("Purge Data Directories? '1' for Yes '0' for No: "))
if reset == 1:
    try:
        dirPath = "/home/pi/Bellwether/ADO_LOAD_DATA"
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            os.remove(dirPath + "/" + fileName)
            print ('Dir Removed')
    except FileNotFoundError:
        os.system('mkdir ADO_LOAD_DATA')
        print ('Directory Created')

    try:
        dirPath = "/home/pi/Bellwether/ADO_PNU_DROP_DATA"
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            os.remove(dirPath + "/" + fileName)
            print ('Dir Removed')
    except FileNotFoundError:
        os.system('mkdir ADO_PNU_DROP_DATA')
        print ('Directory Created')

    try:
        dirPath = "/home/pi/Bellwether/ADO_EXIT_DATA"
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            os.remove(dirPath + "/" + fileName)
            print ('Dir Removed')
    except FileNotFoundError:
        os.system('mkdir ADO_EXIT_DATA')
        print ('Directory Created')

    try:
        dirPath = "/home/pi/Bellwether/ADO_EXHAUST_DATA"
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            os.remove(dirPath + "/" + fileName)
            print ('Dir Removed')
    except FileNotFoundError:
        os.system('mkdir ADO_EXIT_DATA')
        print ('Directory Created')

    try:
        dirPath = "/home/pi/Bellwether/ADO_HVC_DATA"
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            os.remove(dirPath + "/" + fileName)
            print ('Dir Removed')
    except FileNotFoundError:
        os.system('mkdir ADO_HVC_DATA')
        print ('Directory Created')

    try:
        dirPath = "/home/pi/Bellwether/ADO_SLT_DATA"
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            os.remove(dirPath + "/" + fileName)
            print ('Dir Removed')
    except FileNotFoundError:
        os.system('mkdir ADO_SLT_DATA')
        print ('Directory Created')

    try:
        dirPath = "/home/pi/Bellwether/ADO_MASTER_LIST_DATA"
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            os.remove(dirPath + "/" + fileName)
            print ('Dir Removed')
    except FileNotFoundError:
        os.system('mkdir ADO_MASTER_LIST_DATA')
        print ('Directory Created')

    try:
        dirPath = "/home/pi/Bellwether/ADO_TEMP_DATA"
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            os.remove(dirPath + "/" + fileName)
            print ('Dir Removed')
    except FileNotFoundError:
        os.system('mkdir ADO_TEMP_DATA')
        print ('Directory Created')

    try:
        dirPath = "/home/pi/Bellwether/ADO_BP_DATA"
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            os.remove(dirPath + "/" + fileName)
            print ('Dir Removed')
    except FileNotFoundError:
        os.system('mkdir ADO_BP_DATA')
        print ('Directory Created')

    try:
        dirPath = "/home/pi/Bellwether/ADO_EXHAUST_DATA"
        fileList = os.listdir(dirPath)
        for fileName in fileList:
            os.remove(dirPath + "/" + fileName)
            print ('Dir Removed')
    except FileNotFoundError:
        os.system('mkdir /home/pi/Bellwether/ADO_EXHAUST_DATA')
        print ('Directory Created')

    print("Directories purged")

else:
    print("Directories purge skipped")

reset = eval(input ("Reset Master Lists? '1' for Yes '0' for No: "))
if reset == 1:
    with open('/home/pi/Bellwether/ADO_MASTER_LIST_DATA/Load_Master_List.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Date', 'Time', 'ADO','ADO_Rev' ,'PN', 'SSN', 'Cycle Count', 'Resets', 'Notes', 'State',
                              'PASS / FAIL', 'User'])
        Test_file.flush()
    with open('/home/pi/Bellwether/ADO_MASTER_LIST_DATA/Drop_Master_List.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Date', 'Time', 'ADO','ADO_Rev' ,'PN', 'SSN', 'Cycle Count', 'Resets', 'Notes', 'State',
                              'PASS / FAIL', 'User'])
        Test_file.flush()
    with open('/home/pi/Bellwether/ADO_MASTER_LIST_DATA/PNU_Drop_Master_List.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Date', 'Time', 'ADO','ADO_Rev' ,'PN', 'SSN', 'Cycle Count', 'Resets', 'Notes', 'State',
                              'PASS / FAIL', 'User'])
        Test_file.flush()
    with open('/home/pi/Bellwether/ADO_MASTER_LIST_DATA/Exit_Master_List.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Date', 'Time', 'ADO','ADO_Rev' ,'PN', 'SSN', 'Cycle Count', 'Resets', 'Notes', 'State',
                              'PASS / FAIL', 'User'])
        Test_file.flush()
    with open('/home/pi/Bellwether/ADO_MASTER_LIST_DATA/Exhaust_Master_List.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Date', 'Time', 'ADO','ADO_Rev' ,'PN', 'SSN', 'Cycle Count', 'Resets', 'Notes', 'State',
                              'PASS / FAIL', 'User'])
        Test_file.flush()
    with open('/home/pi/Bellwether/' + str(ado_) +'_' + 'Useage_Log.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Date', 'Time', 'ADO','Device' , 'SSN', 'Cycle Count', 'Resets', 'Notes','State', 'PASS / FAIL', 'User',
                              'ADO_Rev', 'TTime'])
        Test_file.flush()
    with open('/home/pi/Bellwether/ADO_MASTER_LIST_DATA/HVC_Master_List.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Date', 'Time', 'ADO','ADO_Rev' ,'PN', 'SSN', 'Cycle Count', 'Resets', 'Notes' ,'State',
                              'PASS / FAIL', 'User'])
        Test_file.flush()

    with open('/home/pi/Bellwether/ADO_MASTER_LIST_DATA/SLT_Master_List.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Date', 'Time', 'ADO','ADO_Rev' ,'PN', 'SSN', 'Cycle Count', 'Resets', 'Notes' ,'State',
                              'PASS / FAIL', 'User'])
        Test_file.flush()


    with open('/home/pi/Bellwether/ADO_MASTER_LIST_DATA/ST_Master_List.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Date', 'Time', 'ADO', 'ADO_Rev', 'PN', 'SSN', 'Cycle Count', 'Resets', 'Notes', 'State',
                              'PASS / FAIL', 'User'])

    with open('/home/pi/Bellwether/ADO_MASTER_LIST_DATA/TEMP_Master_List.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Date', 'Time', 'ADO', 'ADO_Rev', 'PN', 'SSN', 'Cycle Count', 'Resets', 'Notes', 'State',
                              'PASS / FAIL', 'User'])

    with open('/home/pi/Bellwether/ADO_MASTER_LIST_DATA/BP_Master_List.csv', mode='w') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow(['Date', 'Time', 'ADO', 'ADO_Rev', 'PN', 'SSN', 'Cycle Count', 'Resets', 'Notes', 'State',
                              'PASS / FAIL', 'User'])

    print("Master List Reset Complete")
else:
    print("Master List Reset Skipped")



reset = eval(input ("Reset ODO? '1' for Yes '0' for No: "))
if reset == 1:
    f = open('ADO_ODO_Load.py', "w")
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
    f = open('ADO_ODO_Drop.py', "w")
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
    f = open('ADO_ODO_PNU_Drop.py', "w")
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
    f = open('ADO_ODO_Exit.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' + "'" + str(BC) + "'")
    f.write('\n')
    f.write('res ' + '= ' + str(res))
    f.write('\n')
    f.write('fail ' + '= ' + str(fail))
    f.write('\n')
    # f.write('hall ' + '= ' + str(0))
    f.close()
    f = open('ADO_ODO_Exhaust.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.write('ssn ' + '= ' + "'" + str(BC) + "'")
    f.write('\n')
    f.write('res ' + '= ' + str(res))
    f.write('\n')
    f.write('fail ' + '= ' + str(fail))
    f.close()
    f = open('ADO_ODO_TEST.py', "w")
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
    f = open('ADO_ODO_HVC.py', "w")
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
    f = open('ADO_ODO_SLT.py', "w")
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
    f = open('ADO_ODO_ST.py', "w")
    f.write('cnt ' + '= ' + str(cnt))
    f.write('\n')
    f.close()
    f = open('/home/pi/Bellwether/ADO_SLT_List.py', "w")
    f.write('T1 ' + '= ' + "int(0)")
    f.write('\n')
    f.write('T2 ' + '= ' + "int(0)")
    f.write('\n')
    f.write('T3 ' + '= ' + "int(0)")
    f.write('\n')
    f.write('T4 ' + '= ' + "int(0)")
    f.write('\n')
    f.write('T5 ' + '= ' + "int(0)")
    f.write('\n')
    f.write('T6 ' + '= ' + "int(0)")
    f.write('\n')
    f.write('T7 ' + '= ' + "int(0)")
    f.write('\n')
    f.close()
    f = open('ADO_ODO_SLT.py', "w")
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
    f = open('ADO_ODO_BP.py', "w")
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
    print("ODO Reset Complete")

else:
    print("ODO Reset Skipped")


print("Reset Complete")