import pifacedigitalio as p
import RPi.GPIO as GPIO
from ADO_WatchDog import WD
import time
import lcddriver
display = lcddriver.lcd()
from ADO_EIOi import GPAi0
from ADO_EIOi import GPAi1
from ADO_EIOi import GPAi2
from ADO_EIOi import GPAi3
p.init()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Main Pressure
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Leak Pressure
GPIO.setup(26,GPIO.IN, pull_up_down=GPIO.PUD_UP) #<--- Fan 1 Tach
GPIO.setup(19,GPIO.IN, pull_up_down=GPIO.PUD_UP) #<--- Fan 2 Tach
GPIO.setup(16,GPIO.IN, pull_up_down=GPIO.PUD_UP) #<--- External Reset
GPIO.setup(13,GPIO.OUT) #<PWM



class ADO:
    def __init__(self):
        pass

    def OPN(self):
        p.digital_write(2, 1)
        p.digital_write(3, 0)

    def OPN_S(self):
        self.state = p.digital_read(2)
        return self.state

    def CLS(self):
        p.digital_write(2, 0)
        p.digital_write(3, 1)

    def CLS_S(self):
        self.state = p.digital_read(3)
        return self.state

    def OCO(self):
        p.digital_write(2, 0)
        p.digital_write(3, 0)

    def OCOn(self):
        p.digital_write(2, 1)
        p.digital_write(3, 1)

    def ISO(self):
        if GPAi0.value == True:
            GPAi0.switch_to_output(False)
            self.state = 1
        elif GPAi0.value == False:
            GPAi0.switch_to_output(True)
            self.state = 0
    def ISO_(self, bit):
        if bit == 0:
            GPAi0.switch_to_output(True)
        elif bit == 1:
            GPAi0.switch_to_output(False)
    def CDA(self):
        if GPAi1.value == True:
            GPAi1.switch_to_output(False)
            self.state = 1
        elif GPAi1.value == False:
            GPAi1.switch_to_output(True)
            self.state = 0

    def CDA_(self, bit):
        if bit == 0:
            GPAi1.switch_to_output(True)
        elif bit == 1:
            GPAi1.switch_to_output(False)

    def PNU_ISO(self):
        if GPAi2.value == True:
            GPAi2.switch_to_output(False)
            self.state = 1
        elif GPAi2.value == False:
            GPAi2.switch_to_output(True)
            self.state = 0
        return self.state

    def PNU_ISO_(self, bit):
        if bit == 0:
            GPAi2.switch_to_output(True)
        elif bit == 1:
            GPAi2.switch_to_output(False)

    def B_Green(self):
        p.digital_write(7, 0)
        p.digital_write(6, 1)

    def B_Red(self):
        p.digital_write(6, 0)
        p.digital_write(7, 1)

    def B_Yellow(self):
        p.digital_write(6, 1)
        p.digital_write(7, 1)

    def B_Off(self):
        p.digital_write(6, 0)
        p.digital_write(7, 0)

    def V24A(self):
        p.digital_write(0, 0)
        p.digital_write(1, 0)
        p.digital_write(0, 1)
        print('V24A On')

    def V24B(self): # CPC pin 3 High
        p.digital_write(0, 0)
        p.digital_write(1, 0)
        p.digital_write(1, 1)
        print ('V24B On')

    def V24Off(self): # CPC pin 4 High
        p.digital_write(0, 0)
        p.digital_write(1, 0)
        print('V24 A and B off')

    def V48(self): # CPC pin 6 High
        p.digital_write(5, 1)

    def V48Off(self):
        p.digital_write(5, 0)

    def PWM(self, dutycycle):
        pwm = GPIO.PWM(13, 100)
        dutycycle_ = 100 - dutycycle
        pwm.start(dutycycle_)
        print('PWM @ ' + str(dutycycle))
        input('Press Return to end')

    def PWM_Stop(self):
        pwm.stop()
        print('PWM Off')

    def Mag(self):
        p.digital_write(4, 1)
        time.sleep(1)
        p.digital_write(4, 0)

    def SHOPS(self):
        self.state = p.digital_read(4)
        return self.state

    def Min_CDA(self):
        self.state = GPIO.input(5)
        return self.state

    def Leak_S(self):
        self.state = GPIO.input(6)
        return self.state

    def BTN(self):
        self.state = p.digital_read(7)
        return self.state

    def GDisplay(self, Line1, Line2, Line3, Line4):
        display.lcd_clear()
        display.lcd_display_string(Line1, 1)
        display.lcd_display_string(Line2, 2)
        display.lcd_display_string(Line3, 3)
        display.lcd_display_string(Line4, 4)

    def GDisplay_Cnt(self, Line3):
        display.lcd_display_string(Line3, 3)
    def GDisplay_CLR(self):
        display.lcd_clear()
    def GScroll(self, text='', num_line=1, num_cols=20):
        if D_OLED == 1:
            if (len(text) > num_cols):
                display2.lcd2_display_string(text[:num_cols], num_line)
                time.sleep(1)
                for i in range(len(text) - num_cols + 1):
                    text_to_print = text[i:i + num_cols]
                    display2.lcd2_display_string(text_to_print, num_line)
                    time.sleep(0.1)
                time.sleep(1)
            else:
                display2.lcd2_display_string(text, num_line)
        else:
            if (len(text) > num_cols):
                display.lcd_display_string(text[:num_cols], num_line)
                time.sleep(1)
                for i in range(len(text) - num_cols + 1):
                    text_to_print = text[i:i + num_cols]
                    display.lcd_display_string(text_to_print, num_line)
                    time.sleep(0.2)
                time.sleep(1)
            else:
                display.lcd_display_string(text, num_line)
    def Reset(self):
        GPIO.wait_for_edge(16, GPIO.FALLING)
        GPIO.cleanup()

ado = ADO()


