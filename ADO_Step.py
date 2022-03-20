from smbus2 import SMBus, i2c_msg
import ADO_Decoder
import time
bus = SMBus(11)
address = 14

class TicI2C(object):
    def __init__(self, bus, address):
        self.bus = bus
        self.address = address

    def exit_safe_start(self):
        command = [0x83]
        write = i2c_msg.write(self.address, command)
        self.bus.i2c_rdwr(write)

    def goto(self, target):
        command = [0xE0,
                   target >> 0 & 0xFF,
                   target >> 8 & 0xFF,
                   target >> 16 & 0xFF,
                   target >> 24 & 0xFF]
        write = i2c_msg.write(self.address, command)
        self.bus.i2c_rdwr(write)

    def get_variables(self, offset, length):
        write = i2c_msg.write(self.address, [0xA1, offset])
        read = i2c_msg.read(self.address, length)
        self.bus.i2c_rdwr(write, read)
        return list(read)

    def pos(self):
        b = self.get_variables(0x22, 4)
        position = b[0] + (b[1] << 8) + (b[2] << 16) + (b[3] << 24)
        if position >= (1 << 31):
            position -= (1 << 32)
        return position

    def safe_start(self):
        command = [0x8F]
        write = i2c_msg.write(self.address, command)
        self.bus.i2c_rdwr(write)

    def servo(self):
        command = [0x85]
        write = i2c_msg.write(self.address, command)
        self.bus.i2c_rdwr(write)

    def dservo(self):
        command = [0x86]
        write = i2c_msg.write(self.address, command)
        self.bus.i2c_rdwr(write)

    def reset(self):
        command = [0xB0]
        write = i2c_msg.write(self.address, command)
        self.bus.i2c_rdwr(write)

    def cerror(self):
        command = [0x8A]
        write = i2c_msg.write(self.address, command)
        self.bus.i2c_rdwr(write)

    def home(self):
        TicI2C.servo(self)
        TicI2C.exit_safe_start(self)
        time.sleep(1)
        TicI2C.goto(self, -2400)
        time.sleep(5)
        TicI2C.reset(self)
        time.sleep(1)
        TicI2C.servo(self)
        TicI2C.exit_safe_start(self)



ado_step = TicI2C(bus, address)