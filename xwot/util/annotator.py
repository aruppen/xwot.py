#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

import json

from vocab_builder import VocabBuilder


class Klass(object):

    def __init__(self, klass, mapper):
        self._klass = klass
        self._mapper = mapper
        self._exposed_properties = {}
        self._description = None
        self._operations = []
        self._iri = None
        self._title = None
        self._extra_context = []

    def expose(self, name, title=None, type=None, iri=None, description=None, label=None, domain=None, range=None,
               operations=None, required=None, readonly=None, writeonly=None):

        self._exposed_properties[name] = Property(name=name, title=title, type=type, iri=iri, description=description,
                                                  label=label, domain=domain, range=range, operations=operations,
                                                  required=required, readonly=readonly, writeonly=writeonly)
        return self

    def describe(self, title=None, description=None, iri=None, operations=None):
        self._title = title
        self._description = description
        self._iri = iri
        if operations is not None:
            self._operations = operations
        return self

    def add_context(self, context):
        self._extra_context += [context]

    @property
    def extra_context(self):
        return self._extra_context

    @property
    def description(self):
        return self._description

    @property
    def iri(self):
        return self._iri

    @property
    def title(self):
        return self._title

    @property
    def operations(self):
        return self._operations


    @property
    def exposed_properties(self):
        return self._exposed_properties.items()

    @property
    def mapper(self):
        return self._mapper


class Property(object):

    def __init__(self, name, title, iri, description, type, label, domain, range, operations, required, readonly, writeonly):
        self._name = name
        self._title = title
        self._description = description
        self._type = type
        self._label = label
        self._domain = domain
        self._range = range
        self._iri = iri

        if operations is None:
            self._operations = []
        else:
            self._operations = operations

        self._required = required
        self._readonly = readonly
        self._writeonly = writeonly

    @property
    def iri(self):
        return self._iri

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def writeonly(self):
        return self._writeonly

    @property
    def readonly(self):
        return self._readonly

    @property
    def required(self):
        return self._required

    @property
    def operations(self):
        return self._operations

    @property
    def description(self):
        return self._description

    @property
    def range(self):
        return self._range

    @property
    def domain(self):
        return self._domain

    @property
    def label(self):
        return self._label

    @property
    def description(self):
        return self._description

    @property
    def title(self):
        return self._title


class Operation(object):

    def __init__(self, name, method, description=None, returns=None, status_codes=None, expects=None):
        self._name = name
        self._method = method
        self._description = description
        self._returns = returns

        if status_codes is None:
            self._status_codes = []
        else:
            self._status_codes = status_codes

        self._expects = expects

    @property
    def name(self):
        return self._name

    @property
    def method(self):
        return self._method

    @property
    def description(self):
        return self._description

    @property
    def returns(self):
        return self._returns

    @property
    def status_codes(self):
        return self._status_codes

    @property
    def expects(self):
        return self._expects


class Documentation(object):

    def __init__(self, vocab_url, title=None, description=None, entrypoint=None, iri=None):
        self._title = title
        self._description = description
        self._vocab_url = vocab_url
        self._entrypoint = entrypoint
        self._iri = iri

    @property
    def title(self):
        return self._title

    @property
    def vocab_url(self):
        return self._vocab_url

    @property
    def description(self):
        return self._description

    @property
    def entrypoint(self):
        return self._entrypoint

    @property
    def iri(self):
        return self._iri


class Annotator(object):

    def __init__(self):
        self._classes = {}
        self._routes = {}
        self._documentation = None

    def klass(self, py_class):
        klass = Klass(py_class, self)
        self._classes[py_class] = klass
        return klass

    def documentation(self, vocab_url, title=None, description=None, entrypoint=None):
        self._documentation = Documentation(vocab_url=vocab_url, title=title, description=description,
                                            entrypoint=entrypoint)

    def route(self, name, method, description=None, returns=None, status_codes=None, expects=None):
        self._routes[name] = Operation(name=name, method=method, description=description, returns=returns,
                                       expects=expects, status_codes=status_codes)
        def wrapper(f):
            return f
        return wrapper

    def get_class(self, klass):
        return self._classes.get(klass, None)

    def get_route(self, route):
        return self._routes[route]

    def get_routes(self):
        return self._routes

    def get_classes(self):
        return self._classes

    def get_documentation(self):
        return self._documentation
