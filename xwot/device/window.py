#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       6.07.2015

"""

from xwot.model import Context as XWOTContext
from xwot.model import Device as XWOTDevice
from xwot.model import Model
from xwot.model import BaseModel

from xwot.i2c.adapter import WindowAdapter
from xwot.i2c.adapter import ShutterAdapter


class Window(XWOTDevice, BaseModel):

    __mutable_props__ = ['name', 'streetAddress', 'roomAddress', 'postalCode', 'addressLocality']
    __expose__ = __mutable_props__ + ['description', 'handle', 'lock']

    def __init__(self, name, street_address, postal_code, address_locality, room_address):
        super(Window, self).__init__()
        self._dic = {
            'name': name,
            'streetAddress': street_address,
            'postalCode': postal_code,
            'addressLocality': address_locality,
            'roomAddress': room_address
        }

        self.add_type('xwot-ext:Window')
        self.add_link('handle')
        self.add_link('lock')

    @property
    def resource_path(self):
        return '/window'

    @property
    def name(self):
        return self._dic['name']

    @property
    def description(self):
        return "Hi there my name is %s. I'm a window and currently present in room %s at the location: %s, %s, %s" % \
               (self.name, self.roomAddress, self.streetAddress, self.addressLocality, self.postalCode)

    @property
    def handle(self):
        return '/window/handle'

    @property
    def lock(self):
        return '/window/lock'

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


class Lock(XWOTContext, Model):

    __mutable_props__ = ['name', 'state']
    __expose__ = __mutable_props__ + ['description', 'window']

    def __init__(self, name, adapter=WindowAdapter()):
        super(Lock, self).__init__()

        self._dic = {
            'name': name
        }
        self._adapter = adapter
        self.add_type('xwot-ext:Lock')
        self.add_link('window')

    @property
    def resource_path(self):
        return '/window/lock'

    @property
    def window(self):
        return '/window'

    @property
    def description(self):
        return "A window lock which can be locked and unlocked."

    @property
    def state(self):
        return self._adapter.lock_state

    @property
    def name(self):
        return self._dic['name']

    def handle_update(self, dic):
        if dic.get('state') == 'locked':
            self._adapter.lock()

        if dic.get('state') == 'unlocked':
            self._adapter.unlock()

        self._dic['name'] = str(dic.get('name', self._dic['name']))

        return 200


class Handle(XWOTContext, Model):

    __mutable_props__ = ['name', 'state']
    __expose__ = __mutable_props__ + ['description', 'window']

    def __init__(self, name, adapter=WindowAdapter()):
        super(Handle, self).__init__()

        self._dic = {
            'name': name
        }
        self._adapter = adapter
        self.add_type('xwot-ext:Handle')
        self.add_link('window')

    @property
    def resource_path(self):
        return '/window/handle'

    @property
    def window(self):
        return '/window'

    @property
    def description(self):
        return "A window handle which can be closed and opened."

    @property
    def state(self):
        return self._adapter.close_state

    @property
    def name(self):
        return self._dic['name']

    def handle_update(self, dic):
        if dic.get('state') == 'closed':
            self._adapter.close()

        if dic.get('state') == 'opened':
            self._adapter.open()

        self._dic['name'] = str(dic.get('name', self._dic['name']))

        return 200