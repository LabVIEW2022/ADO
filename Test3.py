from ADO_Step import ado_step
import time
import csv
ado_step.home()
con = float(1.579)
ado_step.goto(0)
time.sleep(5)
from ADO_Decoder import Encoder
enc = Encoder(18, 17)
name = ('NewDay3')

print('Now')
while True:
    ado_step.goto(0)
    time.sleep(5)
    tic = enc.read() * con
    open_ = int(tic)
    print(str(ado_step.pos()) + ' ' + str(open_))
    print('')
    ado_step.goto(2400)
    time.sleep(5)
    tic = enc.read() * con
    closed_ = int(tic)
    print(str(ado_step.pos()) + ' ' + str(closed_))
    time.sleep(5)
    with open('/home/pi/logs/Encoder_' + str(name) + '.csv', mode='a') as Test_file:  # Rpi
        Test_writer = csv.writer(Test_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        Test_writer.writerow([open_, closed_])
        Test_file.flush()


# while True:
#     ado_step.goto(-2400)
#     print (enc.read() * con)
#     # print('')
#     time.sleep(3)
#     ado_step.goto(0)
#     print(enc.read() * con)
#     print()
#     time.sleep(3)