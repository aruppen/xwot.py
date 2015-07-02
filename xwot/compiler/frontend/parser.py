#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       12.04.2015

"""

import xml.etree.ElementTree as ET

import node


class Parser(object):

    def parse(self, xwot_file):
        tree = ET.parse(xwot_file)
        root = tree.getroot()
        parse_tree = TreeWalker.walk(root)
        return parse_tree

    def parse_str(self, xml):
        tree = ET.fromstring(xml)
        root = tree.getroot()
        parse_tree = TreeWalker.walk(root)
        return parse_tree


class TreeWalker(object):

    class NodeHelper:

        # parsing actions
        @classmethod
        def create_vnode(cls, clazz):
            """
            Creates a virtual entity node.
            :param clazz:
            :return:
            """
            def create_vnode(node, dict_attr):
                uri = dict_attr['uri']
                name = dict_attr['name']
                return clazz(name, uri, dict_attr)

            return create_vnode


        @classmethod
        def create_pnode(cls, clazz):
            """
            Creates a physical entity node.
            :param clazz:
            :return:
            """
            def create_node(node, dict_attr):
                if 'name' in dict_attr:
                    name = dict_attr['name']
                else:
                    name = 'RootResource'
                return clazz(name, dict_attr)

            return create_node


    # mapped namespaces / namespace lookup table
    NAMESPACE = {
        'http://www.omg.org/XMI': 'xmi',
        'http://www.w3.org/2001/XMLSchema-instance': 'xsi',
        'http://diuf.unifr.ch/softeng': 'xwot'
    }



    # parsing action table
    ACTION = {
        'xwot:ActuatorResource': NodeHelper.create_vnode(node.ActuatorResource),
        'xwot:SensorResource': NodeHelper.create_vnode(node.SensorResource),
        'xwot:DeviceResource': NodeHelper.create_vnode(node.DeviceResource),
        'xwot:ContextResource': NodeHelper.create_vnode(node.ContextResource),
        'xwot:TagResource': NodeHelper.create_vnode(node.TagResource),
        'xwot:ServiceResource': NodeHelper.create_vnode(node.ServiceResource),
        'xwot:Resource': NodeHelper.create_vnode(node.Resource),
        'xwot:PublisherResource': NodeHelper.create_vnode(node.PublisherResource),

        'xwot:Actuator': NodeHelper.create_pnode(node.Actuator),
        'xwot:Sensor': NodeHelper.create_pnode(node.Sensor),
        'xwot:Device': NodeHelper.create_pnode(node.Device),
        'xwot:Tag': NodeHelper.create_pnode(node.Tag),

        'xwot:Entity': NodeHelper.create_pnode(node.Entity)
    }


    @classmethod
    def _resolve_namespace(cls, uri):
        """
        Resolves the uri to a namespace.
        :param uri:
        :return:
        """
        return TreeWalker.NAMESPACE[uri] if uri in TreeWalker.NAMESPACE else uri


    @classmethod
    def _parse_ns(cls, tag):
        """
        Parses the ns prefix of a tag or attr key.
        :param tag:
        :return:
        """
        if tag[0] == '{':
            index = tag.index('}')
            ns = tag[1:index]
            name = tag[index+1:]
            return TreeWalker._resolve_namespace(ns) + ':' + name
        return tag


    @classmethod
    def _parse_attrs(cls, node):
        """
        Parse attributes of a node and returns a hash with resolved namespaces.
        :param node:
        :return:
        """
        pairs = map(lambda (key, value): (TreeWalker._parse_ns(key), value), node.attrib.items())
        return dict(pairs)


    @classmethod
    def walk(cls, node):
        root_node = TreeWalker._create_node(node)
        for child in node:
            child_node = TreeWalker.walk(child)
            root_node.add_child(child_node)

        return root_node


    @classmethod
    def _create_node(cls, node):
        dict_attr = TreeWalker._parse_attrs(node)

        if 'xsi:type' in dict_attr:
            node_type = dict_attr['xsi:type']
        else:
            node_type = TreeWalker._parse_ns(node.tag)
        parse_action = TreeWalker.ACTION[node_type]

        return parse_action(node, dict_attr)
