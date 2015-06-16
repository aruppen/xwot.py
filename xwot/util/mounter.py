#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       14.06.2015

"""

from __future__ import absolute_import


class Mounter(object):

    def mount(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError


class FlaskVocabMounter(Mounter):

    def __init__(self, app, vocabbuilder):
        self._app = app
        self._vocab_builder = vocabbuilder
        vocab, class_contexts = vocabbuilder.output()
        self._vocab = vocab
        self._class_contexts = class_contexts

        from xwot.util.flask import hydra_link
        doc = vocabbuilder.documentation
        self._link = hydra_link(doc.vocab_url)

    def update(self):
        vocab, class_contexts = self._vocab_builder.output()
        self._vocab = vocab
        self._class_contexts = class_contexts

    def _mount_contexts(self):
        from flask import Response

        @self._link
        def contexts(file):
            if file in self._class_contexts:
                doc = self._class_contexts[file]
                return Response(response=doc, status=200, content_type='application/ld+json')
            else:
                return Response(status=404)
        self._app.add_url_rule('/contexts/<string:file>', 'index', contexts)

    def _mount_vocab(self):
        from flask import Response

        @self._link
        def vocab():
            if self._vocab is not None:
                return Response(response=self._vocab, status=200, content_type='application/ld+json')
            else:
                return Response(status=404)
        self._app.add_url_rule('/vocab', 'vocab', vocab)

    def mount(self):
        self._mount_contexts()
        self._mount_vocab()
