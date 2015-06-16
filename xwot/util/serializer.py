#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

import json
import dicttoxml
from xml.dom.minidom import parseString


class Visitor(object):

    def _is_builtin(self, obj):
        return obj.__class__.__module__ == '__builtin__'

    def _is_not_builtin(self, obj):
        return self._is_builtin(obj) is False

    def visit(self, obj):
        # check the type of the object obj and call the corresponding handler method
        if type(obj) is list:
            self.visit_list(obj)

        elif type(obj) is dict:
            self.visit_dict(obj)

        elif type(obj) is float:
            self.visit_float(obj)

        elif type(obj) is int:
            self.visit_int(obj)

        elif type(obj) is str:
            self.visit_str(obj)

        elif type(obj) is bool:
            self.visit_bool(obj)

        elif type(obj) is type(None):  # Is the simplest way to get NoneType. Otherwise use 'from types import NoneType'
            self.visit_none(obj)

        elif self._is_not_builtin(obj):  # check if obj is a user defined type
            self.visit_user_object(obj)
        else:
            raise NotImplementedError

    def visit_none(self, val):
        raise NotImplementedError

    def visit_bool(self, val):
        raise NotImplementedError

    def visit_int(self, val):
        raise NotImplementedError

    def visit_float(self, val):
        raise NotImplementedError

    def visit_str(self, val):
        raise NotImplementedError

    def visit_dict(self, dic):
        # example for traversing
        # for item_key, item_obj in dic.items():
        #     self.handle(item_obj)
        raise NotImplementedError

    def visit_list(self, val):
        # example for traversing
        # for index, item in enumerate(val):
        #     self.handle(item)
        raise NotImplementedError

    def visit_tuple(self, val):
        # example for traversing
        # for index, item in enumerate(val):
        #     self.handle(item)
        raise NotImplementedError

    def visit_user_object(self, obj):
        # example for traversing
        # for key, new_obj in vars(obj).iteritems():
        #     self.handle(new_obj)
        raise NotImplementedError


def pretty_json(dic):
    json_doc = json.dumps(dic, indent=4, sort_keys=True, separators=(',', ': '))
    return json_doc


class Serializer(object):

    def serialize(self, obj):
        raise NotImplementedError


class DictionarySerializer(Visitor, Serializer):
    """
    The dictionary serializer serializes built-in types and user defined types into a dictionary.
    """

    def __init__(self, ignore_hidden=True):
        self._output_stack = None
        self._current_key = None
        self._hook_methods = {}
        self._ignore_hidden = ignore_hidden

    def _set_initial_state(self):
        self._output_stack = [('root', {})]
        self._current_key = 'root'

    def _call_hook(self, method_name, args):
        if method_name in self._hook_methods:
            hook_method = self._hook_methods[method_name]
            return hook_method(args)

    def hook_in(self, visit_method, hook_method=None):
        hook_method = hook_method or (lambda x: x)
        self._hook_methods[visit_method] = hook_method

    def serialize(self, obj):
        """
        Serializes a user define type to a dictionary.

        :param obj
        :return dict
        """

        self._set_initial_state()
        self.visit(obj)
        out = self._get_output()
        return out

    def _get_output(self):
        key, _output = self._output_stack[0]
        output = _output[self._current_key]
        return output

    def visit_none(self, val):
        self.visit_primitives(val)

    def visit_bool(self, val):
        self.visit_primitives(val)

    def visit_int(self, val):
        self.visit_primitives(val)

    def visit_float(self, val):
        self.visit_primitives(val)

    def visit_str(self, val):
        self.visit_primitives(val)

    def visit_primitives(self, val):
        _, output = self._output_stack[-1]
        new_val = self._call_hook('visit_primitives', (self._current_key, val))

        if new_val is not None:
            val = new_val

        output[self._current_key] = val

    def visit_list(self, val):
        self._call_hook('visit_list', (self._current_key, val))
        self._save_current_state(self._current_key)
        for index, item in enumerate(val):
            self._current_key = index
            self.visit(item)

        key, pairs = self._output_stack.pop()
        new_list = map(lambda (k, v): v, pairs.items())
        self._output_stack.append((key, new_list))

        self._restore_state()

    def visit_tuple(self, val):
        self._call_hook('visit_tuple', (self._current_key, val))
        self._save_current_state(self._current_key)
        for index, item in enumerate(val):
            self._current_key = index
            self.visit(item)

        key, pairs = self._output_stack.pop()
        new_list = map(lambda (k, v): v, pairs.items())
        self._output_stack.append((key, new_list))

        self._restore_state()

    def visit_dict(self, val):
        self._call_hook('visit_dict', (self._current_key, val))
        self._save_current_state(self._current_key)
        for item_key, item_value in val.items():
            self._current_key = item_key
            self.visit(item_value)

        self._restore_state()

    def visit_user_object(self, obj):
        is_embedded = self._current_key != 'root'  # if the current key is not root then it's a embedded object
        self._save_current_state(self._current_key)

        user_object_dic = vars(obj)
        self._call_hook('visit_user_object', (self._current_key, obj, user_object_dic, is_embedded))
        for key, value in user_object_dic.iteritems():

            if str(key).startswith('_') is False or self._ignore_hidden is False:
                self._current_key = key
                self.visit(value)

        self._restore_state()

    def _save_current_state(self, prop):
        self._output_stack.append((prop, {}))

    def _restore_state(self):
        prev_key, prev_output = self._output_stack.pop()
        self._current_key, output = self._output_stack[-1]
        output[prev_key] = prev_output


class JSONSerializer(Serializer):
    """
    The json serializer serializes a dictionary, list or a user defined type to json.
    """

    def __init__(self):
        self._ds = DictionarySerializer()

    def serialize(self, obj):
        """
        :param obj:
        :return: json string
        """

        out = self._ds.serialize(obj)
        json_str = pretty_json(out)
        return json_str


class JSONLDSerializer(Serializer):
    """
    The jsonld serializer serializes a dictionary, list or a user defined type to jsonld.
    """

    class Mapping(object):

        def __init__(self, key, type, id, context, is_iri, embed):
            self._id = id
            self._key = key
            self._type = type
            self._context = context
            self._is_iri = is_iri
            self._embed = embed

        @property
        def embed(self):
            return self._embed

        @property
        def is_iri(self):
            return self._is_iri

        @property
        def context(self):
            return self._context

        @property
        def id(self):
            return self._id

        @property
        def type(self):
            return self._type

        @property
        def key(self):
            return self._key

    def __init__(self):
        self._ds = DictionarySerializer()
        self._js = JSONSerializer()
        self._mappings = {}
        self._ds.hook_in('visit_user_object', self._hook_method_object)
        self._ds.hook_in('visit_dic', self._hook_method_dic)
        self._ds.hook_in('visit_primitives', self._hook_method_primitives)

    def map(self, mapping):
        """
        Maps user defined types and properties to @id, @type and @context properties.

        Example:
        obj.map(mapping={
            User: {
                '@type': 'Person',
                '@id', 'id', # valid property of the User object
                '@context': 'http://schema.org/',
                'embed': False
            },
            'url': {
                'is_iri': True
            }
        })
        :param mapping:
        :return:
        """

        mapping = mapping or {}
        for key, mapping_for_key in mapping.items():
            _type = mapping_for_key.get('@type', False)
            _id = mapping_for_key.get('@id', False)
            _is_iri = mapping_for_key.get('is_iri', False)
            _context = mapping_for_key.get('@context', False)
            _embed = mapping_for_key.get('embed', False)
            self._mappings[key] = self.Mapping(key=key, type=_type, id=_id, context=_context, is_iri=_is_iri,
                                               embed=_embed)

    def _hook_method_primitives(self, args):
        key, val = args
        if key in self._mappings:
            mapping = self._mappings[key]
            if mapping.is_iri:
                return {'@id': val}

        return None

    def _hook_method_dic(self, args):
        key, dic = args
        if key in self._mappings:
            mapping = self._mappings[key]
            if mapping.type is not False:
                dic['@type'] = mapping.type

            if mapping.id is not False:
                dic['@id'] = mapping.id

            if mapping.context is not False:
                dic['@context'] = mapping.context

    def _hook_method_object(self, args):
        key, obj, dic, is_embedded = args
        py_class = obj.__class__

        if py_class in self._mappings:
            mapping = self._mappings[py_class]

            if mapping.type is not False:
                dic['@type'] = mapping.type

            if mapping.id is not False and hasattr(obj, mapping.id):
                dic['@id'] = getattr(obj, mapping.id)

            if mapping.context is not False:
                dic['@context'] = mapping.context

            # check if we should embed this object
            if mapping.embed is False and is_embedded is True:
                # if not then we need to delete all properties
                for key, item in dic.items():
                    if key not in ['@context', '@id', '@type']:  # do not delete ['@context', '@id', '@type'] props
                        del dic[key]

    def serialize(self, obj, id=False, type=False, context=False):
        """
        Serializes the object obj and sets the top level jsonld '@id', '@type' and '@context' properties.
        If the default values are used then the corresponding properties are not set.

        :param obj:
        :param id: jsonld top level @id
        :param type: jsonld top level @type
        :param context: jsonld top level @context
        :return: jsonld string
        """

        dic = self._ds.serialize(obj)

        if context is not False:
            dic['@context'] = context

        if id is not False:
            dic['@id'] = id

        if type is not False:
            dic['@type'] = type

        json_doc = self._js.serialize(dic)
        return json_doc


class XMLSerializer(Serializer):
    """
    The xml serializer serializes a dictionary, list or a user defined type to xml.
    """

    def __init__(self):
        self._ds = DictionarySerializer()

    def serialize(self, obj, root=None, pretty=True):
        """
        Serialize the object 'obj' and uses the value of 'root' as the name of the root element.
        The pretty options pretty prints the xml output.

        :param obj:
        :param root:
        :param pretty:
        :return: xml string
        """

        if root is None:
            root = obj.__class__.__name__.lower()
        out = self._ds.serialize(obj)

        xml_str = dicttoxml.dicttoxml(out, custom_root=root)

        if pretty:
            xml_str = parseString(xml_str).toprettyxml()
        return xml_str


class HTMLSerializer(Serializer):
    """
    The html serializer serializes a dictionary, list or a user defined type to html.
    """

    def __init__(self):
        self._ds = DictionarySerializer()
        self._output = None
        self._current_key = None
        self._set_initial_state()

    def _set_initial_state(self):
        self._output = []
        
    def _visit(self, value):
        if type(value) is dict:
            self._visit_dic(value)
        elif type(value) is list:
            self._visit_list(value)
        elif type(value) in [str, int, float, bool, type(None)]:
            self._visit_literal(value)

    def _visit_dic(self, dic):
        if self._current_key is not None:
            self._output.append("<strong>%s</strong>" % self._current_key)

        self._output.append('<ul>')
        prev_key = self._current_key
        for key, value in dic.items():
            self._current_key = key
            self._output.append('<li>')
            self._visit(value)
            self._output.append('</li>')

        self._output.append('</ul>')
        self._current_key = prev_key

    def _visit_list(self, value):
        if self._current_key is not None:
            self._output.append("<strong>%s</strong>" % self._current_key)

        self._output.append('<ul>')
        prev_key = self._current_key
        for key, item in enumerate(value):
            self._current_key = str(prev_key) + ("[%s]" % key)
            self._output.append('<li>')
            self._visit(item)
            self._output.append('</li>')

        self._output.append('</ul>')
        self._current_key = prev_key

    def _visit_literal(self, value):
        value = str(value)
        if len(value) > 0 and value[0] == '/':
            self._output.append("<a href=\"%s\">" % value)
            self._output.append(str(self._current_key))
            self._output.append('</a>')
        else:
            self._output.append(str(self._current_key))
            self._output.append(': ')
            self._output.append(value)

    def serialize(self, obj, title=None):
        """
        Serialize a user defined type, list or dictionary to html.
        The title properties specifies the title of the produced html page.

        :param obj:
        :param title:
        :return:
        """

        self._set_initial_state()
        dic = self._ds.serialize(obj)
        self._visit(dic)

        if title is None:
            title = obj.__class__.__name__

        _start = ['<html>', '<head>',
                  "<title> %s </title>" % title,
                  '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/1.12.2/semantic.css" type="text/css" >',
                  '</head>', '<body>']

        _scripts = ['<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.js"> </script>',
                    '<script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/1.12.2/semantic.js"> </script>']

        _end = _scripts + ['</body>', '</html>']

        _body = ['<h1>', title, '</h1>'] + self._output

        html_list = _start + _body + _end
        html_list = map(str, html_list)
        return "".join(html_list)


class ContentTypeSerializer(Serializer):

    def __init__(self, default='application/json'):
        self._serializers = {
            'application/ld+json': JSONLDSerializer(),
            'application/xml': XMLSerializer(),
            'application/json': JSONSerializer(),
            'text/html': HTMLSerializer(),
            'text/plain': HTMLSerializer()
        }

        if default in self._serializers:
            self._default = default

    def register_serializer(self, content_type, serializer):
        self._serializers[content_type] = serializer

    def unregister_serializer(self, content_type):
        if content_type in self._serializers:
            del self._serializers[content_type]

    def serialize(self, obj, content_type=None):
        if content_type in self._serializers:
            serializer = self._serializers[content_type]
        else:
            serializer = self._serializers[self._default]

        return serializer.serialize(obj)

#
# Some helper functions
#

# global serializer variable
SERIALIZER = ContentTypeSerializer()


def register_serializer(content_type, serializer):
    """
    Associates a serializer to the provided cotent_type and registers it to the global serializer().
    :param content_type:
    :param serializer:
    :return:
    """
    SERIALIZER.register_serializer(content_type=content_type, serializer=serializer)


def unregister_serializer(content_type):
    """
    Removes a serializer from the global serializer.
    :param content_type:
    :return:
    """
    SERIALIZER.unregister_serializer(content_type=content_type)


def serialize(obj, content_type='application/json'):
    """
    Serialize an object based on the provided content type.
    If the correspond serializer is not present the default value of content_type is used.
    :param obj:
    :param content_type:
    :return:
    """

    doc = SERIALIZER.serialize(obj=obj, content_type=content_type)
    return doc
