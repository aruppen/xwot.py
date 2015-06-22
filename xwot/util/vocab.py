#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""


class Iri(object):

    __iri__ = True

    def __init__(self, iri):
        self._iri = iri

    def __str__(self):
        return self._iri


class NullIri(Iri):

    def __init__(self):
        super(NullIri, self).__init__(None)



class Owl(object):
    NOTHING = Iri("http://www.w3.org/2002/07/owl#Nothing")

    @classmethod
    def Nothing(cls):
        return cls.NOTHING


class Xsd(object):

    BOOLEAN = Iri("http://www.w3.org/2001/XMLSchema#boolean")
    STRING = Iri("http://www.w3.org/2001/XMLSchema#string")
    DATE_TIME = Iri("http://www.w3.org/2001/XMLSchema#dateTime")
    INTEGER = Iri("http://www.w3.org/2001/XMLSchema#integer")
    FLOAT = Iri("http://www.w3.org/2001/XMLSchema#float")
    DOUBLE = Iri("http://www.w3.org/2001/XMLSchema#double")
    LONG = Iri("http://www.w3.org/2001/XMLSchema#long")

    @classmethod
    def string(cls):
        return cls.STRING

    @classmethod
    def boolean(cls):
        return cls.BOOLEAN

    @classmethod
    def datetime(cls):
        return cls.DATE_TIME

    @classmethod
    def integer(cls):
        return cls.INTEGER

    @classmethod
    def double(cls):
        return cls.DOUBLE

    @classmethod
    def float(cls):
        return cls.FLOAT

    @classmethod
    def long(cls):
        return cls.LONG


class Hydra(object):

    RDF_PROPERTY = Iri('http://www.w3.org/1999/02/22-rdf-syntax-ns#Property')
    HYDRA = Iri("http://www.w3.org/ns/hydra/core#")
    HYDRA_COLLECTION = Iri("http://www.w3.org/ns/hydra/core#Collection")
    HYDRA_LINK = Iri("http://www.w3.org/ns/hydra/core#Link")
    HYDRA_TITLE = Iri('http://www.w3.org/ns/hydra/core#title')
    HYDRA_DESCRIPTION = Iri('http://www.w3.org/ns/hydra/core#description')
    HYDRA_CLASS = Iri('http://www.w3.org/ns/hydra/core#Class')
    HYDRA_OPERATION = Iri('http://www.w3.org/ns/hydra/core#Operation')
    HYDRA_MEMBER = Iri('http://www.w3.org/ns/hydra/core#member')

    @classmethod
    def core(cls):
        return cls.HYDRA

    @classmethod
    def Collection(cls):
        return cls.HYDRA_COLLECTION

    @classmethod
    def Link(cls):
        return cls.HYDRA_LINK

    @classmethod
    def Class(cls):
        return cls.HYDRA_CLASS

    @classmethod
    def Property(cls):
        return cls.RDF_PROPERTY

    @classmethod
    def member(cls):
        return cls.HYDRA_MEMBER


class SchemaOrg(object):

    DESCRIPTION = Iri("http://schema.org/description")
    NAME = Iri("http://schema.org/name")
    EMAIL = Iri("http://schema.org/email")
    URL = Iri("http://schema.org/url")
    PERSON = Iri("http://schema.org/Person")
    TEXT = Iri("http://schema.org/Text")
    ACCESS_CODE = Iri("http://schema.org/accessCode")


    @classmethod
    def Text(cls):
        return cls.TEXT

    @classmethod
    def accessCode(cls):
        return cls.ACCESS_CODE

    @classmethod
    def description(cls):
        return cls.DESCRIPTION

    @classmethod
    def name(cls):
        return cls.NAME

    @classmethod
    def email(cls):
        return cls.EMAIL

    @classmethod
    def url(cls):
        return cls.URL

    @classmethod
    def Person(cls):
        return cls.PERSON


class Xwot(object):

    ENTITY = Iri("http://xwot.lexruee.ch/vocab/core#Entity")
    CONTEXT = Iri("http://xwot.lexruee.ch/vocab/core#Context")
    SENSOR = Iri("http://xwot.lexruee.ch/vocab/core#Sensor")
    SERVICE = Iri("http://xwot.lexruee.ch/vocab/core#Service")
    ACTUATOR = Iri("http://xwot.lexruee.ch/vocab/core#Actuator")
    TAG = Iri("http://xwot.lexruee.ch/vocab/core#Tag")
    PUBLISHER = Iri("http://xwot.lexruee.ch/vocab/core#Publisher")
    DEVICE = Iri("http://xwot.lexruee.ch/vocab/core#Device")
    RESOURCE = Iri("http://xwot.lexruee.ch/vocab/core#Resource")
    DESCRIPTION = Iri("http://xwot.lexruee.ch/vocab/core#Description")

    @classmethod
    def Description(cls):
        return cls.DESCRIPTION

    @classmethod
    def Entity(cls):
        return cls.ENTITY

    @classmethod
    def Context(cls):
        return cls.CONTEXT

    @classmethod
    def Sensor(cls):
        return cls.SENSOR

    @classmethod
    def Actuator(cls):
        return cls.ACTUATOR

    @classmethod
    def Service(cls):
        return cls.SERVICE

    @classmethod
    def Publisher(cls):
        return cls.PUBLISHER

    @classmethod
    def Device(cls):
        return cls.DEVICE

    @classmethod
    def Resource(cls):
        return cls.RESOURCE

    @classmethod
    def Tag(cls):
        return cls.TAG