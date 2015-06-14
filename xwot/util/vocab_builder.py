#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

import inspect


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

    def __init__(self, documentation, classes, routes):
        self._documentation = documentation
        self._classes = classes
        self._routes = routes


    def _handle_type(self, obj):
        if isinstance(obj, basestring):
            return obj
        elif inspect.isclass(obj):
            return "vocab:%s" % obj.__name__
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
        property_def = None

        if iri:
            type = '@id'
            property_def = {
                    '@id': iri,
                    '@type': type
            }
        else:
            iri = ("vocab:%s/%s" % (klass.__name__, property.name))
            type = ''
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

    def output(self):
        context = self.BASE_CONTEXT
        context['vocab'] = self._documentation.get('vocab', '')
        vocab = {
            '@context': context,
            '@type': 'ApiDocumentation',
            '@id': self._documentation.get('id', ''),
            ("%s" % self.HYDRA_TITLE): self._documentation.get('title', ''),
            ("%s" % self.HYDRA_DESCRIPTION): self._documentation.get('description', ''),
            ("%s" % self.HYDRA_ENTRYPOINT): self._documentation.get('entrypoint', '')
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
            for operation_key in klass.description.get('operation', []):
                if operation_key in self._routes:
                    options = self._routes[operation_key]
                    operation = self._create_operation(operation_key, options)
                    class_operations.append(operation)
                else:
                    print("WARNING: operation %s was not annotated!" % operation_key)

            supported_classes.append({
                '@id': ("vocab:%s" % py_class.__name__),
                '@type': self.HYDRA_CLASS,
                ("%s" % self.HYDRA_TITLE): klass.description.get('title', None),
                ("%s" % self.HYDRA_DESCRIPTION): klass.description.get('description', None),
                ("%s" % self.SUPPORTED_PROPERTY): supported_properties,
                ("%s" % self.SUPPORTED_OPERATION): class_operations
            })

        class_contexts = {}
        for py_class, klass in self._classes.items():
            key = py_class.__name__ + '.jsonld'
            _context = {
                    'vocab': self._documentation.get('vocab', ''),
                    'hydra': self.HYDRA,
                    ("%s" % py_class.__name__): "vocab:%s" % py_class.__name__
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
