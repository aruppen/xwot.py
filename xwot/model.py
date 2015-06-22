#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       21.06.2015

"""

import json
import dicttoxml
from xml.dom.minidom import parseString


def pretty_json(dic):
    json_doc = json.dumps(dic, indent=4, sort_keys=True, separators=(',', ': '))
    return json_doc


class Entity(object):
    __type__ = 'xwot:Entity'

    __contexts__ = ['http://xwot.lexruee.ch/contexts/xwot']

    __links__ = []
    __expose__ = []

    def __init__(self):
        self._links = []
        self._types = []
        self._contexts = []
        self._resource_path = '/'

    @property
    def resource_path(self):
        return self._resource_path

    @resource_path.setter
    def resource_path(self, value):
        self._resource_path = value

    @property
    def id(self):
        return ''

    @property
    def type(self):
        return self.__type__

    def add_link(self, name):
        self._links.append(name)

    def add_context(self, context):
        self._contexts += [context]

    def add_type(self, type):
        self._types += [type]

    def _get_exposed_properties(self):
        props = [prop for prop in self.__expose__ if hasattr(self, prop)]
        return props

    def _get_dict(self):
        dic = {}
        for key in self._get_exposed_properties():
            dic[key] = getattr(self, key)
        return dic

    def _enhance_dic(self, dic):
        dic['type'] = self.__type__
        dic['links'] = []

        for link in self._links:
            dic['links'].append(dic[link])
            del dic[link]

        return dic

    def to_json(self):
        dic = self._get_dict()
        dic = self._enhance_dic(dic)
        return pretty_json(dic)

    def to_xml(self):
        dic = self._get_dict()
        dic = self._enhance_dic(dic)
        xml_str = dicttoxml.dicttoxml(dic, custom_root=self.__class__.__name__, attr_type=False)
        xml_str = parseString(xml_str).toprettyxml()
        return xml_str

    def to_dict(self):
        return self._get_dict()

    def to_jsonld(self):
        dic = self._get_dict()
        dic['@id'] = self.resource_path
        dic['@context'] = self.__contexts__ + self._contexts
        dic['@type'] = self.__type__
        dic['additionalType'] = self._types
        dic['links'] = []

        for link in self._links:
            dic['links'].append(dic[link])
            del dic[link]

        return pretty_json(dic)

    def to_html(self):
        return ''

    def _create_path(self, parts, prefix=''):
        new_parts = [prefix]
        for part in parts:
            part = str(part)
            if part[0] == '/':
                part = part[1:]
            if part[-1] == '/':
                part = part[0:-1]
            new_parts.append(part)
        return "/".join(new_parts)


class Resource(Entity):
    __type__ = 'xwot:Resource'


class Collection(Resource):
    __type__ = ['xwot:Resource', 'hydra:Collection']

    @property
    def members(self):
        return []

    def _enhance_dic(self, dic):
        dic['type'] = self.__type__
        dic['additionalType'] = self._types
        dic['members'] = []

        for member in self.members:
            item_link = self._create_path([self.resource_path, member.id])
            item_dic = {
                'type': member.type,
                'link': item_link
            }
            dic['members'].append(item_dic)

        dic['links'] = []
        for link in self._links:
            dic['links'].append(dic[link])
            del dic[link]

        return dic

    def to_jsonld(self):
        dic = self._get_dict()
        dic['@id'] = self.resource_path
        dic['@context'] = self.__contexts__
        dic['@type'] = self.__type__
        dic['additionalType'] = self._types
        dic['members'] = []

        for member in self.members:
            item_link = self._create_path([self.resource_path, member.id])
            item_dic = {
                '@type': member.type,
                '@id': item_link
            }
            dic['members'].append(item_dic)

        dic['links'] = []

        for link in self._links:
            dic['links'].append(dic[link])
            del dic[link]

        return pretty_json(dic)


class Device(Entity):
    __type__ = 'xwot:Device'


class Sensor(Entity):
    __type__ = 'xwot:Sensor'


class Actuator(Entity):
    __type__ = 'xwot:Actuator'


class Context(Entity):
    __type__ = 'xwot:Context'


class Tag(Entity):
    __type__ = 'xwot:Tag'


class Service(Entity):
    __type__ = 'xwot:Service'


class Publisher(Entity):
    __type__ = 'xwot:Publisher'


class Model(object):

    __mutable_props__ = []

    def update(self, dic, content_type):
        if content_type in ['application/json', 'application/ld+json']:
            return self.handle_update(dic)
        elif content_type in ['application/xml']:
            dic = dic.get([self.__class__.__name__], {})
            return self.handle_update(dic)
        else:
            return 400

    def handle_update(self, dic):
        raise NotImplementedError


class BaseModel(Model):

    __mutable_props__ = []

    def __init__(self, dic=None):
        self._dic = dic or {}

    def handle_update(self, dic):
        valid_keys = [key for key in dic.keys() if key in self.__mutable_props__]
        for key in valid_keys:
            self._dic[key] = str(dic[key])

        return 200

