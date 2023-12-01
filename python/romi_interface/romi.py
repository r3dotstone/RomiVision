import smbus
import struct
import time

# i2c register for romi
addr = 20

class Romi:
  def __init__(self):
    self.bus = smbus.SMBus(1)

  def read_unpack(self, address, size, format):
    self.bus.write_byte(addr, address)
    time.sleep(0.001)
    byte_list = [self.bus.read_byte(addr) for _ in range(size)]
    return struct.unpack(format, bytes(byte_list))

  def write_pack(self, address, format, *data):
    data_array = list(struct.pack(format, *data))
    self.bus.write_i2c_block_data(addr, address, data_array)
    time.sleep(0.001)

  def motors(self, left, right):
    self.write_pack(0, 'hh', left, right)

  def read_encoders(self):
    return self.read_unpack(4, 4, 'hh')
