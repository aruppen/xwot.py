#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

import dicttoxml
from xml.dom.minidom import parseString
from xwot.util import pretty_json


def _build_rec_dic(klass, object, annotator, url, context):
    output = {}


    for prop_name, prop_options in klass.exposed_properties:
                prop_value = getattr(object, prop_name)
                py_class = prop_value.__class__
                prop_klass = annotator.get_class(py_class)

                if prop_klass is not None:
                    output[prop_name] = _build_rec_dic(prop_klass, object, annotator)



                elif type(prop_value) is list:
                    output[prop_name] = []
                    _set = set()
                    for index, item in enumerate(prop_value):
                        item_py_class = item.__class__
                        item_klass = annotator.get_class(item_py_class)
                        id = index


                        if item_klass is not None:
                            if hasattr(item, 'id'):
                                id = getattr(item, 'id')
                            item_out = {}
                            item_out['@id'] = "%s/%s" % (item_klass.path, id)
                            item_out['@type'] = item_klass.iri

                            if item_klass.embedded:
                                _set.add("%s/contexts/%s.jsonld" % (url, item_py_class.__name__))
                                _item_out = _build_rec_dic(item_klass, item, annotator, url, context)
                                item_out.update(_item_out)
                        else:
                            item_out = item
                        output[prop_name].append(item_out)

                    for i in _set:
                        context.append(i)

                else:
                    output[prop_name] = prop_value.__str__()

                print(output[prop_name])
    return output


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
        py_class = object.__class__
        klass = self._annotator.get_class(py_class)
        context = ["%s/contexts/%s.jsonld" % (url, py_class.__name__)]
        context += klass.extra_context

        output = {
            '@id': '/',
            '@context': context,
            '@type': py_class.__name__
        }

        if klass:
            _out = _build_rec_dic(klass, object, self._annotator, url, context)
            print _out
            output.update(_out)

        return output

    def serialize(self, object, url=''):
        output = self.build_dic(object)
        return pretty_json(output)


class XMLSerializer(object):

    def __init__(self, annotator):
        self._annotator = annotator

    def serialize(self, object, url=''):
        py_class = object.__class__
        klass = self._annotator.get_class(py_class)
        context = ["%s/contexts/%s.jsonld" % (url, py_class.__name__)]
        output = {
            '@id': '/',
            '@context': context,
            '@type': py_class.__name__
        }

        if klass:
            _out = _build_rec_dic(klass, object, self._annotator, url, context)
            output.update(_out)

        xml = dicttoxml.dicttoxml(output, custom_root=py_class.__name__)
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
        py_class = object.__class__
        klass = self._annotator.get_class(py_class)

        links = []
        props = []

        if klass:
            for prop_name, prop_options in klass.exposed_properties:
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
                ['<h1>', py_class.__name__, '</h1>'],
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