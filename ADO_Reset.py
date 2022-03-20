import time
import os
from ADO import ado


ado.Reset()
ado.GDisplay('System Reset', 'Please Wait', '', '')
os.system('sudo reboot')