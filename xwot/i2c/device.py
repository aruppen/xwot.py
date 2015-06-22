# encoding: utf8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       19.05.2015

"""


from xwot.i2c.util import Adapter


class Door(object):

    UNLOCK_DOOR = 0x01
    LOCK_DOOR = 0x02
    OPEN_DOOR = 0x03
    CLOSE_DOOR = 0x04

    READ_LOCK_STATE = 0x09
    READ_CLOSE_STATE = 0x0A

    def __init__(self, bus=1, i2c_addr=0x04):
        self._adapter = Adapter(bus=bus, i2c_addr=i2c_addr)

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


class LightBulb(object):

    SWITCH_LIGHT_ON = 0x01
    SWITCH_LIGHT_OFF = 0x02
    READ_LIGHT_BULB_STATE = 0x09
    READ_ILLUMINANCE = 0x0A

    def __init__(self, bus=1, i2c_addr=0x04):
        self._adapter = Adapter(bus=bus, i2c_addr=i2c_addr)

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


class WaterDispenser(object):

    OPEN_SOLENOID_VALVE = 0x01
    CLOSE_SOLENOID_VALVE = 0x02

    READ_SOIL_MOISTURE = 0x09
    READ_SOLENOID_VALVE_STATE = 0x0A

    def __init__(self, bus=1, i2c_addr=0x04):
        self._adapter = Adapter(bus=bus, i2c_addr=i2c_addr)

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
        self._adapter = Adapter(bus=bus, i2c_addr=i2c_addr)

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