import time
import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = busio.I2C(board.SCL, board.SDA)

init_io = int(5)

while init_io != 0:
    EIOp = MCP23017(i2c, address=0x24)  # MCP23017
    time.sleep(.25)
    init_io -= 1



# IO Board Pneumatic 0x21
GPAp0 = EIOp.get_pin(0)  # GPAp0
GPAp1 = EIOp.get_pin(1)  # GPAp1
GPAp2 = EIOp.get_pin(2)  # GPAp2
GPAp3 = EIOp.get_pin(3)  # GPAp3
GPAp4 = EIOp.get_pin(4)  # GPAp4
GPAp5 = EIOp.get_pin(5)  # GPAp5
GPAp6 = EIOp.get_pin(6)  # GPAp6
GPAp7 = EIOp.get_pin(7)  # GPAp7

GPBp0 = EIOp.get_pin(8)  # GPBp0
GPBp1 = EIOp.get_pin(9)  # GPBp1
GPBp2 = EIOp.get_pin(10)  # GPBp2
GPBp3 = EIOp.get_pin(11)  # GPBp3
GPBp4 = EIOp.get_pin(12)  # GPBp4
GPBp5 = EIOp.get_pin(13)  # GPBp5
GPBp6 = EIOp.get_pin(14)  # GPBp6
GPBp7 = EIOp.get_pin(15)  # GPBp7
#
#
GPAp0.switch_to_output(value=True)# Initial Setup in the off state
GPAp1.switch_to_output(value=True)# Initial Setup in the off state
GPAp2.switch_to_output(value=True)# Initial Setup in the off state
GPAp3.switch_to_output(value=True)# Initial Setup in the off state
GPAp4.switch_to_output(value=True)# Initial Setup in the off state
GPAp5.switch_to_output(value=True)# Initial Setup in the off state
GPAp6.switch_to_output(value=True)# Initial Setup in the off state
GPAp7.switch_to_output(value=True)# Initial Setup in the off state

GPBp0.switch_to_output(value=True)# Initial Setup in the off state
GPBp1.switch_to_output(value=True)# Initial Setup in the off state
GPBp2.switch_to_output(value=True)# Initial Setup in the off state
GPBp3.switch_to_output(value=True)# Initial Setup in the off state
GPBp4.switch_to_output(value=True)# Initial Setup in the off state
GPBp5.switch_to_output(value=True)# Initial Setup in the off state
GPBp6.switch_to_output(value=True)# Initial Setup in the off state
GPBp7.switch_to_output(value=True)# Initial Setup in the off state