# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       12.04.2015

"""


class Visitable:

    def accept(self, node):
        raise NotImplementedError


class Visitor(object):
    def visit_entity(self, node):
        raise NotImplementedError

    def visit_resource(self, node):
        raise NotImplementedError

    def visit_device_resource(self, node):
        raise NotImplementedError

    def visit_sensor_resource(self, node):
        raise NotImplementedError

    def visit_service_resource(self, node):
        raise NotImplementedError

    def visit_actuator_resource(self, node):
        raise NotImplementedError

    def visit_tag_resource(self, node):
        raise NotImplementedError

    def visit_context_resource(self, node):
        raise NotImplementedError

    def visit_publisher_resource(self, node):
        raise NotImplementedError

    def visit_device(self, node):
        raise NotImplementedError

    def visit_sensor(self, node):
        raise NotImplementedError

    def visit_actuator(self, node):
        raise NotImplementedError

    def visit_tag(self, node):
        raise NotImplementedError


class BaseVisitor(Visitor):

    def __init__(self):
        self._entity_node = None
        self._nodes = []

    def before(self):
        pass

    def after(self):
        pass

    def before_resource(self, node):
        pass

    def after_resource(self, node):
        pass

    def visit_entity(self, node):
        node.set_name('RootResource')
        self._entity_node = node
        self._nodes.append(node)
        self.before()
        self.handle_entity(node)
        [child.accept(self) for child in node.children() if child.is_virtual()]
        self.after()

    def visit_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_resource(node)
        self.after_resource(node)
        for child in node.children():
            child.accept(self)

    def visit_device_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_device_resource(node)
        self.after_resource(node)
        for child in node.children():
            child.accept(self)

    def visit_sensor_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_sensor_resource(node)
        self.after_resource(node)
        for child in node.children():
            child.accept(self)

    def visit_service_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_service_resource(node)
        self.after_resource(node)

    def visit_actuator_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_actuator_resource(node)
        self.after_resource(node)
        for child in node.children():
            child.accept(self)

    def visit_tag_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_tag_resource(node)
        self.after_resource(node)
        for child in node.children():
            child.accept(self)

    def visit_context_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_context_resource(node)
        self.after_resource(node)
        for child in node.children():
            child.accept(self)

    def visit_publisher_resource(self, node):
        self._nodes.append(node)
        self.before_resource(node)
        self.handle_publisher_resource(node)
        self.after_resource(node)

    def visit_device(self, node):
        pass

    def visit_sensor(self, node):
        pass

    def visit_actuator(self, node):
        pass

    def visit_tag(self, node):
        pass

    def handle_entity(self, node):
        pass

    def handle_resource(self, node):
        pass

    def handle_device_resource(self, node):
        pass

    def handle_sensor_resource(self, node):
        pass

    def handle_tag_resource(self, node):
        pass

    def handle_context_resource(self, node):
        pass

    def handle_service_resource(self, node):
        pass

    def handle_actuator_resource(self, node):
        pass

    def handle_publisher_resource(self, node):
        pass

