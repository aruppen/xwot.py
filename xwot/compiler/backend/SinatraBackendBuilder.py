#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       25.04.2015

"""

from helper import OutputPrinter
from xwot.compiler.frontend import visitor


class SinatraBackendBuilder(visitor.BaseVisitor):

    def __init__(self):
        visitor.BaseVisitor.__init__(self)
        self._out = OutputPrinter()

    def before(self):
        self._out.code([
            '#',
            '# Generated by xwot compiler.',
            '#',
            '# Sinatra xwot application.',
            '#',
            '',
            "require 'sinatra'",
            '',
            'class App < Sinatra::Application',
            '',
            'end'
        ], ["xwot", "app"])

    def after(self):
        self._out.code([
            "require_relative '%s'" % node.name() for node in self._nodes
        ], ["xwot", "app"])

        self._out.code([
            '#',
            '# Generated by xwot compiler.',
            '#',
            '# Sinatra xwot application.',
            '#',
            '',
            "require 'sinatra/base'",
            "require './xwot/app'",
            '',
            "App::run!",
        ], ["runserver"])

    def before_resource(self, node):
        self._out.code([
            '#',
            '# Generated by xwot compiler.',
            '#',
            "# Type:       %s" % node.type(),
            "# Resource:   %s" % node.name(),
            "# Path:       %s" % node.fullpath(),
            '#',
            '',
            "require 'sinatra'",
            '',
            'class App < Sinatra::Application'
        ], ["xwot", node.name()])

    def after_resource(self, node):
        self._out.code([
            'end',
        ], ["xwot", node.name()])

    def handle_entity(self, node):
        self.before_resource(node)
        self._out.code([
            self._out.indent([
                "get '/' do ",
                self._out.indent([
                    '"Hello World at: %s"' % node.fullpath()
                ]),
                'end'
            ]),
        ], ["xwot", "RootResource" ])
        self.after_resource(node)

    def handle_resource(self, node):
        for method in ['get', 'post', 'put', 'delete']:
            self._out.code([
                self._out.indent([
                    '#',
                    "# %s '%s'" % (method.upper(), node.fullpath()),
                    '#',
                    "%s '%s' do " % (method, node.fullpath()),
                        self._out.indent([
                            '"Hello World at: %s"' % node.fullpath()
                        ]),
                    'end'
                ]),
            ], [ "xwot", node.name() ])

    def handle_device_resource(self, node):
        for method in ['get', 'post', 'put', 'delete']:
            self._out.code([
                self._out.indent([
                    '#',
                    "# %s '%s'" % (method.upper(), node.fullpath()),
                    '#',
                    "%s '%s' do " % (method, node.fullpath()),
                        self._out.indent([
                            '"Hello World at: %s"' % node.fullpath()
                        ]),
                    'end'
                ]),
            ], [ "xwot", node.name() ])

    def handle_sensor_resource(self, node):
        for method in ['get', 'post', 'put', 'delete']:
            self._out.code([
                self._out.indent([
                    '#',
                    "# %s '%s'" % (method.upper(), node.fullpath()),
                    '#',
                    "%s '%s' do " % (method, node.fullpath()),
                        self._out.indent([
                            '"Hello World at: %s"' % node.fullpath()
                        ]),
                    'end'
                ]),
            ], [ "xwot", node.name() ])

    def handle_tag_resource(self, node):
        for method in ['get', 'post', 'put', 'delete']:
            self._out.code([
                self._out.indent([
                    '#',
                    "# %s '%s'" % (method.upper(), node.fullpath()),
                    '#',
                    "%s '%s' do " % (method, node.fullpath()),
                        self._out.indent([
                            '"Hello World at: %s"' % node.fullpath()
                        ]),
                    'end'
                ]),
            ], [ "xwot", node.name() ])

    def handle_context_resource(self, node):
        for method in ['get', 'post', 'put', 'delete']:
            self._out.code([
                self._out.indent([
                    '#',
                    "# %s '%s'" % (method.upper(), node.fullpath()),
                    '#',
                    "%s '%s' do " % (method, node.fullpath()),
                        self._out.indent([
                            '"Hello World at: %s"' % node.fullpath()
                        ]),
                    'end'
                ]),
            ], [ "xwot", node.name() ])

    def handle_service_resource(self, node):
        for method in ['get', 'post', 'put', 'delete']:
            self._out.code([
                self._out.indent([
                    '#',
                    "# %s '%s'" % (method.upper(), node.fullpath()),
                    '#',
                    "%s '%s' do " % (method, node.fullpath()),
                        self._out.indent([
                            '"Hello World at: %s"' % node.fullpath()
                        ]),
                    'end'
                ]),
            ], [ "xwot", node.name() ])

    def handle_actuator_resource(self, node):
        for method in ['get', 'post', 'put', 'delete']:
            self._out.code([
                self._out.indent([
                    '#',
                    "# %s '%s'" % (method.upper(), node.fullpath()),
                    '#',
                    "%s '%s' do " % (method, node.fullpath()),
                        self._out.indent([
                            '"Hello World at: %s"' % node.fullpath()
                        ]),
                    'end'
                ]),
            ], [ "xwot", node.name() ])

    def handle_publisher_resource(self, node):
        for method in ['get', 'post', 'put', 'delete']:
            self._out.code([
                self._out.indent([
                    '#',
                    "# %s '%s'" % (method.upper(), node.fullpath()),
                    '#',
                    "%s '%s' do " % (method, node.fullpath()),
                        self._out.indent([
                            '"Hello World at: %s"' % node.fullpath()
                        ]),
                    'end'
                ]),
            ], [ "xwot", node.name() ])

    def output(self):
        # get all created files
        files = self._out.flush()
        new_files_dic = {}

        for file_name, code in files.items():
            # append to each file its correct file extension
            new_files_dic[file_name + ".rb"] = code

        return new_files_dic