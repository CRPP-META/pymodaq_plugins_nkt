from pylablib.devices import NKT


class Extreme:
    def __init__(self, port):

        self.laser = None

        self.laser_addr = 15  # 15 for Extreme/Fianum lasers

        self.open_connection(port)

    def open_connection(self, port):
        self.laser = NKT.GenericInterbusDevice(port)

    def close_connection(self):
        # register_address = 0x30
        # self.laser.ib_set_reg(self.laser_addr, register_address, 0, "u8")  # Turn OFF laser
        self.laser.close()

    def system_address(self):
        register_address = 0x60
        return self.laser.ib_get_reg(self.laser_addr, register_address, "u8")
    
    def get_temp(self):  # Inlet temperature
        register_address = 0x11
        return self.laser.ib_get_reg(self.laser_addr, register_address, "u8")
    
    def interlock(self):
        """
        The first byte (LSB) indicates if the interlock circuit is open or closed.
        The second byte (MSB) indicates where the interlock circuit is open, if relevant.
        """
        register_address = 0x32
        return self.laser.ib_get_reg(self.laser_addr, register_address, "u8")

    def status(self) -> int:
        """ Returns laser status bit as a 16-bit integer 
        Bit 0: Emission on
        Bit 1: Interlock relays off
        Bit 2: Interlock supply voltage low (possible short circuit)
        Bit 3: Interlock loop open
        Bit 4: Output Control signal low
        Bit 5: Supply voltage low
        Bit 6: Inlet temperature out of range
        Bit 7: Clock battery low voltage
        ...
        Bit 13: CRC error on startup (possible module address conflict)
        Bit 14: Log error code present
        Bit 15: System error code present
        """
        register_address = 0x66
        return self.laser.ib_get_reg(self.laser_addr, register_address, "u16")

    def set_power(self, value: int):
        register_address = 0x37
        self.laser.ib_set_reg(self.laser_addr, register_address, value, "u16")

    def set_emission(self, state):  # state = 0 for OFF, state = 3 for ON
        register_address = 0x30
        self.laser.ib_set_reg(self.laser_addr, register_address, state, "u8")


# if __name__ == "__main__":
#     laser = Extreme('COM5')
#     # print(laser.system_type())