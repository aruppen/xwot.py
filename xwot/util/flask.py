#encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       4.06.2015

"""

from __future__ import absolute_import
from functools import wraps

from flask import make_response
from flask import request
from flask import Response
import xwot.util.serializer


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


def mount_vocab(app, vocab_builder):
    from xwot.util.mount import FlaskMounter
    mounter = FlaskMounter(app=app, vocab_builder=vocab_builder)
    mounter.mount()


class Serializer(object):

    def __init__(self, annotator):
        self._serializer = xwot.util.serializer.Serializer(annotator)

    def serialize(self, object, url=''):
        cts = request.accept_mimetypes
        ct = 'application/ld+json'

        if cts:
            ct, _ = cts[0]

        doc = self._serializer.serialize(object=object, content_type=ct, url=url)
        resp = Response(response=doc, status=200, content_type=ct)
        return resp
