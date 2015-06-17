# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

from vocab import Hydra
from serializer import Serializer


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
        collection.describe(title='Collection', description='A Collection', iri='Collection')
        collection.expose('members', description="The members of this collection.", iri=Hydra.member(), writeonly=False,
                          readonly=False)


class JSONLDSerializer(Serializer):

    def __init__(self, annotator):
        self._annotator = annotator
        from serializer import JSONLDSerializer as RealJSONLDSerializer
        self._jsld = RealJSONLDSerializer()
        self._mapping = {}

        # annotate Collection
        Collection.annotate(self._annotator)

        for py_class, klass in self._annotator.get_classes().items():
            self._mapping[py_class] = {
                '@context': "/contexts/%s.jsonld" % py_class.__name__,  # quick and dirty solution
                '@type': "vocab:%s" % py_class.__name__,
                '@id': klass.id_property,
                'embed': klass.embed
            }

        self._jsld.map(mapping=self._mapping)

    def serialize(self, obj):
        # set the context for the top level object
        py_class = obj.__class__
        klass = self._annotator.get_class_from_instance(obj)
        contexts = ["/contexts/%s.jsonld" % py_class.__name__]  # example: /contexts/User.jsonld

        # and add extra content
        contexts += klass.extra_context

        # set @id, @type and @context for the top level obj
        return self._jsld.serialize(obj=obj, id='/', type=klass.iri, context=contexts)
