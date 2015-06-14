# encoding: utf8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       15.03.2015

"""

import util


class Plant(object):

    OPEN_SOLENOID_VALVE = 0x01
    CLOSE_SOLENOID_VALVE = 0x02

    READ_SOIL_MOISTURE = 0x09
    READ_SOLENOID_VALVE_STATE = 0x0A

    def __init__(self, bus=1, i2c_addr=0x04):
        self._adapter = util.I2CAdapter(bus=bus, i2c_addr=i2c_addr)

    @property
    def soil_moisture(self):
        return self._adapter.read_float(self.READ_SOIL_MOISTURE)

    @property
    def solenoid_valve_state(self):
        state = self._adapter.read_byte(self.READ_SOLENOID_VALVE_STATE)
        if state == 1:
            return "open"
        elif state == 0:
            return "closed"
        else:
            return None

    def open_solenoid_valve(self):
        self._adapter.write_byte(self.OPEN_SOLENOID_VALVE)

    def close_solenoid_valve(self):
        self._adapter.write_byte(self.CLOSE_SOLENOID_VALVE)