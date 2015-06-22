#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       22.06.2015

"""

from xwot.model import Model
from xwot.model import BaseModel
from xwot.model import Sensor as XWOTSensor
from xwot.model import Context as XWOTContext


class WaterDispenser(XWOTContext, BaseModel):

    __mutable_props__ = ['name', 'streetAddress', 'roomAddress', 'postalCode', 'addressLocality']
    __expose__ = __mutable_props__ + ['description', 'valve', 'sensor']

    def __init__(self, name, street_address, postal_code, address_locality, room_address):
        super(WaterDispenser, self).__init__()
        self._dic = {
            'name': name,
            'street_address': street_address,
            'postal_code': postal_code,
            'address_locality': address_locality,
            'room_address': room_address
        }

        self.add_type('http://xwot.lexruee.ch/vocab/core-ext#WaterDispenser')
        self.add_link('valve')
        self.add_link('sensor')

    @property
    def name(self):
        return self._dic['name']

    @property
    def description(self):
        return "Hi there my name is %s. I'm a water dispenser and currently present in room %s at the location: %s, %s, %s" % \
               (self.name, self.roomAddress, self.streetAddress, self.addressLocality, self.postalCode)

    @property
    def switch(self):
        return '/waterdispenser/valve'

    @property
    def sensor(self):
        return '/waterdispenser/sensor'

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


from xwot.i2c.adapter import WaterDispenserAdapter


class Valve(XWOTContext, Model):

    __mutable_props__ = ['name', 'state']
    __expose__ = __mutable_props__ + ['description']

    def __init__(self, name, adapter=WaterDispenserAdapter()):
        super(Valve, self).__init__()

        self._dic = {
            'name': name
        }
        self._adapter = adapter
        self.add_type('http://xwot.lexruee.ch/vocab/core-ext#Valve')

    @property
    def description(self):
        return "A valve that can be used for opening or closing the water supply of this water dispenser."

    @property
    def state(self):
        return self._adapter.solenoid_valve_state

    @property
    def name(self):
        return self._dic['name']

    def handle_update(self, dic):
        if dic.get('state') == 'closed':
            self._adapter.close_solenoid_valve()

        if dic.get('state') == 'open':
            self._adapter.open_solenoid_valve()

        self._dic['name'] = str(dic.get('name', self._dic['name']))


class Sensor(XWOTSensor, Model):

    __expose__ = ['name', 'unit', 'measures', 'description', 'measurement', 'symbol']

    def __init__(self, adapter=WaterDispenserAdapter()):
        super(Sensor, self).__init__()
        self._adapter = adapter
        self.add_type('http://xwot.lexruee.ch/vocab/core-ext#SoilMoistureSensor')

    @property
    def name(self):
        return 'Soil moisture Sensor'

    @property
    def unit(self):
        return 'Percentage'

    @property
    def symbol(self):
        return '%'

    @property
    def description(self):
        return 'A sensor that measures the soil moisture.'

    @property
    def measures(self):
        return 'Soil moisture'

    @property
    def measurement(self):
        return self._adapter.soil_moisture

    def handle_update(self, dic):
        pass