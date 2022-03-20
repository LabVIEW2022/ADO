import time
import pifacedigitalio as p
p.init()
import lcddriver
display = lcddriver.lcd()

loop = int(0)
cnt = int(0)
button = int(0)
ver = str('Rev 1.0')


def GDisplay(Line1,Line2):
        display.lcd_clear()
        display.lcd_display_string(Line1, 1)
        display.lcd_display_string(Line2, 2)
def Open():
        p.digital_write(0, 1)
        p.digital_write(1, 0)
def Close():
        p.digital_write(0, 0)
        p.digital_write(1, 1)
def Cycle():
        Open()
        time.sleep(5)
        Close()
        time.sleep(5)

GDisplay('Valve Board', ver)
time.sleep(5)
GDisplay('Press Button 1', 'To Begin')

while p.digital_read(0) != 1:
        print('wait')
display.lcd_clear()
print('Here')

Close()
while loop != 1:
        if p.digital_read(0) == 1:
                GDisplay('Open', '')
                Open()
        if p.digital_read(1) == 1:
                GDisplay('Close', '')
                Close()
        if p.digital_read(2) == 1:

                while p.digital_read(3) != 1:
                        GDisplay('Cycle Count', str(cnt))
                        Cycle()
                        cnt += 1
                display.lcd_clear()
                GDisplay('Press Button 1', 'To Begin')
