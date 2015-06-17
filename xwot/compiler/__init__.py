#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       25.04.2015

"""

__author__ = 'Alexander Rüedlinger'

import sys
import os
import os.path

from backend.FlaskBackendBuilder import FlaskBackendBuilder
from backend.FlaskHydraBackendBuilder import FlaskHydraBackendBuilder
from backend.SinatraBackendBuilder import SinatraBackendBuilder
from backend.ExpressBackendBuilder import ExpressBackendBuilder
from frontend.parser import Parser
from frontend.processing import JSONLDDescriptionPrinter
from frontend.processing import TreeCleaner


class Compiler(object):

    BACKENDS = {
        'flask': FlaskBackendBuilder,
        'flask-hydra': FlaskHydraBackendBuilder,
        'express': ExpressBackendBuilder,
        'sinatra': SinatraBackendBuilder
    }

    def __init__(self, input_file, output_dir, platform):
        self._xwot_file = input_file
        self._output_dir = output_dir
        self._platform = platform

    def _parse_input_file(self, file_path):
        # parse xml xwot file
        parser = Parser()
        root_node = parser.parse(file_path)
        return root_node

    def _check_input_file(self, file_path):
        # check if input file exists
        if not os.path.exists(file_path):
            print "Input file does not exist: %s " % file_path
            sys.exit(1)

    def _clean_tree(self, root_node):
        cleaner = TreeCleaner()
        root_node.accept(cleaner)

    def _build_backend(self, root_node):
         # select backend builder
        backend_builder = self.BACKENDS[self._platform]
        builder = backend_builder()

        # build backend
        root_node.accept(builder)

        for file_name, code in builder.output().items():
            file_name = os.path.join(self._output_dir, file_name)
            path = os.path.dirname(file_name)

            # if path does not exit
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(file_name))

            with open(file_name, 'w+') as f:
                f.write(code)

    def _create_description(self, root_node):
        file_name = os.path.join(self._output_dir, 'description.jsonld')
        description_printer = JSONLDDescriptionPrinter('')
        root_node.accept(description_printer)
        out = description_printer.output()

        with open(file_name, 'w+') as f:
            f.write(out)

    def _create_xml_xwot_file(self, xml_filepath):
        xml_str = open(xml_filepath, "r").read()
        file_name = os.path.join(self._output_dir, 'device.xwot')

        with open(file_name, 'w+') as f:
            f.write(xml_str)

    def compile(self):
        self._check_input_file(self._xwot_file)
        root_node = self._parse_input_file(self._xwot_file)

        self._clean_tree(root_node)
        self._build_backend(root_node)
        self._create_description(root_node)
        self._create_xml_xwot_file(self._xwot_file)

