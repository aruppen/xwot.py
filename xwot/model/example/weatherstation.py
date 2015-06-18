# encoding: utf8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       9.06.2015

"""

from xwot.model.example import util


class Weatherstation(object):

    READ_TEMPERATURE_1 = 0x01
    READ_TEMPERATURE_2 = 0x02
    READ_PRESSURE = 0x03  # long value
    READ_HUMIDITY = 0x04
    READ_ALTITUDE = 0x05  # long value
    READ_ILLUMINANCE = 0x06  # long value
    READ_COLOR_TEMPERATURE = 0x07
    READ_COLOR_ILLUMINANCE = 0x08

    def __init__(self, bus=1, i2c_addr=0x05):
        self._adapter = util.I2CAdapter(bus=bus, i2c_addr=i2c_addr)

    @property
    def pressure(self):
        return self._adapter.read_int32(self.READ_PRESSURE)

    @property
    def altitude(self):
        return self._adapter.read_int32(self.READ_ALTITUDE)

    @property
    def illuminance(self):
        return self._adapter.read_int32(self.READ_ILLUMINANCE)

    @property
    def humidity(self):
        return self._adapter.read_float(self.READ_HUMIDITY)

    @property
    def temperature_1(self):
        return self._adapter.read_float(self.READ_TEMPERATURE_1)

    @property
    def temperature_2(self):
        return self._adapter.read_float(self.READ_TEMPERATURE_2)

    @property
    def color_temperature(self):
        return self._adapter.read_int32(self.READ_COLOR_TEMPERATURE)

    @property
    def color_illuminance(self):
        return self._adapter.read_int32(self.READ_COLOR_ILLUMINANCE)