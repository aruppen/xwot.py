# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

from xwot.util.serializer import pretty_json
import logging

logger = logging.getLogger('hydra vocab builder')


class HydraApiDocBuilder(object):
    CONTEXT = {
        "vocab": "missing",
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

    def __init__(self, annotator):
        self._annotator = annotator
        self._supported_classes = {}

    def _handle_type(self, obj):
        if obj is None:
            return None
        elif type(obj) is str:
            return obj
        else:
            return "vocab:%s" % obj.__name__

    def build(self):
        resources = self._visit_resources()
        api_doc = {
            '@context': self.CONTEXT,
            '@type': 'ApiDocumentation',
            'supportedClass': resources
        }

        js = pretty_json(api_doc)
        with open('test.json', 'w+') as f:
            f.write(js)
        return api_doc

    def _visit_resources(self):
        resources = []

        for resource_key, resource in self._annotator._resources.items():
            routes = self._annotator.get_routes(resource_key)
            props = self._annotator.get_properties(resource_key)
            operations = self._visit_routes(resource, routes)
            properties = self._visit_properties(resource, props)

            resource_dic = {
                '@id': "vocab:%s" % resource.name,
                '@type': 'hydra:Class',
                'label': resource.name,
                'description': resource.description,
                'supportedOperation': operations,
                'supportedProperty': properties
            }

            resources.append(resource_dic)

        return resources

    def _visit_routes(self, resource, routes):
        operations = []
        for route_key, route in routes.items():
            operation = self._create_operation(route_key, route)
            operations.append(operation)

        return operations

    def _create_operation(self, route_key, route):
        route_dic = {
            '@id': "_:%s" % route_key,
            '@type': route.method,
            'label': route.description,
            'description': route.description,
            'expects': self._handle_type(route.expects),
            'returns': self._handle_type(route.returns),
            'statusCodes': route.status_codes
        }
        return route_dic

    def _visit_properties(self, resource, props):
        properties = []
        for prop_key, prop in props.items():
            prop_def = self._visit_iri(resource, prop)
            prop_dic = {
                'property': prop_def,
                'hydra:title': prop_key,
                'hydra:description': prop.description,
                'required': prop.required,
                'readonly': prop.readonly,
                'writeonly': prop.writeonly
            }
            properties.append(prop_dic)

        return properties

    def _visit_iri(self, resource, prop):
        prop_def = prop.iri
        if len(prop.operations) > 0:  # property is of type hydra:Link
            _routes = self._annotator.get_routes_from_keys(prop.operations)
            operations = [self._create_operation(route.name, route) for route in _routes]
            _first_route = _routes[0]
            _range = self._handle_type(_first_route.returns)

            prop_def = {
                '@id': "vocab:%s/%s" % (resource.name, prop.name),
                '@type': 'hydra:Link',
                'label': prop.name,
                'description': prop.description,
                'domain': "vocab:%s" % resource.name,
                'range': "vocab:%s" % _range,
                'supportedOperation': operations
            }
        elif prop.iri is None:  # need to create a property definition
            prop_def = {
                '@id': "vocab:%s/%s" % (resource.name, prop.name),
                '@type': "rdf:Property",
                'label': prop.name,
                'description': prop.description,
                'domain': "vocab:%s" % resource.name,
                'range': "%s" % prop.range,  # need hint from the api user here...
                'supportedOperation': []

            }
        return prop_def
