# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       25.04.2015

"""

from helper import OutputPrinter
from xwot.compiler.frontend import visitor


class KleinBackendBuilder(visitor.BaseVisitor):
    def __init__(self):
        visitor.BaseVisitor.__init__(self)
        self._out = OutputPrinter()

    def before(self):
        self._out.code([
                           '#',
                           '# Generated by xwot compiler.',
                           '#',
                           '# Klein xwot application.',
                           '#',
                           '',
                           'import os',
                           'from yadp.device import Description',
                           '',
                           'from xwot.util import local_ip',
                           'from xwot.util import create_description',
                           'from xwot.util import dir_path',
                           'from xwot.util import parent_dir_path',
                           '',
                           '# base config',
                           'ip = local_ip()',
                           'port = 5000',
                           'http_addr = "http://%s:%s/" % (ip, port)',
                           'module_dir_path = dir_path(__file__)',
                           'app_dir_path = parent_dir_path(__file__)',
                           'xwot_file = os.path.join(app_dir_path, "device.xwot")',
                           '',
                           'jsonld_description_str = create_description(xwot_file=xwot_file, base=http_addr)',
                           'yadp_description = Description(content_type="application/ld+json", content=jsonld_description_str)',
                           '',
                           '',
                           'from klein import Klein',
                           'app = Klein()',
                           ], ["xwot_app", "__init__"])

    def after(self):
        self._out.code([
                           "import %s" % node.name() for node in self._nodes
                       ], ["xwot_app", "__init__"])

        self._out.code([
                           '#',
                           '# Generated by xwot compiler.',
                           '#',
                           '# Klein xwot application.',
                           '#',
                           '',
                           'import xwot_app',
                           'from xwot_app import app',
                           '',
                           'import yadp',
                           'yadp.debug()',
                           '',
                           'from yadp import service',
                           'from yadp.device import Device',
                           '',
                           "device = Device(urn='urn:xwot:Device', url=xwot_app.http_addr, descriptions=[xwot_app.yadp_description])",
                           '',
                           'service = service()',
                           'service.register(device=device, passive=True)',
                           '',
                           "",
                           "if __name__ == '__main__':",
                           self._out.indent([
                               "app.run(host='0.0.0.0', port=xwot_app.port)"
                           ])
                       ], ['runserver'])

    def before_resource(self, node):
        self._out.code([
                           '#',
                           '# Generated by xwot compiler.',
                           '#',
                           '# Klein xwot application.',
                           '#',
                           "# Type:       %s" % node.type(),
                           "# Resource:   %s" % node.name(),
                           "# Path:       %s" % node.fullpath(),
                           '#',
                           '',
                           'from xwot_app import app',
                           ''
                       ], ["xwot_app", node.name()])

    def handle_entity(self, node):
        self._out.code([
                           '#',
                           '# Generated by compiler compiler.',
                           '#',
                           '# Klein xwot application.',
                           '#',
                           "# Type:       %s" % node.type(),
                           "# Resource:   %s" % node.name(),
                           "# Path:       %s" % node.fullpath(),
                           '#',
                           '',
                           'import xwot_app',
                           'from xwot_app import app',
                           '',
                           '',
                           "@app.route('/')",
                           'def home(request):',
                           self._out.indent([
                               "request.setHeader('Content-Type', 'application/ld+json')",
                               'return xwot_app.jsonld_description_str'
                           ])
                       ], ["xwot_app", node.name()])

    def handle_resource(self, node):
        for method in ['GET', 'POST', 'PUT', 'DELETE']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s(request):" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_app", node.name()])

    def handle_device_resource(self, node):
        for method in ['GET', 'POST', 'PUT']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s(request):" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_app", node.name()])

    def handle_sensor_resource(self, node):
        for method in ['GET']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s(request):" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_app", node.name()])

    def handle_tag_resource(self, node):
        for method in ['GET']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s(request):" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_app", node.name()])

    def handle_context_resource(self, node):
        for method in ['GET', 'POST', 'PUT']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s(request):" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_app", node.name()])

    def handle_service_resource(self, node):
        for method in ['GET', 'POST', 'PUT', 'DELETE']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s(request):" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_app", node.name()])

    def handle_actuator_resource(self, node):
        for method in ['GET', 'PUT']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s(request):" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_app", node.name()])

    def handle_publisher_resource(self, node):
        for method in ['GET', 'POST', 'PUT', 'DELETE']:
            self._out.code([
                               '#',
                               "# %s '%s'" % (method.upper(), node.fullpath()),
                               '#',
                               "@app.route('%s', methods=['%s'])" % (node.fullpath(), method),
                               "def handle%s_%s(request):" % (node.fullpath().replace("/", "_"), method),
                               self._out.indent([
                                   'return "Name: %s , Hello at: %s"' % (node.name(), node.fullpath())
                               ])
                           ], ["xwot_app", node.name()])

    def output(self):

        # get all created files
        files = self._out.flush()
        new_files_dic = {}

        for file_name, pycode in files.items():
            # append to each file its correct file extension
            new_files_dic[file_name + ".py"] = pycode

        # create on the fly a requirements.txt file
        requirements = "\n".join(['klein'])
        new_files_dic['requirements.txt'] = requirements

        return new_files_dic