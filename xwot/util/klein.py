# encoding: utf-8
"""
@author     Alexander Rüedlinger <a.rueedlinger@gmail.com>
@date       13.07.2015

"""

from __future__ import absolute_import
from functools import wraps

__all__ = ['cors', 'make_response']

SERIALIZERS = {
    'application/json': lambda obj: obj.to_json(),
    'application/xml': lambda obj: obj.to_xml(),
    'text/plain': lambda obj: obj.to_html(),
    'application/ld+json': lambda obj: obj.to_jsonld()
}

# TODO: fix bug
def cors(origin='*', methods=None, max_age=2520, headers=None):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    else:
        methods = 'GET, OPTIONS'

    if headers is not None:
        headers = ', '.join(headers)
    else:
        headers = 'x-prototype-version,x-requested-with'

    def deco(f):
        def _call(f, *_args, **_kwargs):
            return f(*_args, **_kwargs)

        def _f(request, *a, **kw):
            request.setHeader('Access-Control-Allow-Origin', origin)
            request.setHeader('Access-Control-Allow-Methods', methods)
            request.setHeader('Access-Control-Allow-Headers', headers)
            request.setHeader('Access-Control-Max-Age', max_age)
            return _call(f, request, *a, **kw)
        return _f

    return deco


def make_response(obj, request, default='application/ld+json', status=200):
    content_type = request.getHeader('Accept')

    if content_type in SERIALIZERS:
        fun_serializer = SERIALIZERS[content_type]
        doc = fun_serializer(obj)
        request.setHeader('Content-Type', content_type)
        request.setResponseCode(status)
        return doc
    else:
        fun_serializer = SERIALIZERS[default]
        doc = fun_serializer(obj)
        request.setHeader('Content-Type', default)
        request.setResponseCode(status)
        return doc


