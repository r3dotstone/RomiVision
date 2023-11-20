# Copyright Pololu Corporation.  For more information, see https://www.pololu.com/
import smbus
import struct
import time

addr = 20

class AStar:
  def __init__(self):
    self.bus = smbus.SMBus(1)

  def read_unpack(self, address, size, format):
    # Ideally we could do this:
    #    byte_list = self.bus.read_i2c_block_data(20, address, size)
    # But the AVR's TWI module can't handle a quick write->read transition,
    # since the STOP interrupt will occasionally happen after the START
    # condition, and the TWI module is disabled until the interrupt can
    # be processed.
    #
    # A delay of 0.0001 (100 us) after each write is enough to account
    # for the worst-case situation in our example code.

    self.bus.write_byte(addr, address)
    time.sleep(0.0001)
    byte_list = [self.bus.read_byte(addr) for _ in range(size)]
    return struct.unpack(format, bytes(byte_list))

  def write_pack(self, address, format, *data):
    data_array = list(struct.pack(format, *data))
    self.bus.write_i2c_block_data(addr, address, data_array)
    time.sleep(0.0001)

  def motors(self, left, right):
    self.write_pack(0, 'hh', left, right)

  def read_encoders(self):
    return self.read_unpack(4, 4, 'hh')
