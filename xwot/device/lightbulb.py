#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       22.06.2015

"""

from xwot.model import Context as XWOTContext
from xwot.model import Sensor as XWOTSensor
from xwot.model import Model
from xwot.model import BaseModel
import time


class LightBulb(XWOTContext, BaseModel):

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
        return "Hi there my name is %s. I'm a light bulb and currently present in room %s at the location: %s, %s, %s" % \
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


from xwot.i2c.adapter import LightBulbAdapter


class Switch(XWOTContext, Model):

    __mutable_props__ = ['name', 'state']
    __expose__ = __mutable_props__ + ['description']

    def __init__(self, name, adapter=LightBulbAdapter()):
        super(Switch, self).__init__()

        self._dic = {
            'name': name
        }
        self._adapter = adapter
        self.add_type('http://xwot.lexruee.ch/vocab/core-ext#Switch')

    @property
    def description(self):
        return "A switch to turn off or on this light bulb."

    @property
    def state(self):
        time.sleep(0.5)
        return self._adapter.state

    @property
    def name(self):
        return self._dic['name']

    def handle_update(self, dic):
        if dic.get('state') == 'off':
            self._adapter.switch_off()

        if dic.get('state') == 'on':
            self._adapter.switch_on()

        self._dic['name'] = str(dic.get('name', self._dic['name']))


class Sensor(XWOTSensor, Model):

    __expose__ = ['name', 'unit', 'measures', 'description', 'measurement', 'symbol']

    def __init__(self, adapter=LightBulbAdapter()):
        super(Sensor, self).__init__()
        self._adapter = adapter
        self.add_type('http://xwot.lexruee.ch/vocab/core-ext#IlluminanceSensor')

    @property
    def name(self):
        return 'Illuminance sensor'

    @property
    def unit(self):
        return 'Lux'

    @property
    def description(self):
        return 'A sensor that measures the illuminance of this light bulb.'

    @property
    def measures(self):
        return 'Illuminance'

    @property
    def measurement(self):
        return self._adapter.illuminance

    @property
    def symbol(self):
        return 'lx'

    def handle_update(self, dic):
        pass
