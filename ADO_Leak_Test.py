import os
import RPi.GPIO as GPIO
import pifacedigitalio as p
import time
p.init()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# Main Pressure
GPIO.setup(29,GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Leak Pressure
GPIO.setup(31,GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Hopper Present Bit
GPIO.setup(36,GPIO.IN, pull_up_down=GPIO.PUD_UP)

stop = int(0)
cnt = int(1)

p.digital_write(2, 0)
p.digital_write(3, 1)

# while stop == 0:
#     main = GPIO.input(29)
#     leak = GPIO.input(31)
#     print cnt
#     print 'Main', main
#     print 'leak', leak
#
#     cnt += 1
#     time.sleep(2)


