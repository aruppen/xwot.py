# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

from vocab import Hydra
from serializer import Serializer


class Collection(object):

    __expose__ = ['members']

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
        klass = annotator.klass(Collection)
        klass.describe_class(title='Collection', description='A Collection', iri=Hydra.Collection())
        klass.describe_property('members', description="The members of this collection.", iri=Hydra.member(),
                                writeonly=False, readonly=False)


class JSONLDSerializer(Serializer):

    def __init__(self, annotator):
        self._annotator = annotator
        from serializer import JSONLDSerializer as _JSONLDSerializer
        self._jsld = _JSONLDSerializer()
        self._mapping = {}

        # annotate Collection
        Collection.annotate(self._annotator)

        for py_class, klass in self._annotator.get_classes().items():
            contexts = ["/contexts/%s.jsonld" % py_class.__name__]
            types = ["%s" % py_class.__name__]

            contexts += klass.extra_contexts
            types += klass.extra_types

            contexts, types = self._simplify_metadata(contexts, types)

            self._mapping[py_class] = {
                '@context': contexts,  # quick and dirty solution
                '@type': types,
                '@id': klass.id_property,
                'id_prefix': klass.id_prefix,
                'embed': klass.embed
            }

        self._jsld.map(mapping=self._mapping)

    def serialize(self, obj, **kwargs):
        contexts = []
        types = []
        path = kwargs.get('path', '/')

        # set the context for the top level object
        klass = self._annotator.get_class_from_instance(obj)
        if klass is not None:
            py_class = obj.__class__
            contexts = ["/contexts/%s.jsonld" % py_class.__name__]  # example: /contexts/User.jsonld
            types = [py_class.__name__]

        # and add extra content
        contexts += klass.extra_contexts
        types += klass.extra_types

        contexts, types = self._simplify_metadata(contexts, types)

        # set @id, @type and @context for the top level obj
        return self._jsld.serialize(obj=obj, id=str(path), type=types, context=contexts)

    def _simplify_metadata(self, contexts, types):
        if len(contexts) == 0:
            contexts = False
        elif len(contexts) == 1:
            contexts = contexts[0]

        if len(types) == 0:
            types = False
        elif len(types) == 1:
            types = types[0]
        return contexts, types