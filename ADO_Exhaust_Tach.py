import time
import datetime
import csv
import lcddriver
import lcddriver2
import pifacedigitalio as p
p.init()
import os
import sys
import RPi.GPIO as GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # Sets Physical Pin
GPIO.setup(13,GPIO.OUT) #<PWM
GPIO.setup(26,GPIO.IN, pull_up_down=GPIO.PUD_UP) #<--- Fan 1 Tach
GPIO.setup(19,GPIO.IN, pull_up_down=GPIO.PUD_UP) #<--- Fan 2 Tach
GPIO.setup(17,GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #<--- PWM Fan 1 Pull up Check todo change to pull down after debug
GPIO.setup(18,GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #<--- PWM Fan 2 Pull up Check todo change to pull down after debug
pwm = GPIO.PWM(13, 100)

p.digital_write(5, 1)
pwm.start(80)
time.sleep(00000)
p.digital_write(5, 0)