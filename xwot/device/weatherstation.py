# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       23.06.2015

"""

from xwot.model import Model
from xwot.model import BaseModel
from xwot.model import Device as XWOTDevice
from xwot.model import Sensor as XWOTSensor
from xwot.model import Collection


class WeatherStation(XWOTDevice, BaseModel):
    __mutable_props__ = ['name', 'streetAddress', 'roomAddress', 'postalCode', 'addressLocality']
    __expose__ = __mutable_props__ + ['description', 'sensors']

    def __init__(self, name, street_address, postal_code, address_locality, room_address):
        super(WeatherStation, self).__init__()
        self._dic = {
            'name': name,
            'streetAddress': street_address,
            'postalCode': postal_code,
            'addressLocality': address_locality,
            'roomAddress': room_address
        }

        self.add_type('http://xwot.lexruee.ch/vocab/core-ext#WeatherStation')
        self.add_link('sensors')


    @property
    def name(self):
        return self._dic['name']

    @property
    def description(self):
        return "Hi there my name is %s. I'm a weather station and currently present in room %s at the location: %s, %s, %s" % \
               (self.name, self.roomAddress, self.streetAddress, self.addressLocality, self.postalCode)

    @property
    def sensors(self):
        return '/weatherstation/sensors'

    @property
    def streetAddress(self):
        return self._dic['streetAddress']

    @property
    def postalCode(self):
        return self._dic['postalCode']

    @property
    def addressLocality(self):
        return self._dic['addressLocality']

    @property
    def roomAddress(self):
        return self._dic['roomAddress']


class Sensor(XWOTSensor, Model):
    __expose__ = ['name', 'unit', 'measures', 'description', 'measurement', 'symbol', 'waterdispenser',
                  'back_link1', 'back_link2']

    def __init__(self, name, unit, symbol, description, measures, type_iri, adapter, adapter_measurement_fun, id):
        super(Sensor, self).__init__()
        self._name = name
        self._id = id
        self._unit = unit
        self._symbol = symbol
        self._description = description
        self._measures = measures
        self._adapter = adapter
        self.add_type(type_iri)
        self._adapter_measurement_fun = adapter_measurement_fun
        self.add_link('back_link1')
        self.add_link('back_link2')

    @property
    def id(self):
        return self._id

    @property
    def back_link1(self):
        return '/weatherstation/sensors'

    @property
    def back_link2(self):
        return '/weatherstation'

    @property
    def name(self):
        return self._name

    @property
    def unit(self):
        return self._unit

    @property
    def symbol(self):
        return self._symbol

    @property
    def description(self):
        return self._description

    @property
    def measures(self):
        return self._measures

    @property
    def measurement(self):
        val = self._adapter_measurement_fun(self._adapter)
        return round(val, 2)

    def handle_update(self, dic):
        pass


from xwot.i2c.adapter import WeatherstationAdapter


def create_sensors():
    adapter = WeatherstationAdapter()

    _sensors = {
        'temperature_1': Sensor(id='temperature1', name='Temperature sensor 1', unit='Celsius', symbol='°C',
                                measures='Temperature',
                                description='A temperature sensor of this weather station.',
                                adapter=adapter, adapter_measurement_fun=lambda a: a.temperature_1,
                                type_iri='http://xwot.lexruee.ch/vocab/core-ext#TemperatureSensor'),

        'temperature_2': Sensor(id='temperature2', name='Temperature sensor 2', unit='Celsius', symbol='°C',
                                measures='Temperature',
                                description='A temperature sensor of this weather station.',
                                adapter=adapter, adapter_measurement_fun=lambda a: a.temperature_2,
                                type_iri='http://xwot.lexruee.ch/vocab/core-ext#TemperatureSensor'),

        'pressure': Sensor(id='pressure', name='Pressure sensor', unit='Pascal', symbol='pa', measures='Pressure',
                           description='A pressure sensor of this weather station.',
                           adapter=adapter, adapter_measurement_fun=lambda a: a.pressure,
                           type_iri='http://xwot.lexruee.ch/vocab/core-ext#PressureSensor'),

        'humidity': Sensor(id='humidity', name='Humidity sensor', unit='Percentage', symbol='%',
                           measures='Humidity',
                           description='A humidity sensor of this weather station.',
                           adapter=adapter, adapter_measurement_fun=lambda a: a.humidity,
                           type_iri='http://xwot.lexruee.ch/vocab/core-ext#HumiditySensor'),

        'altitude': Sensor(id='altitude', name='Altitude sensor', unit='Meters', symbol='m', measures='Altitude',
                           description='An altitude sensor of this weather station.',
                           adapter=adapter, adapter_measurement_fun=lambda a: a.altitude,
                           type_iri='http://xwot.lexruee.ch/vocab/core-ext#AltitudeSensor'),

        'illuminance': Sensor(id='illuminance', name='Illuminance sensor', unit='Lux', symbol='lx',
                              measures='Illuminance',
                              description='An illuminance sensor of this weather station.',
                              adapter=adapter, adapter_measurement_fun=lambda a: a.illuminance,
                              type_iri='http://xwot.lexruee.ch/vocab/core-ext#IlluminanceSensor'),

        'color': Sensor(id='color', name='Color sensor', unit='Kelvin', symbol='k', measures='Temperature',
                        description='A color sensor of this weather station.',
                        adapter=adapter, adapter_measurement_fun=lambda a: a.color_temperature,
                        type_iri='http://xwot.lexruee.ch/vocab/core-ext#TemperatureSensor')
    }

    return _sensors


class SensorCollection(Collection, Model):

    __expose__ = ['back_link']

    def __init__(self, sensors):
        super(SensorCollection, self).__init__()
        self._sensors = sensors
        self.add_link('back_link')


    @property
    def members(self):
        return self._sensors

    @property
    def back_link(self):
        return '/weatherstation'

    def handle_update(self, dic):
        pass
