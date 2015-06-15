#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

import inspect
import json
from vocab import Hydra


class Collection(object):

    def __init__(self, members=None):
        if members is None:
            self._members = []
        else:
            self._members = members

    @property
    def members(self):
        return self._members

    def get(self, id):
        return self._members[id]

    @classmethod
    def annotate(self, annotator):
        # annotate Collection class
        collection = annotator.klass(Collection)
        collection.describe(title='Collection', description='A Collection', iri=Hydra.Collection())
        collection.expose('members', description="The members of this collection.", iri=Hydra.member(), writeonly=False,
                          readonly=False)


class VocabBuilder(object):

    BASE_CONTEXT = {
        "hydra": "http://www.w3.org/ns/hydra/core#",
        "ApiDocumentation": "hydra:ApiDocumentation",
        "property": {
            "@id": "hydra:property",
            "@type": "@id"
        },
        "readonly": "hydra:readonly",
        "writeonly": "hydra:writeonly",
        "supportedClass": "hydra:supportedClass",
        "supportedProperty": "hydra:supportedProperty",
        "supportedOperation": "hydra:supportedOperation",
        "method": "hydra:method",
        "expects": {
            "@id": "hydra:expects",
            "@type": "@id"
        },
        "returns": {
            "@id": "hydra:returns",
            "@type": "@id"
        },
        "statusCodes": "hydra:statusCodes",
        "code": "hydra:statusCode",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "label": "rdfs:label",
        "description": "rdfs:comment",
        "domain": {
            "@id": "rdfs:domain",
            "@type": "@id"
        },
        "range": {
            "@id": "rdfs:range",
            "@type": "@id"
        },
        "subClassOf": {
            "@id": "rdfs:subClassOf",
            "@type": "@id"
        }
    }

    CONTEXT = '@context'
    ID = '@id'
    TYPE = '@type'

    SUPPORTED_CLASS = 'supportedClass'
    SUPPORTED_OPERATION = 'supportedOperation'
    SUPPORTED_PROPERTY = 'supportedProperty'

    SUBCLASS_OF = 'subClassOf'
    LABEL = 'label'
    DESCRIPTION = 'description'
    PROPERTY = 'property'

    HYDRA_TITLE = 'hydra:title'
    HYDRA_DESCRIPTION = 'hydra:description'
    HYDRA_CLASS = 'hydra:Class'
    HYDRA_OPERATION = 'hydra:Operation'
    HYDRA_ENTRYPOINT = 'hydra:entrypoint'
    HYDRA_LINK = 'hydra:Link'

    RDF_PROPERTY = 'rdf:Property'

    READ_ONLY = 'readonly'
    WRITE_ONLY = 'writeonly'
    REQUIRED = 'required'

    DOMAIN = 'domain'
    RANGE = 'range'
    METHOD = 'method'
    STATUS_CODES = 'statusCodes'
    RETURNS = 'returns'
    EXPECTS = 'expects'

    HYDRA = "http://www.w3.org/ns/hydra/core#"

    HYDRA_RESOURCE = {
        "@id": "http://www.w3.org/ns/hydra/core#Resource",
        "@type": "hydra:Class",
        "hydra:title": "Resource",
        "hydra:description": None,
        "supportedOperation": [],
        "supportedProperty": []
    }

    HYDRA_COLLECTION = {
        "@id": "http://www.w3.org/ns/hydra/core#Collection",
        "@type": "hydra:Class",
        "hydra:title": "Collection",
        "hydra:description": None,
        "supportedOperation": [],
        "supportedProperty": [
            {
                "property": "http://www.w3.org/ns/hydra/core#member",
                "hydra:title": "members",
                "hydra:description": "The members of this collection.",
                "required": None,
                "readonly": False,
                "writeonly": False
            }
        ]
    }

    def __init__(self, annotator):
        self._annotator = annotator
        self._documentation = annotator.get_documentation()
        self._classes = annotator.get_classes()
        self._routes = annotator.get_routes()

    @property
    def annotator(self):
        return self._annotator

    @property
    def documentation(self):
        return self._documentation

    @property
    def routes(self):
        return self._routes

    @property
    def classes(self):
        return self._classes

    def _handle_type(self, obj):
        if isinstance(obj, basestring):
            return obj
        elif inspect.isclass(obj):
            py_class = obj
            klass = self._classes[py_class]
            return klass.iri
        else:
            return obj

    def _create_operation(self, route_name, operation):
        returns = self._handle_type(operation.returns)
        expects = self._handle_type(operation.expects)
        operation_dic = {
                '@id': ("_:%s" % route_name),
                '@type': ("%s" % self.HYDRA_OPERATION),
                ("%s" % self.METHOD): operation.method,
                ("%s" % self.DESCRIPTION): operation.description,
                ("%s" % self.LABEL): operation.description,
                ("%s" % self.EXPECTS): expects,
                ("%s" % self.RETURNS): returns,
                ("%s" % self.STATUS_CODES): operation.status_codes
            }
        return operation_dic

    def _create_supported_property(self, klass, property, operations):
        iri = property.iri
        type = property.type
        property_def = None

        if iri is not None:
            property_def = iri
            if type is not None:
                property_def = {
                    '@id': iri,
                    '@type': type
                }

        else:
            iri = ("vocab:%s/%s" % (klass.__name__, property.name))
            if type is None:
                if len(operations):
                    type = self.HYDRA_LINK
                else:
                    type = self.RDF_PROPERTY

            property_def = {
                    '@id': iri,
                    '@type': type,
                    ("%s" % self.LABEL): property.name,
                    ("%s" % self.DOMAIN): ("vocab:%s" % klass.__name__),
                    ("%s" % self.DESCRIPTION): property.description,
                    ("%s" % self.RANGE): property.range,
                    ("%s" % self.SUPPORTED_OPERATION): operations
            }

        prop_dic = {
                ("%s" % self.PROPERTY): property_def,
                ("%s" % self.HYDRA_TITLE): property.name,
                ("%s" % self.HYDRA_DESCRIPTION): property.description,
                ("%s" % self.REQUIRED): property.required,
                ("%s" % self.READ_ONLY): property.readonly,
                ("%s" % self.WRITE_ONLY): property.writeonly
            }

        return prop_dic

    def _build_vocab(self):
        context = self.BASE_CONTEXT
        context['vocab'] = self._documentation.vocab_url
        _id = ''

        if self._documentation.iri is not None:
            _id = self._documentation.iri

        vocab = {
            '@context': context,
            '@type': 'ApiDocumentation',
            '@id': _id,
            ("%s" % self.HYDRA_TITLE): self._documentation.title,
            ("%s" % self.HYDRA_DESCRIPTION): self._documentation.description,
            ("%s" % self.HYDRA_ENTRYPOINT): self._documentation.entrypoint
        }

        supported_classes = []
        vocab['supportedClass'] = supported_classes
        for py_class, klass in self._classes.items():
            supported_properties = []

            # add operations to properties
            for prop_name, property in klass.exposed_properties:
                supported_property_operations = []
                for operation_key in property.operations:
                    if operation_key in self._routes:
                        operation = self._routes[operation_key]
                        operation_dic = self._create_operation(operation_key, operation)
                        supported_property_operations.append(operation_dic)

                supported_property = self._create_supported_property(py_class, property, supported_property_operations)
                supported_properties.append(supported_property)

            # add operations to classes
            class_operations = []
            for operation_key in klass.operations:
                if operation_key in self._routes:
                    options = self._routes[operation_key]
                    operation = self._create_operation(operation_key, options)
                    class_operations.append(operation)
                else:
                    print("WARNING: operation %s was not annotated!" % operation_key)

            supported_classes.append({
                '@id': klass.iri,
                '@type': self.HYDRA_CLASS,
                ("%s" % self.HYDRA_TITLE): klass.title,
                ("%s" % self.HYDRA_DESCRIPTION): klass.description,
                ("%s" % self.SUPPORTED_PROPERTY): supported_properties,
                ("%s" % self.SUPPORTED_OPERATION): class_operations
            })

        class_contexts = {}
        for py_class, klass in self._classes.items():
            key = py_class.__name__ + '.jsonld'

            _context = {
                    'vocab': self._documentation.vocab_url,
                    'hydra': self.HYDRA,
                    ("%s" % py_class.__name__): klass.iri
            }
            class_contexts[key] = {
                '@context': _context
            }

            for prop_name, property in klass.exposed_properties:
                iri = property.iri
                if iri is None:
                    iri = "vocab:%s/%s" % (py_class.__name__, prop_name)

                if len(property.operations):
                    _context[prop_name] = {
                        '@id': iri,
                        '@type': '@id'
                    }
                elif property.type:
                    _context[prop_name] = {
                        '@id': iri,
                        '@type': property.type
                    }
                else:
                    _context[prop_name] = iri
                # todo: add support for type coercion
                #{
                #    '@id': iri,
                #    '@type': '@id'
                #}

        return vocab, class_contexts

    def output(self):
        doc, class_contexts = self._build_vocab()
        json_doc = json.dumps(doc, indent=4, sort_keys=True, separators=(',', ': '))

        class_contexts_json_doc = {}
        for filename, context in class_contexts.items():
            json_context_doc = json.dumps(context, indent=4, sort_keys=True, separators=(',', ': '))
            class_contexts_json_doc[filename] = json_context_doc

        return json_doc, class_contexts_json_doc
