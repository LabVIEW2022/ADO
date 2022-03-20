# AD0 Quadrature
import RPi.GPIO as GPIO

class Encoder(object):
    def __init__(self, A, B): # Define Pins for A and B SoC Pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.A = A
        self.B = B
        self.pos = 0
        self.state = 0
        if GPIO.input(A):
            self.state |= 1
        if GPIO.input(B):
            self.state |= 2
        GPIO.add_event_detect(A, GPIO.BOTH, callback=self.__update)
        GPIO.add_event_detect(B, GPIO.BOTH, callback=self.__update)

    def __update(self, channel):
        state = self.state & 3
        if GPIO.input(self.A):
            state |= 4
        if GPIO.input(self.B):
            state |= 8

        self.state = state >> 2

        if state == 1 or state == 7 or state == 8 or state == 14:
            self.pos += 1
        elif state == 2 or state == 4 or state == 11 or state == 13:
            self.pos -= 1
        elif state == 3 or state == 12:
            self.pos += 2
        elif state == 6 or state == 9:
            self.pos -= 2

    def zero(self):
        def __init__(self, A, B):
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(B, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.A = A
            self.B = B
            self.pos = 0
            self.state = 0
            if GPIO.input(A):
                self.state |= 1
            if GPIO.input(B):
                self.state |= 2
            GPIO.add_event_detect(A, GPIO.BOTH, callback=self.__update)
            GPIO.add_event_detect(B, GPIO.BOTH, callback=self.__update)
    def read(self):
        return self.pos
