import time
from ADO_EIOp import GPAp0
from ADO_EIOp import GPAp1
from ADO_EIOp import GPAp2
from ADO_EIOp import GPAp3
from ADO_EIOp import GPAp4
from ADO_EIOp import GPAp5
from ADO_EIOp import GPAp6
from ADO_EIOp import GPAp7
from ADO import ado

#Note:  V0 = Bean Exit, V1 = Belly Drop, V2 = Bean Load


class SLT:
    def __init__(self):
        pass
    
    def V0(self, state): # Bean Exit
        if state == 0:
            GPAp0.switch_to_output(True)
        elif state == 1:
            GPAp0.switch_to_output(False)
            
    def V1(self, state): # Belly Drop
        if state == 0:
            GPAp1.switch_to_output(True)
        elif state == 1:
            GPAp1.switch_to_output(False)
            
    def V2(self, state): # Bean Load
        if state == 0:
            GPAp2.switch_to_output(True)
        elif state == 1:
            GPAp2.switch_to_output(False)
            
    def V3(self, state):
        if state == 0:
            GPAp3.switch_to_output(True)
        elif state == 1:
            GPAp3.switch_to_output(False)
            
    def V4(self, state):
        if state == 0:
            GPAp4.switch_to_output(True)
        elif state == 1:
            GPAp4.switch_to_output(False)
            
    def V5(self, state):
        if state == 0:
            GPAp5.switch_to_output(True)
        elif state == 1:
            GPAp5.switch_to_output(False)
            
    def V6(self, state):
        if state == 0:
            GPAp6.switch_to_output(True)
        elif state == 1:
            GPAp6.switch_to_output(False)
            
    def V7(self, state):
        if state == 0:
            GPAp7.switch_to_output(True)
        elif state == 1:
            GPAp7.switch_to_output(False)
            
slt = SLT()

# ado.V24A()
#
# while True:
#     slt.V0(1)
#     time.sleep(0.2)
#     slt.V1(1)
#     time.sleep(0.2)
#     slt.V2(1)
#     time.sleep(0.2)
#     slt.V3(1)
#     time.sleep(0.2)
#     slt.V4(1)
#     time.sleep(0.2)
#     slt.V5(1)
#     time.sleep(0.2)
#     slt.V6(1)
#     time.sleep(0.2)
#     slt.V7(1)
#     time.sleep(0.2)
#
#
#     slt.V0(0)
#     time.sleep(0.2)
#     slt.V1(0)
#     time.sleep(0.2)
#     slt.V2(0)
#     time.sleep(0.2)
#     slt.V3(0)
#     time.sleep(0.2)
#     slt.V4(0)
#     time.sleep(0.2)
#     slt.V5(0)
#     time.sleep(0.2)
#     slt.V6(0)
#     time.sleep(0.2)
#     slt.V7(0)
#     time.sleep(0.2)
