#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

__author__ = 'Alexander Rüedlinger'

import json
import socket
from xwot.compiler.frontend.processing import JSONLDDescriptionBuilder


def local_ip():
    # source: http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    return [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s
            in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]


def create_description(xml_file, base=''):
    description_builder = JSONLDDescriptionBuilder()
    out = description_builder.build(xml_file=xml_file, base=base)
    return out


def pretty_json(dic):
    json_doc = json.dumps({}, indent=4, sort_keys=True, separators=(',', ': '))
    return json_doc