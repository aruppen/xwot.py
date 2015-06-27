#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       12.06.2015

"""

import struct
import smbus


class Adapter(object):

    def __init__(self, bus=1, i2c_addr=0x04):
        self._bus = smbus.SMBus(bus)
        self._i2c_addr = i2c_addr

    @property
    def bus(self):
        return self._bus

    @property
    def i2c_addr(self):
        return self._i2c_addr

    def _to_int(self, data):
        """
        Assumes that data is in big endian format: [msb, ..., lsb]
        """
        b = ''.join(chr(i) for i in data)
        r = struct.unpack('>i', b)
        return r[0]

    def _to_uint(self, data):
        """
        Assumes that data is in big endian format: [msb, ..., lsb]
        """
        b = ''.join(chr(i) for i in data)
        r = struct.unpack('>I', b)
        return r[0]

    def _to_short(self, data):
        """
        Assumes that data is in big endian format: [msb, ..., lsb]
        """
        b = ''.join(chr(i) for i in data)
        r = struct.unpack('>h', b)
        return r[0]

    def _to_ushort(self, data):
        """
        Assumes that data is in big endian format: [msb, ..., lsb]
        """
        b = ''.join(chr(i) for i in data)
        r = struct.unpack('>H', b)
        return r[0]

    def _to_float(self, data):
        """
        Assumes that data is in big endian format: [msb, ..., lsb]
        """
        b = ''.join(chr(i) for i in data)
        r = struct.unpack('>f', b)
        return r[0]

    def _to_double(self, data):
        """
        Assumes that data is in big endian format: [msb, ..., lsb]
        """
        b = ''.join(chr(i) for i in data)
        r = struct.unpack('>d', b)
        return r[0]

    def write_byte(self, reg):
        try:
            self._bus.write_byte(self._i2c_addr, reg)
            return True
        except IOError:
            return False

    def write_word(self, reg, val):
        try:
            self._bus.write_word_data(self._i2c_addr, reg, val)
            return True
        except IOError:
            return False

    def read_byte(self, reg):
        try:
            return self._bus.read_byte_data(self._i2c_addr, reg)
        except IOError:
            return None

    def read_bytes(self, reg, byte_count):
        try:
            return self._bus.read_i2c_block_data(self._i2c_addr, reg, byte_count)
        except IOError:
            return None

    def read_int32(self, reg):
        data = self.read_bytes(reg, 4)
        if data is not None:
            return self._to_int(data)
        else:
            return None

    def read_uint32(self, reg):
        data = self.read_bytes(reg, 4)
        if data is not None:
            return self._to_uint(data)
        else:
            return None

    def read_int16(self, reg):
        data = self.read_bytes(reg, 2)
        if data is not None:
            return self._to_short(data)
        else:
            return None

    def read_uint16(self, reg):
        data = self.read_bytes(reg, 2)
        if data is not None:
            return self._to_ushort(data)
        else:
            return None

    def read_float(self, reg):
        data = self.read_bytes(reg, 4)
        if data is not None:
            return self._to_float(data)
        else:
            return None

    def read_double(self, reg):
        data = self.read_bytes(reg, 8)
        if data is not None:
            return self._to_double(data)
        else:
            return None