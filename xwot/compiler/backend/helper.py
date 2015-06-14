#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       3.06.2015

"""

import os


class OutputPrinter(object):
    """
    OutputPribter is used to generate code.
    """

    def __init__(self):
        # a key in the dictionary represents a file name
        # each key is associated with a list of strings
        # the strings are more or less expressions or statements in some programming language
        self._output = {}

    def indent(self, items):
        return "\n".join([("    %s" % item) for item in items])

    def _add_line(self, item, node_name):
        node_name = tuple(node_name)
        if node_name not in self._output:
            self._output[node_name] = []

        self._output[node_name].append(item)
        self._output[node_name].append("\n")

    def code(self, lines, node_name):
        lines.append("")
        [self._add_line(item, node_name) for item in lines]

    def flatten(self, items):
        return [val for sub_list in items for val in sub_list]

    def flush(self):
        dic = {}
        for node_name, lines in self._output.items():
            out = ''
            for line in lines:
                out += line
            simple_node_name = os.path.join(*node_name)
            dic[simple_node_name] = out

        self._output = {}
        return dic
