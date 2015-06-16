# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

from __future__ import absolute_import
from functools import wraps

from flask import make_response
from flask import request
from flask import Response
from xwot.util.serializer import ContentTypeSerializer


def _add_response_header(headers):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in headers.items():
                h[header] = value
            return resp

        return decorated_function

    return decorator


def hydra_link(vocab_url):
    link_header = '<' + vocab_url + '>; rel="http://www.w3.org/ns/hydra/core#apiDocumentation"'

    def wrapped_link(f):
        @wraps(f)
        @_add_response_header({'Link': link_header})
        def decorated_function(*args, **kwargs):
            return f(*args, **kwargs)

        return decorated_function

    return wrapped_link


def mount_vocab(app, vocabbuilder):
    from xwot.util.mounter import FlaskVocabMounter

    mounter = FlaskVocabMounter(app=app, vocabbuilder=vocabbuilder)
    mounter.mount()
    return mounter


SERIALIZER = ContentTypeSerializer()


def serialize(obj, content_type=None):
    if content_type is None:
        cts = request.accept_mimetypes
        content_type = 'application/json'

        if cts:
            content_type, _ = cts[0]

    doc = SERIALIZER.serialize(obj=obj, content_type=content_type)
    return doc
