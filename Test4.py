from ADO_Step import ado_step
from ADO import ado
import time

con = float(1.5706)
ado.V24Off()
input('Power On?')
time.sleep(3)
ado.V24A()
time.sleep(5)
ado_step.home()
from ADO_Decoder import Encoder
enc = Encoder(18, 17)