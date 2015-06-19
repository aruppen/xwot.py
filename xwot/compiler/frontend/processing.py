#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       29.04.2015

"""

import json
from visitor import Visitor
from parser import Parser


class TreeCleaner(Visitor):
    """
    TreeCleaner removes all physical nodes and adds absolute uri to all nodes.
    """

    def __init__(self):
        self._path = ['']

    def path(self):
        return "/".join(self._path)

    def visit_entity(self, node):
        virtual_children = [child for child in node.children() if child.is_virtual()]
        [child.accept(self) for child in virtual_children]
        node.set_children(virtual_children)

    def visit_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath
        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._path.pop()

    def visit_device_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._path.pop()

    def visit_sensor_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._path.pop()

    def visit_service_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

    def visit_actuator_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._path.pop()

    def visit_tag_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._path.pop()

    def visit_context_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._path.pop()

    def visit_publisher_resource(self, node):
        fullpath = self.path() + '/' + node.uri()
        node._fullpath = fullpath

    def visit_device(self, node):
        pass

    def visit_sensor(self, node):
        pass

    def visit_actuator(self, node):
        pass

    def visit_tag(self, node):
        pass


class JSONLDDescriptionPrinter(Visitor):
    """
    JSONLDDescriptionPrinter creates a minimal device description file in the jsonld format.
    """

    CHILDREN = 'knows'
    TYPE = "@type"
    ID = "@id"
    CONTEXT = '@context'

    def __init__(self, site='', base=None):
        self._output = None
        self._current = None
        self._site = self._remove_last_forwardslash(site)
        self._base = base
        self._path = [self._site]

    def _remove_last_forwardslash(self, site):
        _site = site
        if len(site) > 0:
            if site[-1] == '/':
                _site = site[0:-1]

        return _site

    @property
    def site(self):
        return self._site

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, value):
        self._base = value

    @site.setter
    def site(self, value):
        self._site = self._remove_last_forwardslash(value)
        self._path[0] = self._site

    def path(self):
        return "/".join(self._path)

    def visit_entity(self, node):
        self._output = {
            ("%s" % self.ID): '/',
            ("%s" % self.TYPE): 'Description',
            ("%s" % self.CHILDREN): []
        }

        before = self._output
        self._current = self._output[("%s" % self.CHILDREN)]

        [child.accept(self) for child in node.children() if child.is_virtual()]

        # overwrite entity resource and use the first child as root
        # entity resource has always at most one child !!!
        #self._output = self._output[("%s" % self.CHILDREN)][0]  # hack
        self._output[self.CONTEXT] = ["http://xwot.lexruee.ch/contexts/xwot.jsonld"]

    def visit_resource(self, node):
        resource = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'name': node.name(),
            'sameAs': "http://www.productontology.org/id/Web_resource",
            'additionalType': {
                '@id': "http://www.productontology.org/id/Web_resource"
            },
            ("%s" % self.TYPE): 'Resource',
            ("%s" % self.CHILDREN): []
        }

        self._current.append(resource)
        before = self._current
        self._current = resource[("%s" % self.CHILDREN)]
        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._current = before
        self._path.pop()

    def visit_device_resource(self, node):
        device = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'name': node.name(),
            'sameAs': "http://www.productontology.org/id/Computer_apliance",
            'additionalType': {
                '@id': "http://www.productontology.org/id/Computer_appliance"
            },
            ("%s" % self.TYPE): 'Device',
            ("%s" % self.CHILDREN): []
        }

        self._current.append(device)
        before = self._current
        self._current = device[("%s" % self.CHILDREN)]

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._current = before
        self._path.pop()

    def visit_sensor_resource(self, node):
        sensor = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'name': node.name(),
            'sameAs': "http://www.productontology.org/id/Sensor",
            'additionalType': {
                '@id': "http://www.productontology.org/id/Sensor"
            },
            ("%s" % self.TYPE): 'Sensor',
            ("%s" % self.CHILDREN): []
        }
        self._current.append(sensor)

        before = self._current
        self._current = sensor[("%s" % self.CHILDREN)]

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._current = before
        self._path.pop()

    def visit_service_resource(self, node):
        service = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'name': node.name(),
            'sameAs': "http://www.productontology.org/id/Sensor",
            'additionalType': {
                '@id': "http://www.productontology.org/id/Sensor"
            },
            ("%s" % self.TYPE): 'Service'
        }
        self._current.append(service)

    def visit_actuator_resource(self, node):
        actuator = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'name': node.name(),
            ("%s" % self.TYPE): 'Actuator',
            'sameAs': "http://www.productontology.org/id/Actuator",
            'additionalType': {
                '@id': "http://www.productontology.org/id/Actuator"
            },
            ("%s" % self.CHILDREN): []
        }
        self._current.append(actuator)

        before = self._current
        self._current = actuator[("%s" % self.CHILDREN)]

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._current = before
        self._path.pop()

    def visit_tag_resource(self, node):
        tag = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'name': node.name(),
            'sameAs': "http://www.productontology.org/id/Automatic_identification_and_data_capture",
            'additionalType': {
                '@id': "http://www.productontology.org/id/Automatic_identification_and_data_capture"
            },
            ("%s" % self.TYPE): 'Tag',
            ("%s" % self.CHILDREN): []
        }
        self._current.append(tag)

        before = self._current
        self._current = tag[("%s" % self.CHILDREN)]

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._current = before
        self._path.pop()

    def visit_context_resource(self, node):
        context = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'name': node.name(),
            'sameAs': "http://www.productontology.org/id/Scope_(computer_science)",
            'additionalType': {
                '@id': "http://www.productontology.org/id/Scope_(computer_science)"
            },
            ("%s" % self.TYPE): 'Context',
            ("%s" % self.CHILDREN): []
        }
        self._current.append(context)

        before = self._current
        self._current = context[("%s" % self.CHILDREN)]

        self._path.append(node.uri())
        for child in node.children():
            child.accept(self)

        self._current = before
        self._path.pop()

    def visit_publisher_resource(self, node):
        publisher = {
            ("%s" % self.ID): self.path() + '/' + node.uri(),
            'uri': {
                "@id": self.path() + '/' + node.uri()
            },
            'name': node.name(),
            'sameAs': "http://www.productontology.org/id/Publish%E2%80%93subscribe_pattern",
            'additionalType': {
                '@id': "http://www.productontology.org/id/Publish%E2%80%93subscribe_pattern"
            },
            ("%s" % self.TYPE): 'Publisher',
            ("%s" % self.CHILDREN): []
        }
        self._current.append(publisher)

    def visit_device(self, node):
        device = {
            'name': node.name(),
            ("%s" % self.TYPE): 'device',
            ("%s" % self.CHILDREN): []
        }

        self._current.append(device)
        before = self._current
        self._current = device[("%s" % self.CHILDREN)]

        for child in node.children():
            child.accept(self)

        self._current = before

    def visit_sensor(self, node):
        sensor = {
            'name': node.name(),
            ("%s" % self.TYPE): 'sensor'
        }
        self._current.append(sensor)

    def visit_actuator(self, node):
        actuator = {
            'name': node.name(),
            ("%s" % self.TYPE): 'actuator'
        }
        self._current.append(actuator)

    def visit_tag(self, node):
        tag = {
            'name': node.name(),
            ("%s" % self.TYPE): 'tag'
        }
        self._current.append(tag)

    def output(self):
        if self._base is not None:
            self._output[self.CONTEXT].append({
                "@base": self._base
            })

        out = json.dumps(self._output, indent=4, sort_keys=True, separators=(',', ': '))
        return out


class DescriptionBuilder(object):

    def __init__(self, description_printer):
        self._description_printer = description_printer
        self._out = None

    def build(self, xml_file, site='', base=None):
        parser = Parser()
        root_node = parser.parse(xml_file)

        # set properties for creating absolute paths
        self._description_printer.site = site  # uses the site path as prefix for all relative uris
        self._description_printer.base = base  # sets the jsonld @base property in @context

        root_node.accept(self._description_printer)
        self._out = self._description_printer.output()
        return self._out

    def output(self):
        return self._out


class JSONLDDescriptionBuilder(DescriptionBuilder):

    def __init__(self):
        super(JSONLDDescriptionBuilder, self).__init__(JSONLDDescriptionPrinter())
