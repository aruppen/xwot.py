#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""


class Owl(object):
    NOTHING = "http://www.w3.org/2002/07/owl#Nothing"

    @classmethod
    def Nothing(cls):
        return cls.NOTHING


class Xsd(object):

    XSD_BOOLEAN = "http://www.w3.org/2001/XMLSchema#boolean"
    XSD_STRING = "http://www.w3.org/2001/XMLSchema#string"
    XSD_DATE_TIME = "http://www.w3.org/2001/XMLSchema#dateTime"

    @classmethod
    def string(cls):
        return cls.XSD_STRING

    @classmethod
    def boolean(cls):
        return cls.XSD_BOOLEAN

    @classmethod
    def datetime(cls):
        return cls.XSD_DATE_TIME


class Hydra(object):

    RDF_PROPERTY = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'
    HYDRA = "http://www.w3.org/ns/hydra/core#"
    HYDRA_COLLECTION = "http://www.w3.org/ns/hydra/core#Collection"
    HYDRA_LINK = "http://www.w3.org/ns/hydra/core#Link"
    HYDRA_TITLE = 'http://www.w3.org/ns/hydra/core#title'
    HYDRA_DESCRIPTION = 'http://www.w3.org/ns/hydra/core#description'
    HYDRA_CLASS = 'http://www.w3.org/ns/hydra/core#Class'
    HYDRA_OPERATION = 'http://www.w3.org/ns/hydra/core#Operation'

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


class SchemaOrg(object):

    SCHEMA_ORG_DESCRIPTION = "http://schema.org/description"
    SCHEMA_ORG_NAME = "http://schema.org/name"
    SCHEMA_ORG_EMAIL = "http://schema.org/email"
    SCHEMA_ORG_PERSON = "http://schema.org/Person"

    @classmethod
    def description(cls):
        return cls.SCHEMA_ORG_DESCRIPTION

    @classmethod
    def name(cls):
        return cls.SCHEMA_ORG_NAME

    @classmethod
    def email(cls):
        return cls.SCHEMA_ORG_EMAIL

    @classmethod
    def Person(cls):
        return cls.SCHEMA_ORG_PERSON