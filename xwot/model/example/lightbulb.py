# encoding: utf8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       10.06.2015

"""

from xwot.model.example import util


class LightBulb(object):

    SWITCH_LIGHT_ON = 0x01
    SWITCH_LIGHT_OFF = 0x02
    READ_LIGHT_BULB_STATE = 0x09
    READ_ILLUMINANCE = 0x0A

    def __init__(self, bus=1, i2c_addr=0x04):
        self._adapter = util.I2CAdapter(bus=bus, i2c_addr=i2c_addr)

    def switch_on(self):
        return self._adapter.write_byte(self.SWITCH_LIGHT_ON)

    def switch_off(self):
        return self._adapter.write_byte(self.SWITCH_LIGHT_OFF)

    @property
    def state(self):
        state = self._adapter.read_byte(self.READ_LIGHT_BULB_STATE)
        if state == 1:
            return "on"
        elif state == 0:
            return "off"
        else:
            return None

    @property
    def illuminance(self):
        return self._adapter.read_int32(self.READ_ILLUMINANCE)