import pylablib as pll
from pylablib.devices import NKT


class Extreme:
    def __init__(self, port):

        self.laser = None

        self.laser_addr = 15  # 15 for Extreme/Fianum lasers

        self.open_connection(port)


    def system_type(self):
        register_address = 0x60
        return self.laser.ib_get_reg(self.laser_addr, register_address, "u8")

    def open_connection(self, port):
        self.laser = NKT.GenericInterbusDevice(port)

    def close_connection(self):
        # register_address = 0x30
        # self.laser.ib_set_reg(self.laser_addr, register_address, 0, "u8")  # Turn OFF laser
        self.laser.close()

    def set_power(self, value: int):
        register_address = 0x37
        self.laser.ib_set_reg(self.laser_addr, register_address, value, "u16")

    def set_emission(self, state):
        register_address = 0x30
        self.laser.ib_set_reg(self.laser_addr, register_address, state, "u8")


if __name__ == "__main__":
    laser = Extreme()
    print(laser.system_type())