#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

__author__ = 'Alexander Rüedlinger'

import os
import socket
from xwot.compiler.frontend.processing import JSONLDDescriptionBuilder
import xmltodict
import json


def local_ip():
    # source: http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    return [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s
            in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


def create_description(xwot_file, site='', base=None):
    description_builder = JSONLDDescriptionBuilder()
    out = description_builder.build(xml_file=xwot_file, site=site, base=base)
    return out


def dir_path(file):
    return os.path.dirname(os.path.realpath(file))


def parent_dir_path(file):
    return os.path.dirname(dir_path(file))



CONTENT_TYPES = {
    'application/xml': xmltodict.parse,
    'application/json': json.loads,
    'application/ld+json': json.loads
}


def deserialize(data, content_type):
    print(content_type)
    print(data)
    if content_type in CONTENT_TYPES and data:
        deserializer = CONTENT_TYPES[content_type]
        res = deserializer(data)
        return res
    return {}