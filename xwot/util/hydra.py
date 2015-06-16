# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

from vocab import Hydra
from serializer import Serializer
from serializer import pretty_json


class Collection(object):
    def __init__(self, members=None):
        if members is None:
            self._members = []
        else:
            self._members = members

    @property
    def members(self):
        return self._members

    def get(self, id):
        return self._members[id]

    @classmethod
    def annotate(self, annotator):
        # annotate Collection class
        collection = annotator.klass(Collection)
        collection.describe(title='Collection', description='A Collection', iri=Hydra.Collection())
        collection.expose('members', description="The members of this collection.", iri=Hydra.member(), writeonly=False,
                          readonly=False)


class JSONLDSerializer(Serializer):

    def __init__(self, annotator):
        self._annotator = annotator

    def _visit_object(self, klass, obj, annotator, contexts):
        output = {}

        for prop_name, prop_options in klass.exposed_properties:
            prop_value = getattr(obj, prop_name)
            py_class = prop_value.__class__
            prop_klass = annotator.get_class(py_class)

            if prop_klass is not None:
                output[prop_name] = self._visit_object(prop_klass, obj, annotator, contexts)

            elif type(prop_value) is list:
                output[prop_name] = []
                new_contexts = set()
                for index, item in enumerate(prop_value):
                    item_py_class = item.__class__
                    item_klass = annotator.get_class(item_py_class)
                    _id = index

                    if item_klass is not None:
                        if hasattr(item, 'id'):
                            _id = getattr(item, 'id')

                        item_out = {
                            '@id': "%s/%s" % (item_klass.path, _id),
                            '@type': item_klass.iri
                        }

                        if item_klass.embedded:
                            new_contexts.add("/contexts/%s.jsonld" % item_py_class.__name__)
                            _item_out = self._visit_object(item_klass, item, annotator, contexts)
                            item_out.update(_item_out)
                    else:
                        item_out = item
                    output[prop_name].append(item_out)

                for context in new_contexts:
                    contexts.append(context)

            else:
                output[prop_name] = prop_value.__str__()

        return output

    def build_dic(self, obj, url=''):
        py_class = object.__class__
        klass = self._annotator.get_class(py_class)
        contexts = ["%s/contexts/%s.jsonld" % (url, py_class.__name__)]
        contexts += klass.extra_context

        output = {
            '@id': '/',
            '@context': contexts,
            '@type': py_class.__name__
        }

        if klass is not None:
            _out = self._visit_object(klass, obj, self._annotator, contexts)
            print _out
            output.update(_out)

        return output

    def serialize(self, obj):
        output = self.build_dic(object)
        return pretty_json(output)

