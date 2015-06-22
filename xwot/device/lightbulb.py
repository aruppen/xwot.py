#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       22.06.2015

"""

from xwot.model import Context
from xwot.model import Sensor as XWOTSensor
from xwot.model import Model
from xwot.model import BaseModel
import time


class LightBulb(Context, BaseModel):

    __mutable_props__ = ['name', 'streetAddress', 'roomAddress', 'postalCode', 'addressLocality']
    __expose__ = __mutable_props__ + ['description', 'switch', 'sensor']

    def __init__(self, name, street_address, postal_code, address_locality, room_address):
        super(LightBulb, self).__init__()
        self._dic = {
            'name': name,
            'street_address': street_address,
            'postal_code': postal_code,
            'address_locality': address_locality,
            'room_address': room_address
        }

        self.add_type('http://xwot.lexruee.ch/vocab/core-ext#LightBulb')
        self.add_link('switch')
        self.add_link('sensor')

    @property
    def name(self):
        return self._dic['name']

    @property
    def description(self):
        return "This is smart light %s. I am currently present in room %s at the location: %s, %s, %s" % \
               (self.name, self.roomAddress, self.streetAddress, self.addressLocality, self.postalCode)

    @property
    def switch(self):
        return '/lightbulb/switch'

    @property
    def sensor(self):
        return '/lightbulb/sensor'

    @property
    def streetAddress(self):
        return self._dic['street_address']

    @property
    def postalCode(self):
        return self._dic['postal_code']

    @property
    def addressLocality(self):
        return self._dic['address_locality']

    @property
    def roomAddress(self):
        return self._dic['room_address']


from xwot.i2c.device import LightBulb as I2C_LightBulb


class Switch(Context, Model):

    __mutable_props__ = ['name', 'state']
    __expose__ = __mutable_props__ + ['description']

    def __init__(self, name, i2c_light_bulb=I2C_LightBulb()):
        super(Switch, self).__init__()

        self._dic = {
            'name': name
        }
        self._i2c_light_bulb = i2c_light_bulb
        self.add_type('http://xwot.lexruee.ch/vocab/core-ext#Switch')

    @property
    def description(self):
        return "A switch to turn off or on this light bulb."

    @property
    def state(self):
        time.sleep(0.5)
        return self._i2c_light_bulb.state

    @property
    def name(self):
        return self._dic['name']

    def handle_update(self, dic):
        if dic.get('state') == 'off':
            self._i2c_light_bulb.switch_off()

        if dic.get('state') == 'on':
            self._i2c_light_bulb.switch_on()

        self._dic['name'] = str(dic.get('name', self._dic['name']))


class Sensor(XWOTSensor, Model):

    __expose__ = ['name', 'unit', 'measures', 'description', 'measurement']

    def __init__(self, i2c_light_bulb=I2C_LightBulb()):
        super(Sensor, self).__init__()
        self._i2c_light_bulb = i2c_light_bulb
        self.add_type('http://xwot.lexruee.ch/vocab/core-ext#IlluminanceSensor')

    @property
    def name(self):
        return 'Illuminance sensor'

    @property
    def unit(self):
        return 'lx'

    @property
    def description(self):
        return 'An illuminance sensor that measures the illuminance of this light bulb.'

    @property
    def measures(self):
        return 'Illuminance'

    @property
    def measurement(self):
        return self._i2c_light_bulb.illuminance

    def handle_update(self, dic):
        pass
