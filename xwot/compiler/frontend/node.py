#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       12.04.2015

"""

"""
 Base entities
"""

from visitor import Visitable


class Entity(object, Visitable):

    def __init__(self, name, attributes, uri=''):
        self._name = name
        self._children = []
        self._attributes = attributes
        self._fullpath = '/'
        self._uri = uri

    def add_child(self, node):
        self._children.append(node)

    def children(self):
        return self._children

    def set_children(self, children):
        self._children = children

    def set_uri(self, uri):
        self._uri = uri

    def set_name(self, name):
        self._name = name

    def attributes(self):
        return self._attributes

    def name(self):
        return self._name

    def accept(self, visitor):
        visitor.visit_entity(self)

    def type(self):
        return 'xwot:' + self.__class__.__name__

    def is_virtual(self):
        return True

    def is_physical(self):
        return False

    def fullpath(self):
        return self._fullpath

    def uri(self):
        return self._uri


class PhysicalEntity(Entity):

    def __init__(self, name, attributes):
        super(PhysicalEntity, self).__init__(name, attributes)

    def is_virtual(self):
        return False

    def is_physical(self):
        return True


class VirtualEntity(Entity):

    def __init__(self, name, uri, attributes):
        super(VirtualEntity, self).__init__(name, attributes)
        self._uri = uri

    def uri(self):
        return self._uri

    def is_virtual(self):
        return True

    def is_physical(self):
        return False


"""
 Physical entities
"""


class Device(PhysicalEntity):

    def __init__(self, name, attributes):
        super(Device, self).__init__(name, attributes)

    def accept(self, visitor):
        visitor.visit_device(self)


class Tag(PhysicalEntity):

    def __init__(self, name, attributes):
        super(Tag, self).__init__(name, attributes)

    def accept(self, visitor):
        visitor.visit_tag(self)


class Sensor(PhysicalEntity):

    def __init__(self, name, attributes):
        super(Sensor, self).__init__(name, attributes)

    def accept(self, visitor):
        visitor.visit_sensor(self)


class Actuator(PhysicalEntity):

    def __init__(self, name, attributes):
        super(Actuator, self).__init__(name, attributes)

    def accept(self, visitor):
        visitor.visit_actuator(self)

"""
 Virtual entities
"""


class DeviceResource(VirtualEntity):

    def __init__(self, name, uri, attributes):
        super(DeviceResource, self).__init__(name, uri, attributes)

    def accept(self, visitor):
        visitor.visit_device_resource(self)


class ServiceResource(VirtualEntity):

    def __init__(self, name, uri, attributes):
        super(ServiceResource, self).__init__(name, uri, attributes)

    def accept(self, visitor):
        visitor.visit_service_resource(self)


class ActuatorResource(VirtualEntity):

    def __init__(self, name, uri, attributes):
        super(ActuatorResource, self).__init__(name, uri, attributes)

    def accept(self, visitor):
        visitor.visit_actuator_resource(self)


class SensorResource(VirtualEntity):

    def __init__(self, name, uri, attributes):
        super(SensorResource, self).__init__(name, uri, attributes)

    def accept(self, visitor):
        visitor.visit_sensor_resource(self)


class TagResource(VirtualEntity):

    def __init__(self, name, uri, attributes):
        super(TagResource, self).__init__(name, uri, attributes)

    def accept(self, visitor):
        visitor.visit_tag_resource(self)


class ContextResource(VirtualEntity):

    def __init__(self, name, uri, attributes):
        super(ContextResource, self).__init__(name, uri, attributes)

    def accept(self, visitor):
        visitor.visit_context_resource(self)


class PublisherResource(VirtualEntity):

    def __init__(self, name, uri, attributes):
        super(PublisherResource, self).__init__(name, uri, attributes)

    def accept(self, visitor):
        visitor.visit_publisher_resource(self)


class Resource(VirtualEntity):

    def __init__(self, name, uri, attributes):
        super(Resource, self).__init__(name, uri, attributes)

    def accept(self, visitor):
        visitor.visit_resource(self)