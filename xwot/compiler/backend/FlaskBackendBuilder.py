# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       25.04.2015

"""

from helper import OutputPrinter
from xwot.compiler.frontend import visitor


class FlaskBackendBuilder(visitor.BaseVisitor):
    def __init__(self):
        visitor.BaseVisitor.__init__(self)
        self._out = OutputPrinter()

    def before(self):
        self._out.code([
                           '#',
                           '# Generated by xwot compiler.',
                           '#',
                           '# Flask xwot application.',
                           '#',
                           '',
                           'import os',
                           'from yadp.device import Description',
                           '',
                           'from xwot.util import local_ip',
                           'from xwot.util import create_description',
                           'from xwot.util.flask import hydra_link',
                           'from xwot.util.annotator import Annotator',
                           'from xwot.util.serializer import Serializer',
                           'from xwot.util import dir_path',
                           'from xwot.util import parent_dir_path',
                           'from xwot.util.hydra import VocabBuilder',
                           '',
                           '# base config',
                           'ip = local_ip()',
                           'port = 5000',
                           'http_addr = "http://%s:%s/" % (ip, port)',
                           'module_dir_path = dir_path(__file__)',
                           'app_dir_path = parent_dir_path(__file__)',
                           'xwot_file = os.path.join(app_dir_path, "device.xwot")',
                           '',
                           'iri = "%s%s" % (http_addr, "vocab")',
                           'vocab_url = iri + "#"',
                           'link = hydra_link(iri)',
                           '',
                           'annotator = Annotator()',
                           'serializer = Serializer(annotator)',
                           'vocab_builder = VocabBuilder(annotator)',
                           '',
                           'jsonld_description_str = create_description(xwot_file=xwot_file, base=http_addr)',
                           'yadp_description = Description(content_type="application/ld+json", content=jsonld_description_str)',
                           '',
                           '',
                           'from flask import Flask',
                           'app = Flask(__name__)',
                           ], ["xwot_device", "__init__"])

    def after(self):
        self._out.code([
                           "import %s" % node.name() for node in self._nodes
                       ], ["xwot_device", "__init__"])

        self._out.code([
                           '#',
                           '# Generated by xwot compiler.',
                           '#',
                           '# Flask xwot application.',
                           '#',
                           '',
                           'import xwot_device',
                           'from xwot_device import app',
                           '',
                           'import yadp',
                           'yadp.debug()',
                           '',
                           'from yadp import service',
                           'from yadp.device import Device',
                           '',
                           "device = Device(urn='urn:xwot:device', url=xwot_device.http_addr, descriptions=[xwot_device.yadp_description])",
                           '',
                           'service = service()',
                           'yadp.debug()',
                           'service.register(device=device, passive=True)',
                           '',
                           "",
                           "if __name__ == '__main__':",
                           self._out.indent([
                               "app.run(host='0.0.0.0', port=xwot_device.port, debug=True)",
                               "service.shutdown()"
                           ])
                       ], ['runserver'])

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
                           'from flask import request',
                           'from xwot_device import app',
                           ''
                       ], ["xwot_device", node.name()])

    def handle_entity(self, node):
        self._out.code([
                           '#',
                           '# Generated by compiler compiler.',
                           '#',
                           "# Type:       %s" % node.type(),
                           "# Resource:   %s" % node.name(),
                           "# Path:       %s" % node.fullpath(),
                           '#',
                           '',
                           'from flask import Response',
                           'import xwot_device',
                           'from xwot_device import app',
                           '',
                           '',
                           "@app.route('/')",
                           'def home():',
                           self._out.indent([
                               'return Response(response=xwot_device.jsonld_description_str, status=200, content_type="application/ld+json")'
                           ])
                       ], ["xwot_device", "RootResource"])

    def handle_resource(self, node):
        for method in ['GET', 'POST', 'PUT', 'DELETE']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s():" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_device", node.name()])

    def handle_device_resource(self, node):
        for method in ['GET', 'POST', 'PUT']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s():" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_device", node.name()])

    def handle_sensor_resource(self, node):
        for method in ['GET']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s():" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_device", node.name()])

    def handle_tag_resource(self, node):
        for method in ['GET']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s():" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_device", node.name()])

    def handle_context_resource(self, node):
        for method in ['GET', 'POST', 'PUT']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s():" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_device", node.name()])

    def handle_service_resource(self, node):
        for method in ['GET', 'POST', 'PUT', 'DELETE']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s():" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_device", node.name()])

    def handle_actuator_resource(self, node):
        for method in ['GET', 'PUT']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s():" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_device", node.name()])

    def handle_publisher_resource(self, node):
        for method in ['GET', 'POST', 'PUT', 'DELETE']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s():" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_device", node.name()])

    def output(self):

        # get all created files
        files = self._out.flush()
        new_files_dic = {}

        for file_name, pycode in files.items():
            # append to each file its correct file extension
            new_files_dic[file_name + ".py"] = pycode

        # create on the fly a requirements.txt file
        requirements = "\n".join(['flask'])
        new_files_dic['requirements.txt'] = requirements

        return new_files_dic