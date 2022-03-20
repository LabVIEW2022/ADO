import time
import board
import busio
from adafruit_mcp230xx.mcp23017 import MCP23017
i2c = busio.I2C(board.SCL, board.SDA)

init_io = int(5)

while init_io != 0:
    EIOi = MCP23017(i2c, address=0x23)  # MCP23017
    time.sleep(.25)
    init_io -= 1



# IO Board Internal 0x22 # For ADO only
GPAi0 = EIOi.get_pin(0)  # GPAi0 Iso Relay
GPAi1 = EIOi.get_pin(1)  # GPAi1 System Leak Relay
GPAi2 = EIOi.get_pin(2)  # GPAi2 Leak Test Relay
GPAi3 = EIOi.get_pin(3)  # GPAi3
GPAi4 = EIOi.get_pin(4)  # GPAi4
GPAi5 = EIOi.get_pin(5)  # GPAi5
GPAi6 = EIOi.get_pin(6)  # GPAi6
GPAi7 = EIOi.get_pin(7)  # GPAi7

GPBi0 = EIOi.get_pin(8)  # GPBi0
GPBi1 = EIOi.get_pin(9)  # GPBi1
GPBi2 = EIOi.get_pin(10)  # GPBi2
GPBi3 = EIOi.get_pin(11)  # GPBi3
GPBi4 = EIOi.get_pin(12)  # GPBi4
GPBi5 = EIOi.get_pin(13)  # GPBi5
GPBi6 = EIOi.get_pin(14)  # GPBi6
GPBi7 = EIOi.get_pin(15)  # GPBi7
#
#
GPAi0.switch_to_output(value=True)# Initial Setup in the off state
GPAi1.switch_to_output(value=True)# Initial Setup in the off state
GPAi2.switch_to_output(value=True)# Initial Setup in the off state
GPAi3.switch_to_output(value=True)# Initial Setup in the off state
GPAi4.switch_to_output(value=True)# Initial Setup in the off state
GPAi5.switch_to_output(value=True)# Initial Setup in the off state
GPAi6.switch_to_output(value=True)# Initial Setup in the off state
GPAi7.switch_to_output(value=True)# Initial Setup in the off state

GPBi0.switch_to_output(value=True)# Initial Setup in the off state
GPBi1.switch_to_output(value=True)# Initial Setup in the off state
GPBi2.switch_to_output(value=True)# Initial Setup in the off state
GPBi3.switch_to_output(value=True)# Initial Setup in the off state
GPBi4.switch_to_output(value=True)# Initial Setup in the off state
GPBi5.switch_to_output(value=True)# Initial Setup in the off state
GPBi6.switch_to_output(value=True)# Initial Setup in the off state
GPBi7.switch_to_output(value=True)# Initial Setup in the off state