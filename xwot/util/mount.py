#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       14.06.2015

"""

from __future__ import absolute_import


class VocabMounter(object):

    def mount(self):
        raise NotImplementedError


class FlaskMounter(VocabMounter):

    def __init__(self, app, vocab_builder):
        self._app = app
        vocab, class_contexts = vocab_builder.output()
        self._vocab = vocab
        self._class_contexts = class_contexts

        from xwot.util.flask import hydra_link
        doc = vocab_builder.documentation
        self._link = hydra_link(doc.vocab_url)

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

