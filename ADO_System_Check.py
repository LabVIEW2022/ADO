#!/usr/bin/env python
import time
import datetime
import csv
import lcddriver
import pifacedigitalio as p
import os
import RPi.GPIO as GPIO
import sys
from ADO_Rev import rev

p.init()

latch = int(0)
button = int(0)
display = lcddriver.lcd()


# p.digital_write(7, 1)
display.lcd_clear()
display.lcd_display_string("Bellwether Co. ADO", 1)
display.lcd_display_string('System Test'         , 2)
display.lcd_display_string(str(rev), 4)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Sets Physical Pin
# GPIO.cleanup() # Sets up GPIO Pin as output
GPIO.setup(40,GPIO.OUT) # Sets up GPIO Pin as output
GPIO.setup(33,GPIO.OUT)
# GPIO.output(11,False) # Pin Low
# GPIO.output(11,True) # Pin High





while latch == 0:
        button = p.digital_read(7)
        if button == 1:
            p.digital_write(6,0)
            p.digital_write(7,0)
            GPIO.output(40, 0)
            time.sleep(.5)
            p.digital_write(0, 1)
            time.sleep(.5)
            p.digital_write(1, 1)
            time.sleep(.5)
            p.digital_write(2, 1)
            time.sleep(.5)
            p.digital_write(3, 1)
            time.sleep(.5)
            p.digital_write(4, 1)
            time.sleep(.5)
            p.digital_write(5, 1)
            time.sleep(.5)
            p.digital_write(6, 1)
            time.sleep(.5)
            p.digital_write(7, 1)
            time.sleep(.5)
            p.digital_write(6, 0)
            time.sleep(.5)
            GPIO.output(33, 1)
            time.sleep(.5)
            GPIO.output(40, 1)

            p.digital_write(0, 0)
            p.digital_write(1, 0)
            p.digital_write(2, 0)
            p.digital_write(3, 0)
            p.digital_write(4, 0)
            p.digital_write(5, 0)
            p.digital_write(6, 0)
            p.digital_write(7, 0)
            GPIO.output(33, 0)


            # pwm = GPIO.PWM(40, 100)  # Pin, Hz
            # pwm.start(20)
            # time.sleep(2)
            # pwm.start(80)
            # time.sleep(2)
            # pwm.stop()

        else:
            p.digital_write(6, 1)
            time.sleep(.5)
            p.digital_write(6, 0)
            time.sleep(.5)

        print(button)


