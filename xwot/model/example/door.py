# encoding: utf8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       19.05.2015

"""

from xwot.model.example import util


class Door(object):

    UNLOCK_DOOR = 0x01
    LOCK_DOOR = 0x02
    OPEN_DOOR = 0x03
    CLOSE_DOOR = 0x04

    READ_LOCK_STATE = 0x09
    READ_CLOSE_STATE = 0x0A

    def __init__(self, bus=1, i2c_addr=0x04):
        self._adapter = util.I2CAdapter(bus=bus, i2c_addr=i2c_addr)

    def unlock(self):
        return self._adapter.write_byte(self.UNLOCK_DOOR)

    def lock(self):
        return self._adapter.write_byte(self.LOCK_DOOR)

    def open(self):
        return self._adapter.write_byte(self.OPEN_DOOR)

    def close(self):
        return self._adapter.write_byte(self.CLOSE_DOOR)

    @property
    def lock_state(self):
        state = self._adapter.read_byte(self.READ_LOCK_STATE)
        if state == 1:
            return "locked"
        elif state == 0:
            return "unlocked"
        else:
            return None

    @property
    def close_state(self):
        state = self._adapter.read_byte(self.READ_CLOSE_STATE)
        if state == 1:
            return "open"
        elif state == 0:
            return "closed"
        elif state == 2:
            return "transition"
        else:
            return None