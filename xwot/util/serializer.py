#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

import dicttoxml
from xml.dom.minidom import parseString
from xwot.util import pretty_json


class Serializer(object):

    def __init__(self, annotator):
        self._annotator = annotator
        self._serializers = {
            'application/ld+json': JSONLDSerializer(self._annotator),
            'application/xml': XMLSerializer(self._annotator),
            'application/json': JSONLDSerializer(self._annotator),
            'text/html': HTMLSerializer(self._annotator),
            'text/plain': HTMLSerializer(self._annotator)
        }

    def serialize(self, object, content_type=None, url=''):
        if content_type in self._serializers:
            serializer = self._serializers[content_type]

        else:
            serializer = self._serializers['application/ld+json']

        return serializer.serialize(object, url)


class JSONLDSerializer(object):

    def __init__(self, annotator):
        self._annotator = annotator

    def build_dic(self, object, url=''):
        klass = object.__class__
        annotations = self._annotator.get_class_annotations(klass)

        output = {
            '@id': '/',
            '@context': "%s/contexts/%s.jsonld" % (url, klass.__name__),
            '@type': klass.__name__
        }

        if annotations:
            for prop_name, prop_options in annotations.exposed_properties:
                prop_value = getattr(object, prop_name)
                output[prop_name] = prop_value

        return output

    def serialize(self, object, url=''):
        output = self.build_dic(object)
        return pretty_json(output)


class XMLSerializer(object):

    def __init__(self, annotator):
        self._annotator = annotator

    def serialize(self, object, url=''):
        klass = object.__class__
        annotations = self._annotator.get_class_annotations(klass)

        output = {
            '@id': '/',
            '@context': "%s/contexts/%s.jsonld" % (url, klass.__name__),
            '@type': klass.__name__
        }

        if annotations:
            for prop_name, prop_options in annotations.exposed_properties:
                prop_value = getattr(object, prop_name)
                output[prop_name] = prop_value

        xml = dicttoxml.dicttoxml(output, custom_root=klass.__name__)
        return parseString(xml).toprettyxml()


def indent(items):
    return ["\t %s" % item for item in items]

def flatten(alist):
    return [item for sublist in alist for item in sublist]


class HTMLSerializer(object):

    def __init__(self, annotator):
        self._annotator = annotator
        self._JSONLDSerializer = JSONLDSerializer(annotator)

    def serialize(self, object, url=''):
        klass = object.__class__
        annotations = self._annotator.get_class_annotations(klass)

        links = []
        props = []

        if annotations:
            for prop_name, prop_options in annotations.exposed_properties:
                prop_value = getattr(object, prop_name)
                if prop_value[0] == '/':
                    links.append([
                        '<li>',
                        '<strong><a href="' + prop_value + '">' + prop_name + '</a></strong>',
                        '</li>'
                    ])
                else:
                    props.append([
                        "<strong> %s: </strong> %s" % (prop_name, prop_value),
                        '<br/>'
                    ])

        output = flatten([
            ['<html>'],
            ['<head>',
                '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/1.12.2/semantic.css" type="text/css" >'
            '</head>'],
            ['<body>'],
                ['<h1>', klass.__name__, '</h1>'],
                ['<h2>', 'Properties', '</h2>'],
                ['<ul>'] + flatten(props) + ['</ul>'],
                ['<h2>', 'Links', '</h2>'],
                ['<ul>'] + flatten(links) + ['</ul>'],
                ['<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.js"> </script>'],
                ['<script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/1.12.2/semantic.js"> </script>'],
            ['</body>'],
            ['</html>']
        ])
        print (output)
        return "\n".join(output)